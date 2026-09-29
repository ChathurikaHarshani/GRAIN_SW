"""Verify Pace defaults with multiple crop years and growers."""
import ast
from datetime import date
from pathlib import Path
import sqlite3
import unittest
from unittest.mock import MagicMock, patch

import app as main


class PaceTest(unittest.TestCase):
    def setUp(self):
        source = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text())
        route = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'pace')
        self.lookup = next(n.value for n in ast.walk(route)
                           if isinstance(n, ast.Constant) and isinstance(n.value, str)
                           and 'MIN(h.Harvest_Date)' in n.value).replace('%s', '?')
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.executescript('''
            CREATE TABLE Department (Dpt_ID, Grower_ID);
            CREATE TABLE Field (Field_ID, Dpt_ID, Crop_Year);
            CREATE TABLE Harvest (Field_ID, Harvest_Date);
            INSERT INTO Department VALUES (1, 1), (2, 2);
            INSERT INTO Field VALUES (1, 1, 2024), (2, 1, 2026), (3, 2, 2027), (4, 1, 2027);
            INSERT INTO Harvest VALUES (1, '2024-08-01'), (2, '2026-09-10'),
                (2, '2026-09-01'), (3, '2026-07-01'), (4, '2027-09-01');
        ''')

    def test_first_date_of_latest_active_crop_year_is_grower_scoped(self):
        self.assertEqual(self.db.execute(self.lookup, (1, '2026-09-29')).fetchone()[0], '2026-09-01')

    def test_falls_back_to_latest_available_harvest_year(self):
        self.assertEqual(self.db.execute(self.lookup, (1, '2025-09-29')).fetchone()[0], '2024-08-01')

    def test_no_harvest_returns_no_default_record(self):
        self.assertIsNone(self.db.execute(self.lookup, (3, '2026-09-29')).fetchone())

    def test_date_controls_default_and_override(self):
        user = main.User(dict(id=1, username='test', role='admin', password_hash=''),
                         dict(Grower_ID=1, membership_role='admin', membership_status='active'))
        conn = MagicMock()
        conn.cursor.return_value.fetchall.return_value = []
        today = date.today()
        with patch('flask_login.utils._get_user', return_value=user), \
                patch.object(main, 'get_conn', return_value=conn), \
                patch.object(main, 'render_template', return_value='Pace') as render:
            client = main.app.test_client()
            for query, record, expected_start, expected_end in [
                ('', {'first_date': date(2024, 9, 1)}, date(2024, 9, 1), today),
                ('?start=&end=', None, today, today),
                ('?start=2024-01-01&end=2024-12-31', {'first_date': today}, date(2024, 1, 1), date(2024, 12, 31)),
                ('?start=2024-01-01', {'first_date': today}, date(2024, 1, 1), today),
            ]:
                with self.subTest(query=query):
                    conn.cursor.return_value.fetchone.return_value = record
                    self.assertEqual(client.get('/pace' + query).status_code, 200)
                    self.assertEqual(render.call_args.kwargs['start_date'], expected_start)
                    self.assertEqual(render.call_args.kwargs['end_date'], expected_end)


if __name__ == '__main__':
    unittest.main()
