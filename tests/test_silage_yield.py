"""Exercise the production silage lookup against isolated harvest data."""
import ast
from pathlib import Path
import sqlite3
import unittest


class SilageYieldTest(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8'))
        names = {'calculated_bushels_sql', '_silage_base_field_name', 'populate_silage_yields'}
        module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                                  and n.name in names], type_ignores=[])
        self.scope = {}
        exec(compile(ast.fix_missing_locations(module), 'app.py', 'exec'), self.scope)
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
            CREATE TABLE Department (Dpt_ID INTEGER, Grower_ID INTEGER);
            CREATE TABLE Field (Field_ID INTEGER, Field_Name TEXT, Dpt_ID INTEGER,
                                Crop_Year INTEGER, Acres REAL);
            CREATE TABLE Crop (Crop_ID INTEGER, Crop_Code TEXT, Crop_Name TEXT,
                               Weight_PerBushel REAL, Base_MC REAL);
            CREATE TABLE Harvest (Field_ID INTEGER, Crop_ID INTEGER,
                                  Gross_Weight REAL, Tare_Weight REAL, MC REAL, Bushels REAL);
            INSERT INTO Department VALUES (1,1),(2,1),(3,2);
            INSERT INTO Crop VALUES (1,'C','Corn',56,15.5),(2,'S','Soybeans',60,13);
            INSERT INTO Field VALUES (1,'2628',1,2026,5),(2,'2628',1,2025,5),
                (3,'2628',2,2026,5),(4,'2628',3,2026,5);
            INSERT INTO Harvest VALUES (1,1,66080,0,15.5,NULL),
                (2,1,28000,0,15.5,NULL),(3,1,56000,0,15.5,NULL),
                (4,1,112000,0,15.5,NULL),(1,2,6000,0,13,NULL);
        ''')
        db = self.db

        class Cursor:
            def execute(self, sql, params):
                self.rows = db.execute(sql.replace('%s', '?'), params)

            def fetchall(self):
                return [dict(row) for row in self.rows.fetchall()]

        self.cur = Cursor()

    def resolve(self, manual=None, **changes):
        field = dict(Field_Name='2628-silage', Dpt_ID=1, Crop_Year=2026,
                     Acres=30, Silage_Bu_Per_Acre=manual)
        field.update(changes)
        self.scope['populate_silage_yields'](self.cur, [field], 1)
        return field

    def test_nathans_example_and_crop_isolation(self):
        field = self.resolve()
        self.assertEqual(field['Effective_Silage_Yield'], 236)
        self.assertEqual(field['Acres'] * field['Effective_Silage_Yield'], 7080)
        self.assertEqual(field['Silage_Yield_Source'], 'From grain harvest')

    def test_year_department_and_grower_isolation(self):
        self.assertEqual(self.resolve(Crop_Year=2025)['Effective_Silage_Yield'], 100)
        self.assertEqual(self.resolve(Dpt_ID=2)['Effective_Silage_Yield'], 200)
        self.assertIsNone(self.resolve(Dpt_ID=3)['Effective_Silage_Yield'])

    def test_manual_override(self):
        self.assertEqual(self.resolve(250)['Effective_Silage_Yield'], 250)
        self.assertEqual(self.resolve(250)['Silage_Yield_Source'], 'Manual')

    def test_missing_harvest_or_acres_stays_blank(self):
        self.assertIsNone(self.resolve(Crop_Year=2024)['Effective_Silage_Yield'])
        self.db.execute('UPDATE Field SET Acres=0 WHERE Field_ID=1')
        self.assertIsNone(self.resolve()['Effective_Silage_Yield'])

    def test_recalculates_after_acreage_and_harvest_changes(self):
        self.db.execute('UPDATE Field SET Acres=10 WHERE Field_ID=1')
        self.assertEqual(self.resolve()['Effective_Silage_Yield'], 118)
        self.db.execute('INSERT INTO Harvest VALUES (1,1,NULL,NULL,NULL,1180)')
        self.assertEqual(self.resolve()['Effective_Silage_Yield'], 236)

    def test_ambiguous_companion_stays_blank(self):
        self.db.execute("INSERT INTO Field VALUES (5,'2628',1,2026,5)")
        self.db.execute('INSERT INTO Harvest VALUES (5,1,NULL,NULL,NULL,1000)')
        self.assertIsNone(self.resolve()['Effective_Silage_Yield'])


if __name__ == '__main__':
    unittest.main()
