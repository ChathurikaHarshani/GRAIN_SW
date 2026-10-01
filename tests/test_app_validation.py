"""Request regressions with mocked database writes; no application data changes."""
from datetime import date
import unittest
from unittest.mock import MagicMock, patch

from werkzeug.exceptions import BadRequest
import app as main


class AppValidationTest(unittest.TestCase):
    def setUp(self):
        user = main.User(dict(id=1, username='test', role='admin', password_hash=''),
                         dict(Grower_ID=1, membership_role='admin', membership_status='active'))
        self.user_patch = patch('flask_login.utils._get_user', return_value=user)
        self.user_patch.start()
        self.addCleanup(self.user_patch.stop)
        self.conn = MagicMock()
        self.cur = self.conn.cursor.return_value
        self.cur.fetchall.return_value = []
        self.cur.execute.side_effect = self.query_result
        self.db_patch = patch.object(main, 'get_conn', return_value=self.conn)
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        self.client = main.app.test_client()
        self.form = dict(harvest_id='7', load_num='42', harvest_date='2026-09-29',
                         field_id='1', crop_id='1', cart_id='1', storloc_id='1',
                         gross='56000', tare='1000', mc='15', truck_id='460A', note='Keep this note')

    def query_result(self, sql, params=()):
        self.cur.fetchone.return_value = None
        if 'WHERE h.Harvest_ID = %s' in sql:
            self.cur.fetchone.return_value = dict(Harvest_ID=7, Field_ID=1, Crop_ID=1,
                Cart_ID=1, Truck_ID='496A', StorLoc_ID=1, Load_Num='41', Harvest_Date=date(2026, 9, 28),
                MC=14, Gross_Weight=55000, Tare_Weight=1000, Note='Old note')
        elif 'SELECT f.Dpt_ID' in sql:
            self.cur.fetchone.return_value = dict(Dpt_ID=1)
        elif 'SELECT Cart_ID FROM Cart' in sql:
            self.cur.fetchone.return_value = dict(Cart_ID=1)
        elif 'SELECT StorLoc_ID FROM Storage_Location' in sql:
            self.cur.fetchone.return_value = dict(StorLoc_ID=1)
        elif 'SELECT Weight_PerBushel' in sql:
            self.cur.fetchone.return_value = dict(Weight_PerBushel=56, Base_MC=15.5)
        elif 'MIN(h.Harvest_Date)' in sql:
            self.cur.fetchone.return_value = dict(first_date=None)

    def test_rejected_edit_keeps_id_and_entered_values(self):
        self.form['field_id'] = ''
        response = self.client.post('/harvest-query', data=self.form)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="harvest_id" value="7"', response.data)
        self.assertIn(b'Update Load', response.data)
        self.assertIn(b'value="Keep this note"', response.data)
        self.assertIn(b'value="56000"', response.data)
        self.assertIn(b'value="460A"', response.data)
        self.conn.commit.assert_not_called()

    def test_invalid_harvest_numbers_and_dates_show_validation(self):
        for key, value in [('gross', 'bad'), ('mc', 'nan'), ('tare', 'inf'),
                           ('field_id', 'bad'), ('harvest_date', '2026-02-30')]:
            with self.subTest(key=key):
                response = self.client.post('/harvest-query', data=dict(self.form, **{key: value}))
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Choose valid field', response.data)
                self.assertIn(b'name="harvest_id" value="7"', response.data)
        self.conn.commit.assert_not_called()

    def test_successful_edit_updates_and_closes_connection(self):
        response = self.client.post('/harvest-query', data=self.form)
        self.assertEqual(response.status_code, 302)
        queries = [call.args[0] for call in self.cur.execute.call_args_list]
        self.assertTrue(any('UPDATE Harvest' in sql for sql in queries))
        self.assertFalse(any('INSERT INTO Harvest' in sql for sql in queries))
        self.conn.commit.assert_called_once()
        self.conn.close.assert_called_once()

    def test_edit_form_shows_current_truck(self):
        response = self.client.get('/harvest-query?edit_id=7')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="entry-truck" name="truck_id"', response.data)
        self.assertIn(b'value="496A"', response.data)

    def test_truck_update_allows_unassigned_cart(self):
        self.form['cart_id'] = ''
        response = self.client.post('/harvest-query', data=self.form)
        self.assertEqual(response.status_code, 302)
        update = next(call for call in self.cur.execute.call_args_list
                      if 'UPDATE Harvest' in call.args[0])
        self.assertEqual(update.args[1][:2], (None, '460A'))
        self.conn.commit.assert_called_once()

    def test_invalid_season_year_returns_400_before_database(self):
        response = self.client.get('/season-setup?target_year=bad')
        self.assertEqual(response.status_code, 400)
        self.conn.cursor.assert_not_called()

    def test_report_invalid_and_reversed_ranges_return_400(self):
        for path in ['/billing', '/pace', '/delivery', '/reconcile']:
            for query in ['?start=bad', '?start=2026-09-29&end=2026-09-01']:
                with self.subTest(path=path, query=query):
                    self.assertEqual(self.client.get(path + query).status_code, 400)

    def test_billing_empty_date_controls_use_defaults(self):
        response = self.client.get('/billing?start=&end=')
        self.assertEqual(response.status_code, 200)

    def test_date_range_defaults_and_overflow(self):
        start = date(2026, 9, 1)
        end = date(2026, 9, 30)
        self.assertEqual(main.report_date_range('', '', start, end), (start, end))
        self.assertEqual(main.report_date_range('', '', start, days=1), (start, date(2026, 9, 2)))
        with self.assertRaises(BadRequest):
            main.report_date_range('9999-12-31', '', start, days=60)


if __name__ == '__main__':
    unittest.main()
