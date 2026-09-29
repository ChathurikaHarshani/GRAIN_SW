"""Run the production edit lookup against joined tables with overlapping columns."""
import ast
from pathlib import Path
import sqlite3
import unittest


class HarvestEditTest(unittest.TestCase):
    def setUp(self):
        source = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text())
        route = next(node for node in source.body
                     if isinstance(node, ast.FunctionDef) and node.name == 'harvest_query')
        edit_branch = next(node for node in route.body
                           if isinstance(node, ast.If)
                           and isinstance(node.test, ast.Name)
                           and node.test.id == 'selected_edit_id')
        self.query = edit_branch.body[0].value.args[0].value.replace('%s', '?')
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
            CREATE TABLE Department (Dpt_ID, Grower_ID);
            CREATE TABLE Field (Field_ID, Dpt_ID, Crop_ID);
            CREATE TABLE Harvest (Harvest_ID, Cart_ID, Field_ID, Crop_ID, Dpt_ID,
                StorLoc_ID, Load_Num, Harvest_Date, MC, Gross_Weight, Tare_Weight, Note);
            INSERT INTO Department VALUES (10, 1), (20, 2);
            INSERT INTO Field VALUES (100, 10, 99), (200, 20, 99);
            INSERT INTO Harvest VALUES
                (1, 3, 100, 4, 10, 5, '42', '2026-09-29', 15, 56000, 1000, 'Edit me'),
                (2, 3, 200, 4, 20, NULL, '43', '2026-09-29', 16, 57000, 1000, NULL);
        ''')

    def test_edit_returns_harvest_values(self):
        row = dict(self.db.execute(self.query, (1, 1)).fetchone())
        self.assertEqual(row, dict(Harvest_ID=1, Cart_ID=3, Field_ID=100,
            Crop_ID=4, StorLoc_ID=5, Load_Num='42', Harvest_Date='2026-09-29',
            MC=15, Gross_Weight=56000, Tare_Weight=1000, Note='Edit me'))

    def test_other_grower_load_is_not_returned(self):
        self.assertIsNone(self.db.execute(self.query, (2, 1)).fetchone())

    def test_missing_load_is_not_returned(self):
        self.assertIsNone(self.db.execute(self.query, (999, 1)).fetchone())

    def test_load_without_storage_can_be_opened(self):
        row = self.db.execute(self.query, (2, 2)).fetchone()
        self.assertIsNone(row['StorLoc_ID'])


if __name__ == '__main__':
    unittest.main()
