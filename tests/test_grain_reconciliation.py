import unittest
from decimal import Decimal
from grain_reconciliation import settlement
from unittest.mock import MagicMock, patch
from datetime import date
import app as main


class SettlementTest(unittest.TestCase):
    def quotes(self):
        return [dict(Year=2025, Month=10, Day=d, Market_Price='4.06', Crop_Code='C', Crop_Name='Corn') for d in range(1, 6)]

    def delivery(self, **changes):
        row = dict(DelLoc_ID=1, department='Beef Feedlot', Crop_Code='C', Crop_Name='Corn', bushels=100, billed=400)
        row.update(changes)
        return row

    def test_department_totals_and_credit(self):
        result = settlement([self.delivery(), self.delivery(DelLoc_ID=2, department='Main Feedmill', billed=420)], self.quotes(), 2025)
        self.assertEqual(result['averages']['corn'], Decimal('4.10'))
        self.assertEqual(result['total']['corn']['bushels'], 200)
        self.assertEqual(result['rows'][0]['corn']['due'], 10)
        self.assertEqual(result['rows'][1]['corn']['due'], -10)
        self.assertEqual(result['total']['total_due'], 0)

    def test_hmc_milo_and_missing_billing(self):
        result = settlement([self.delivery(Crop_Code='HMC', Crop_Name='High Moisture Corn', billed=380),
                             self.delivery(Crop_Code='M', Crop_Name='Milo')], self.quotes(), 2025)
        self.assertEqual(result['total']['corn']['due'], Decimal('9.50'))
        self.assertIsNone(result['total']['milo']['due'])
        self.assertIsNone(result['total']['total_due'])
        result = settlement([self.delivery(billed=None)], self.quotes(), 2025)
        self.assertIsNone(result['total']['corn']['billed'])
        self.assertIsNone(result['total']['corn']['due'])

    def test_no_quotes_and_empty(self):
        self.assertIsNone(settlement([self.delivery()], [], 2025)['total']['total_due'])
        self.assertEqual(settlement([], [], 2025)['total']['total_due'], 0)

    def test_route_renders_and_scopes_deliveries(self):
        user = main.User(dict(id=1, username='viewer', role='viewer', password_hash=''),
                         dict(Grower_ID=7, membership_role='viewer', membership_status='active'))
        conn = MagicMock()
        cur = conn.cursor.return_value
        cur.fetchall.side_effect = [self.quotes(), [self.delivery()]]
        cur.fetchone.return_value = {'count': 2}
        context = dict(start_date=date(2026, 1, 1), end_date=date(2026, 9, 9), crops=[],
                       harvest_sum={}, delivery_sum={}, diff={}, status_counts={}, crop_rows=[], rows=[])
        with patch('flask_login.utils._get_user', return_value=user), patch.object(main, 'get_conn', return_value=conn), \
                patch.object(main, 'build_reconcile_context', return_value=context):
            result = main.app.test_client().get('/reconcile?settlement_year=2025&start=2026-01-01&end=2026-09-09')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Beef Feedlot', result.data)
            self.assertIn(b'$10.00', result.data)
            self.assertIn(b'2 deliveries have no crop year', result.data)
            query, params = cur.execute.call_args_list[1].args
            self.assertIn('d.Grower_ID=%s AND d.Crop_Year=%s', query)
            self.assertEqual(params, (7, 2025, date(2026, 9, 9)))


if __name__ == '__main__':
    unittest.main()
