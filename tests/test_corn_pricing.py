import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

import app as main
from corn_pricing import build_report


class CornPricingTest(unittest.TestCase):
    def quotes(self):
        return [dict(Year=2025, Month=10, Day=d, Market_Price=p)
                for d, p in zip([1, 2, 3, 6, 7], ['3.74', '3.79', '3.76', '3.79', '3.77'])]

    def test_example_and_crop_year_order(self):
        rows, average, count = build_report(self.quotes(), 2025)
        self.assertEqual(rows[0]['corn'], Decimal('3.81'))
        self.assertEqual(rows[0]['hmc'], Decimal('3.62'))
        self.assertEqual((rows[-1]['month'], rows[-1]['year']), ('September', 2026))
        self.assertEqual((count, average['corn']), (1, Decimal('3.81')))

    def test_incomplete_duplicate_invalid_and_extra_dates(self):
        for records in [self.quotes()[:4], self.quotes() + [self.quotes()[0]],
                        self.quotes() + [dict(Year=2025, Month=10, Day='Mon', Market_Price=4)]]:
            with self.subTest(records=records):
                rows, average, count = build_report(records, 2025)
                self.assertIsNone(rows[0]['corn'])
                self.assertIsNone(average['corn'])
                self.assertEqual(count, 0)
        records = self.quotes() + [dict(Year=2025, Month=10, Day=8, Market_Price=100)]
        self.assertEqual(build_report(records, 2025)[0][0]['corn'], Decimal('3.81'))

    def test_viewer_report_csv_and_scoped_query(self):
        user = main.User(dict(id=1, username='viewer', role='viewer', password_hash=''),
                         dict(Grower_ID=7, membership_role='viewer', membership_status='active'))
        conn = MagicMock()
        conn.cursor.return_value.fetchall.return_value = self.quotes()
        with patch('flask_login.utils._get_user', return_value=user), patch.object(main, 'get_conn', return_value=conn):
            client = main.app.test_client()
            response = client.get('/reports/corn-pricing?year=2025')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'$3.81', response.data)
            query, params = conn.cursor.return_value.execute.call_args.args
            self.assertIn('mp.Grower_ID=%s', query)
            self.assertEqual(params, (7, 202510, 202609))
            response = client.get('/reports/corn-pricing?year=2025&format=csv')
            self.assertIn(b'October,2025,3.81,3.62', response.data)
            self.assertEqual(client.get('/reports/corn-pricing?year=oops').status_code, 400)


if __name__ == '__main__':
    unittest.main()
