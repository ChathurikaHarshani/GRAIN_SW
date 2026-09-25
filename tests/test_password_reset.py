import hashlib
from unittest.mock import patch
import bcrypt
import app as main
import password_reset as reset
import test_invitations as invitation_tests

class PasswordResetTest(invitation_tests.InvitationsTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tables=('password_resets',)+cls.tables
        cls.reset_db=patch.object(reset,'get_conn',cls.connect)
        cls.reset_db.start()
    @classmethod
    def tearDownClass(cls):
        cls.reset_db.stop()
        super().tearDownClass()
    def setUp(self):
        self.sql("DROP TABLE IF EXISTS password_resets")
        super().setUp()
        conn=self.connect();cur=conn.cursor();reset.ensure_schema(cur);conn.commit();cur.close();conn.close()
        self.sql("INSERT INTO user_emails VALUES (2,'person@unl.edu',UTC_TIMESTAMP()),(1,'admin@unl.edu',UTC_TIMESTAMP())")
        self.mail_patch=patch.object(reset,'send_reset')
        self.mail=self.mail_patch.start()
        self.addCleanup(self.mail_patch.stop)
    def request_reset(self,email='person@unl.edu'):
        return self.client.post('/forgot-password',data={'email':email,'csrf_token':'test-csrf'})
    def finish(self,token):
        return self.client.post('/reset-password/'+token,data=dict(password='newpassword123',confirm_password='newpassword123',csrf_token='test-csrf'))
    def test_reset_success_replay_sessions(self):
        other=main.app.test_client()
        other.post('/login',data=dict(username='existing',password='password123'))
        self.request_reset();token=self.mail.call_args.args[1]
        row=self.sql('SELECT * FROM password_resets')[0]
        self.assertEqual(row['token_hash'],hashlib.sha256(token.encode()).hexdigest())
        self.assertEqual(self.client.get('/reset-password/'+token).status_code,200)
        self.assertIn(b'password has been updated',self.finish(token).data)
        self.assertEqual(self.client.get('/reset-password/'+token).status_code,410)
        self.assertEqual(other.get('/users').status_code,302)
        password=self.sql('SELECT password_hash FROM users WHERE id=2')[0]['password_hash']
        self.assertTrue(bcrypt.checkpw(b'newpassword123',password.encode()))
    def test_admin_rejection_both_stages(self):
        a=self.request_reset('admin@unl.edu'); b=self.request_reset('unknown@unl.edu')
        self.assertEqual(a.data,b.data);self.mail.assert_not_called()
        self.request_reset();token=self.mail.call_args.args[1]
        self.sql("UPDATE grower_memberships SET role='admin' WHERE user_id=2")
        self.assertEqual(self.finish(token).status_code,410)
    def test_expiration_resend_rate_limit(self):
        self.request_reset();old=self.mail.call_args.args[1]
        self.request_reset();self.assertEqual(self.mail.call_count,1)
        self.sql('UPDATE password_resets SET requested_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.request_reset();new=self.mail.call_args.args[1]
        self.assertNotEqual(old,new)
        self.assertEqual(self.finish(old).status_code,410)
        self.sql('UPDATE password_resets SET expires_at=UTC_TIMESTAMP()-INTERVAL 1 SECOND')
        self.assertEqual(self.finish(new).status_code,410)
    def test_reset_csrf_unverified_and_disabled(self):
        self.assertEqual(self.client.post('/forgot-password',data=dict(email='person@unl.edu')).status_code,400)
        self.sql('DELETE FROM user_emails WHERE user_id=2');self.request_reset();self.mail.assert_not_called()
        self.sql("INSERT INTO user_emails VALUES (2,'person@unl.edu',UTC_TIMESTAMP())")
        self.sql('UPDATE users SET is_active=0 WHERE id=2');self.request_reset();self.mail.assert_not_called()

    def test_global_admin_and_other_grower_admin(self):
        self.sql("UPDATE users SET role='admin' WHERE id=2")
        self.request_reset();self.mail.assert_not_called()
        self.sql("UPDATE users SET role='user' WHERE id=2")
        self.sql("INSERT INTO grower_memberships (user_id,Grower_ID,role,status) VALUES (2,1,'admin','pending')")
        self.request_reset();self.mail.assert_not_called()

    def test_editor_limit_and_failed_delivery(self):
        self.sql("UPDATE grower_memberships SET role='editor' WHERE user_id=2")
        self.request_reset();self.assertEqual(self.mail.call_count,1)
        self.sql('UPDATE password_resets SET request_count=5, requested_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.request_reset();self.assertEqual(self.mail.call_count,1)
        self.sql('UPDATE password_resets SET window_started=UTC_TIMESTAMP()-INTERVAL 2 HOUR')
        self.mail.side_effect=OSError('mail failure')
        self.request_reset()
        token=self.mail.call_args.args[1]
        self.assertEqual(self.finish(token).status_code,410)

    def test_reset_validation_and_csrf(self):
        self.request_reset();token=self.mail.call_args.args[1]
        self.assertEqual(self.client.post('/reset-password/'+token,data={}).status_code,400)
        result=self.client.post('/reset-password/'+token,data=dict(password='short',confirm_password='short',csrf_token='test-csrf'))
        self.assertEqual(result.status_code,400)
        self.assertEqual(self.client.get('/reset-password/'+token).status_code,200)

# Do not repeat inherited invitation tests against the reset-specific fixture.
for name in dir(invitation_tests.InvitationsTest):
    if name.startswith("test_") and name not in PasswordResetTest.__dict__:
        setattr(PasswordResetTest,name,None)
