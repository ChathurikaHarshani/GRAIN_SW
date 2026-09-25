import hashlib
from unittest.mock import patch
import app as main
import email_verification as verification
import password_reset as reset
import test_invitations as invitation_tests

class EmailVerificationTest(invitation_tests.InvitationsTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tables=('email_verifications','password_resets')+cls.tables
        cls.extra_patches=[patch.object(verification,'get_conn',cls.connect),patch.object(reset,'get_conn',cls.connect)]
        for p in cls.extra_patches:p.start()
    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.extra_patches):p.stop()
        super().tearDownClass()
    def setUp(self):
        self.sql('DROP TABLE IF EXISTS email_verifications')
        self.sql('DROP TABLE IF EXISTS password_resets')
        super().setUp()
        c=self.connect();q=c.cursor();verification.ensure_schema(q);reset.ensure_schema(q);c.commit();q.close();c.close()
        self.mail_patch=patch.object(verification,'send_verification')
        self.mail=self.mail_patch.start();self.addCleanup(self.mail_patch.stop)
    def as_user(self,user_id):
        with self.client.session_transaction() as s:
            s['_user_id']=str(user_id)
    def request_email(self,email='person@unl.edu',password='password123'):
        return self.client.post('/account/email',data=dict(email=email,password=password,csrf_token='test-csrf'))
    def verify(self,token):
        return self.client.post('/verify-email/'+token,data=dict(csrf_token='test-csrf'))
    def test_signup_verifies_without_approving_access(self):
        self.client.get('/logout')
        response=self.client.post('/signup',data=dict(username='signupuser',email='signup@unl.edu',password='password123',confirm_password='password123',grower_id=1,csrf_token='test-csrf'))
        self.assertEqual(response.status_code,302)
        self.assertIn('/account/email',response.location)
        token=self.mail.call_args.args[1]
        self.assertFalse(self.sql('SELECT * FROM user_emails'))
        self.assertEqual(self.client.get('/account/email').status_code,200)
        self.assertIn(b'email is verified',self.verify(token).data)
        member=self.sql("SELECT gm.status FROM grower_memberships gm JOIN users u ON u.id=gm.user_id WHERE u.username='signupuser'")[0]
        self.assertEqual(member['status'],'pending')
        self.assertEqual(self.client.get('/verify-email/'+token).status_code,410)
    def test_existing_user_verified_then_reset_eligible(self):
        self.as_user(2);self.request_email();token=self.mail.call_args.args[1]
        row=self.sql('SELECT * FROM email_verifications')[0]
        self.assertEqual(row['token_hash'],hashlib.sha256(token.encode()).hexdigest())
        self.assertEqual(self.client.get('/verify-email/'+token).status_code,200)
        self.assertFalse(self.sql('SELECT * FROM user_emails'))
        self.verify(token)
        with patch.object(reset,'send_reset') as mail:
            self.client.post('/forgot-password',data=dict(email='person@unl.edu',csrf_token='test-csrf'))
            mail.assert_called_once()
    def test_wrong_account_and_anonymous_cannot_verify(self):
        self.as_user(2);self.request_email();token=self.mail.call_args.args[1]
        self.as_user(1);self.assertEqual(self.verify(token).status_code,410)
        self.client.get('/logout')
        self.assertIn(b'Sign in to the GMS account',self.client.get('/verify-email/'+token).data)
        self.assertFalse(self.sql('SELECT * FROM user_emails'))
    def test_validation_password_csrf_and_verified_conflict(self):
        self.as_user(2)
        self.request_email(email='x@gmail.com');self.mail.assert_not_called()
        self.request_email(password='wrong');self.mail.assert_not_called()
        self.assertEqual(self.client.post('/account/email',data={}).status_code,400)
        self.sql("INSERT INTO user_emails VALUES (1,'person@unl.edu',UTC_TIMESTAMP())")
        self.request_email();self.mail.assert_not_called()
    def test_resend_expiry_and_mail_failure(self):
        self.as_user(2);self.request_email();old=self.mail.call_args.args[1]
        self.request_email();self.assertEqual(self.mail.call_count,1)
        self.sql('UPDATE email_verifications SET requested_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.request_email();new=self.mail.call_args.args[1]
        self.assertNotEqual(old,new);self.assertEqual(self.verify(old).status_code,410)
        self.sql('UPDATE email_verifications SET expires_at=UTC_TIMESTAMP()-INTERVAL 1 SECOND')
        self.assertEqual(self.verify(new).status_code,410)
        self.sql('UPDATE email_verifications SET requested_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.mail.side_effect=OSError('simulated')
        self.assertIn(b'could not be sent',self.request_email().data)
        self.assertIsNone(self.sql('SELECT token_hash FROM email_verifications')[0]['token_hash'])
    def test_verified_admin_still_cannot_reset(self):
        self.request_email(email='admin@unl.edu');self.verify(self.mail.call_args.args[1])
        with patch.object(reset,'send_reset') as mail:
            self.client.post('/forgot-password',data=dict(email='admin@unl.edu',csrf_token='test-csrf'))
            mail.assert_not_called()
    def test_signup_email_required(self):
        self.client.get('/logout')
        data=dict(username='signupuser',password='password123',confirm_password='password123',grower_id=1,csrf_token='test-csrf')
        response=self.client.post('/signup',data=data)
        self.assertIn(b'Enter an @unl.edu',response.data)
        self.assertFalse(self.sql("SELECT id FROM users WHERE username='signupuser'"))
        self.assertIn(b'name="email"',self.client.get('/signup').data)

for name in dir(invitation_tests.InvitationsTest):
    if name.startswith('test_') and name not in EmailVerificationTest.__dict__:
        setattr(EmailVerificationTest,name,None)
