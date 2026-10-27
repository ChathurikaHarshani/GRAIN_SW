"""Warning dismissal is separate from harvest data and scoped to its grower."""
import sqlite3
import unittest
from unittest.mock import MagicMock, patch

import app as main
import harvest_attention as attention


class AttentionQueryTest(unittest.TestCase):
    def test_dismiss_restore_and_other_grower(self):
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.executescript('''
            CREATE TABLE Department(Dpt_ID, Grower_ID);
            CREATE TABLE Field(Field_ID, Dpt_ID);
            CREATE TABLE Harvest(Harvest_ID, Field_ID, Gross_Weight, MC, StorLoc_ID, Bushels);
            CREATE TABLE Harvest_Attention(Harvest_ID, Grower_ID, Dismissed);
            INSERT INTO Department VALUES(1,1),(2,2);
            INSERT INTO Field VALUES(1,1),(2,2);
            INSERT INTO Harvest VALUES(1,1,NULL,15,NULL,100),(2,1,5600,15,1,100),
                (3,2,NULL,NULL,NULL,200);
            INSERT INTO Harvest_Attention VALUES(1,2,1);
        ''')
        sql = '''SELECT h.Harvest_ID FROM Harvest h JOIN Field f ON f.Field_ID=h.Field_ID
            JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=1 AND ''' + attention.ATTENTION_SQL
        self.assertEqual(db.execute(sql).fetchall(), [(1,)])
        db.execute('INSERT INTO Harvest_Attention VALUES(1,1,1)')
        self.assertEqual(db.execute(sql).fetchall(), [])
        self.assertEqual(db.execute('SELECT SUM(Bushels) FROM Harvest WHERE Field_ID=1').fetchone()[0], 200)
        db.execute('UPDATE Harvest_Attention SET Dismissed=0 WHERE Grower_ID=1')
        self.assertEqual(db.execute(sql).fetchall(), [(1,)])


class AttentionRouteTest(unittest.TestCase):
    def setUp(self):
        self.user = main.User(dict(id=4, username='editor', role='editor', password_hash=''),
                              dict(Grower_ID=7, membership_role='editor', membership_status='active'))
        self.conn = MagicMock()
        self.cur = self.conn.cursor.return_value
        self.cur.fetchone.return_value = {'Harvest_ID': 12}
        self.client = main.app.test_client()
        with self.client.session_transaction() as session:
            session['access_csrf'] = 'test-token'
        self.user_patch = patch('flask_login.utils._get_user', return_value=self.user)
        self.db_patch = patch.object(attention, 'get_conn', return_value=self.conn)
        self.user_patch.start()
        self.db_patch.start()
        self.addCleanup(self.user_patch.stop)
        self.addCleanup(self.db_patch.stop)

    def post(self, **changes):
        data = dict(csrf_token='test-token', action='dismiss', reason='Scale ticket')
        data.update(changes)
        return self.client.post('/harvest/12/attention?crop_year=2025&needs_attention=1', data=data)

    def test_dismiss_and_restore_preserve_filters(self):
        for action, value in [('dismiss', 1), ('restore', 0)]:
            with self.subTest(action=action):
                response = self.post(action=action)
                self.assertEqual(response.status_code, 302)
                self.assertIn('crop_year=2025', response.location)
                self.assertIn('needs_attention=1', response.location)
                self.assertEqual(self.cur.execute.call_args.args[1], (12, 7, value, 'Scale ticket', 4))
                self.assertEqual(self.cur.execute.call_args_list[-2].args[1], (12, 7))
        self.assertEqual(self.conn.commit.call_count, 2)

    def test_invalid_csrf_action_and_reason_do_not_write(self):
        for changes in [dict(csrf_token='bad'), dict(action='delete'), dict(reason='x'*501)]:
            self.assertEqual(self.post(**changes).status_code, 400)
        self.conn.commit.assert_not_called()
        self.cur.execute.assert_not_called()

    def test_viewer_cannot_dismiss(self):
        self.user.grower_role = 'viewer'
        self.user.role = 'viewer'
        self.assertEqual(self.post().status_code, 403)
        self.cur.execute.assert_not_called()

    def test_other_grower_or_missing_load_is_not_modified(self):
        self.cur.fetchone.return_value = None
        self.assertEqual(self.post().status_code, 404)
        self.conn.commit.assert_not_called()
        self.conn.rollback.assert_called_once()
        self.cur.close.assert_called_once()
        self.conn.close.assert_called_once()

    def test_get_cannot_mutate(self):
        self.assertEqual(self.client.get('/harvest/12/attention').status_code, 405)

    def test_template_compiles(self):
        main.app.jinja_env.get_template('harvest_query.html')


if __name__ == '__main__':
    unittest.main()
