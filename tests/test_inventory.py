"""Exercise inventory SQL against an in-memory database without app services."""
import ast
from pathlib import Path
import re
import sqlite3
from types import SimpleNamespace
import unittest


class InventoryTest(unittest.TestCase):
    def setUp(self):
        # Load the production calculation without Flask or a configured MySQL server.
        source = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text())
        names = {'calculated_bushels_sql', 'build_inventory_snapshot', 'storage_sort_key'}
        nodes = [node for node in source.body
                 if (isinstance(node, ast.FunctionDef) and node.name in names)
                 or (isinstance(node, ast.Assign) and any(
                     isinstance(target, ast.Name) and target.id == 'INVENTORY_CROP_SQL'
                     for target in node.targets))]
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.row_factory = sqlite3.Row
        self.db.create_function('YEAR', 1, lambda value: value[:4] if value else None)
        self.db.executescript('''
            CREATE TABLE Storage_Location (StorLoc_ID, Bin_Code, Bin_Name, Grower_ID);
            CREATE TABLE Crop (Crop_ID, Crop_Name, Crop_Code, Weight_PerBushel, Base_MC);
            CREATE TABLE Field (Field_ID, Crop_Year TEXT);
            CREATE TABLE Harvest (StorLoc_ID, Crop_ID, Field_ID, Bushels, MC,
                                  Gross_Weight, Tare_Weight);
            CREATE TABLE Delivery (Delivery_ID, StorLoc_ID, Crop_ID, Grower_ID,
                                   Delivery_Date, Bushels, MC, Gross_Weight, Tare_Weight,
                                   Crop_Year TEXT);
            INSERT INTO Storage_Location VALUES (1, 'Bin1', 'Bin1', 1);
            INSERT INTO Crop VALUES (1, 'Corn', 'C', 56, 15.5);
            INSERT INTO Field VALUES (1, 2025), (2, 2026);
            INSERT INTO Harvest VALUES (1, 1, 1, 100, 15, NULL, NULL),
                                       (1, 1, 2, 50, 15, NULL, NULL);
            INSERT INTO Delivery VALUES
                (1, 1, 1, 1, '2026-01-01', 100, 15, NULL, NULL, 2025),
                (2, 1, 1, 1, '2027-01-01', 20, 15, NULL, NULL, 2026),
                (3, 1, 1, 2, '2026-01-01', 999, 15, NULL, NULL, 2026);
        ''')
        db = self.db

        class Cursor:
            def execute(self, sql, params):
                self.result = db.execute(sql.replace('%s', '?'), params)

            def fetchall(self):
                return [dict(row) for row in self.result.fetchall()]

            def close(self):
                pass

        namespace = {'re': re, 'current_user': SimpleNamespace(grower_id=1),
                     'get_conn': lambda: SimpleNamespace(cursor=lambda **kwargs: Cursor(),
                                                        close=lambda: None)}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'app.py', 'exec'), namespace)
        self.snapshot = namespace['build_inventory_snapshot']

    def test_selected_year_excludes_historical_deliveries(self):
        rows, summary, split = self.snapshot('2026')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['Delivered_Bu'], 20)
        self.assertEqual(rows[0]['Current_Bu'], 30)
        self.assertEqual(summary['Corn']['Inventory'], 30)
        self.assertEqual(split['Dry']['Delivered'], 20)

    def test_year_and_crop_filters_together(self):
        rows, _, _ = self.snapshot('2025', 'Corn')
        self.assertEqual(rows[0]['Delivered_Bu'], 100)
        self.assertEqual(rows[0]['Current_Bu'], 0)
        self.assertEqual(self.snapshot('2026', 'Soybeans')[0], [])

    def test_all_years_retains_all_deliveries(self):
        rows, _, _ = self.snapshot()
        self.assertEqual(rows[0]['Delivered_Bu'], 120)
        self.assertEqual(rows[0]['Current_Bu'], 30)

    def test_unassigned_deliveries_are_not_guessed_from_date(self):
        self.db.execute("UPDATE Delivery SET Crop_Year=NULL WHERE Delivery_ID=2")
        rows, _, _ = self.snapshot('2026')
        self.assertEqual(rows[0]['Delivered_Bu'], 0)
        self.assertEqual(self.snapshot()[0][0]['Delivered_Bu'], 120)

    def test_new_year_without_activity_has_no_old_deliveries(self):
        rows, summary, _ = self.snapshot('2027')
        self.assertEqual(rows, [])
        self.assertEqual(summary, {})


if __name__ == '__main__':
    unittest.main()
