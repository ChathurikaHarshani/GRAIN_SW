"""Manual delivery requests use mocked database writes, never production records."""
from datetime import date
from decimal import Decimal
import unittest
from unittest.mock import MagicMock, patch

import app as main


class DeliveryEntryTest(unittest.TestCase):
    def setUp(self):
        self.user = main.User(dict(id=1, username='editor', role='user', password_hash=''),
                              dict(Grower_ID=7, membership_role='editor', membership_status='active'))
        self.conn = MagicMock()
        self.cur = self.conn.cursor.return_value
        self.cur.execute.side_effect = self.query_result
        self.duplicate = False
        self.db_patch = patch.object(main, 'get_conn', return_value=self.conn)
        self.user_patch = patch('flask_login.utils._get_user', return_value=self.user)
        self.db_patch.start()
        self.user_patch.start()
        self.addCleanup(self.db_patch.stop)
        self.addCleanup(self.user_patch.stop)
        self.client = main.app.test_client()
        with self.client.session_transaction() as session:
            session['access_csrf'] = 'test-token'
        self.form = dict(csrf_token='test-token', ticket_num='42', delivery_date='2026-10-05',
                         crop_year='2025', crop_id='8', delloc_id='14', storloc_id='71',
                         mc='15', gross='56000', tare='0', bushels='', price='4.25',
                         gross_sale='', discounts='10', comments='Manual ticket')

    def query_result(self, sql, params=()):
        self.cur.fetchone.return_value = None
        self.cur.fetchall.return_value = []
        if 'FROM Crop ORDER' in sql:
            self.cur.fetchall.return_value = [dict(Crop_ID=8, Crop_Name='Corn', Weight_PerBushel=56, Base_MC=15.5)]
        elif 'FROM Delivery_Location' in sql:
            self.cur.fetchall.return_value = [dict(DelLoc_ID=14, DelLoc_code='E', Location='Elevator')]
        elif 'FROM Storage_Location' in sql:
            self.cur.fetchall.return_value = [dict(StorLoc_ID=71, Bin_Code='B1', Bin_Name='Bin 1')]
        elif 'SELECT Delivery_ID FROM Delivery' in sql and self.duplicate:
            self.cur.fetchone.return_value = dict(Delivery_ID=1)

    def inserted_values(self):
        return next(c.args[1] for c in self.cur.execute.call_args_list if 'INSERT INTO Delivery' in c.args[0])

    def test_form_renders_grower_locations_and_csrf(self):
        response = self.client.get('/delivery/new')
        self.assertEqual(response.status_code, 200)
        for text in (b'Add Delivery', b'E - Elevator', b'B1 - Bin 1', b'value="test-token"'):
            self.assertIn(text, response.data)
        for call in self.cur.execute.call_args_list:
            if 'Location WHERE' in call.args[0]:
                self.assertIn('Grower_ID=%s', call.args[0])
                self.assertEqual(call.args[1], (7,))
        self.conn.commit.assert_not_called()
        self.conn.close.assert_called_once()

    def test_weight_delivery_saves_calculated_quantity_sale_and_original_year(self):
        response = self.client.post('/delivery/new', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertIn('start=2026-10-05', response.location)
        self.assertEqual(self.inserted_values(), (7, 42, date(2026, 10, 5), 2025, 8, 14, 71,
                         15.0, 56000.0, 0.0, 1000.0, 4.25, Decimal('4250.00'), 10.0, 'Manual ticket'))
        self.conn.commit.assert_called_once()
        self.conn.close.assert_called_once()

    def test_bushels_only_and_explicit_sale(self):
        response = self.client.post('/delivery/new', data=dict(self.form, gross='', tare='',
                                   bushels='500', gross_sale='2100'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.inserted_values()[8:11], (None, None, 500.0))
        self.assertEqual(self.inserted_values()[12], 2100.0)

    def test_moisture_adjusts_weight_bushels(self):
        response = self.client.post('/delivery/new', data=dict(self.form, mc='25.5'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.inserted_values()[10], round(1000 * 74.5 / 84.5, 2))

    def test_invalid_inputs_do_not_write_and_keep_values(self):
        for changes in (dict(ticket_num='ABC'), dict(delivery_date='2026-02-30'),
                        dict(crop_year='2027'), dict(crop_year=''), dict(crop_id='99'),
                        dict(delloc_id='99'), dict(storloc_id='99'), dict(gross='nan'),
                        dict(tare='-1'), dict(tare='57000'), dict(mc='100'),
                        dict(price='inf'), dict(discounts='999999'), dict(bushels='500'),
                        dict(gross='', tare='', bushels=''), dict(comments='x' * 256)):
            with self.subTest(changes=changes):
                response = self.client.post('/delivery/new', data=dict(self.form, **changes))
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'role="alert"', response.data)
                self.assertIn(b'value="2026-10-05"' if 'delivery_date' not in changes else b'value="2026-02-30"', response.data)
        self.conn.commit.assert_not_called()
        self.assertFalse(any('INSERT INTO Delivery' in c.args[0] for c in self.cur.execute.call_args_list))

    def test_duplicate_does_not_write(self):
        self.duplicate = True
        response = self.client.post('/delivery/new', data=self.form)
        self.assertIn(b'already exist', response.data)
        self.conn.commit.assert_not_called()

    def test_missing_csrf_is_rejected_before_database(self):
        response = self.client.post('/delivery/new', data=dict(self.form, csrf_token=''))
        self.assertEqual(response.status_code, 400)
        self.conn.cursor.assert_not_called()

    def test_viewer_cannot_open_or_submit(self):
        viewer = main.User(dict(id=2, username='viewer', role='user', password_hash=''),
                           dict(Grower_ID=7, membership_role='viewer', membership_status='active'))
        with patch('flask_login.utils._get_user', return_value=viewer):
            self.assertEqual(self.client.get('/delivery/new').status_code, 403)
            self.assertEqual(self.client.post('/delivery/new', data=self.form).status_code, 403)
        self.conn.cursor.assert_not_called()


if __name__ == '__main__':
    unittest.main()
