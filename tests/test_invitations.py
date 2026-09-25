"""Integration tests using isolated, uniquely named MySQL tables; no emails are sent.

Run: python -m unittest discover -s tests -p test_invitations.py
The configured DB account needs CREATE/DROP TABLE privileges. Production tables are never modified.
"""
import hashlib
from pathlib import Path
import re
import unittest
import uuid
from unittest.mock import patch

import bcrypt
import app as main
import invitations as inv
from db import get_conn


class InvitationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prefix = 'invtest_' + uuid.uuid4().hex[:16] + '_'
        cls.tables = ('user_invitations','user_emails','grower_memberships','users','Grower')
        cls.old_ready = main._access_schema_ready
        main._access_schema_ready = True
        cls.patches = [patch.object(main, 'get_conn', cls.connect), patch.object(inv, 'get_conn', cls.connect),
                       patch.object(inv, 'mail_config', return_value=('approved@unl.edu','https://example.invalid','/sbin/sendmail')),
                       patch.object(inv, 'send_invitation')]
        cls.mocks = [p.start() for p in cls.patches]
        cls.old_testing = main.app.config['TESTING']
        main.app.config['TESTING'] = True

    @classmethod
    def connect(cls):
        class Cursor:
            def __init__(self, raw):
                self.raw = raw
            def execute(self, sql, params=()):
                pattern = r'\b(' + '|'.join(cls.tables) + r'|fk_membership_\w+|uq_grower_membership)\b'
                sql = re.sub(pattern, lambda m: cls.prefix + m.group(), sql)
                return self.raw.execute(sql, params)
            def __getattr__(self, name):
                return getattr(self.raw, name)
        class Connection:
            def __init__(self):
                self.raw = get_conn()
            def cursor(self, *args, **kwargs):
                return Cursor(self.raw.cursor(*args, **kwargs))
            def __getattr__(self, name):
                return getattr(self.raw, name)
        return Connection()

    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.patches):
            p.stop()
        main._access_schema_ready = cls.old_ready
        main.app.config['TESTING'] = cls.old_testing
        assert re.fullmatch(r'invtest_[0-9a-f]{16}_', cls.prefix)
        conn=get_conn(); cur=conn.cursor()
        for table in cls.tables:
            cur.execute('DROP TABLE IF EXISTS `' + cls.prefix + table + '`')
        cur.close(); conn.close()

    def sql(self, sql, params=()):
        conn=self.connect(); cur=conn.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            rows=cur.fetchall() if cur.with_rows else []
            conn.commit()
            return rows
        finally:
            cur.close(); conn.close()

    def setUp(self):
        conn=self.connect(); cur=conn.cursor()
        cur.execute('SET FOREIGN_KEY_CHECKS=0')
        for table in ('user_invitations','user_emails','grower_memberships','users','Grower'):
            cur.execute('DROP TABLE IF EXISTS ' + table)
        cur.execute('SET FOREIGN_KEY_CHECKS=1')
        cur.execute('CREATE TABLE Grower (Grower_ID BIGINT UNSIGNED PRIMARY KEY, Grower_Name VARCHAR(120))')
        cur.execute("""CREATE TABLE users (id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,username VARCHAR(80) UNIQUE,
            full_name VARCHAR(120),password_hash VARCHAR(255),role VARCHAR(10),is_active INT DEFAULT 1)""")
        schema=(Path(__file__).resolve().parents[1]/'migrations/001_grower_access.sql').read_text()
        schema='\n'.join(line for line in schema.splitlines() if not line.lstrip().startswith('--'))
        cur.execute(schema.split(';')[0])
        inv.ensure_schema(cur)
        cur.execute("INSERT INTO Grower VALUES (1,'Test Farm'),(2,'Other Farm')")
        hashed=bcrypt.hashpw(b'password123',bcrypt.gensalt(rounds=4)).decode()
        cur.execute("INSERT INTO users (id,username,password_hash,role) VALUES (1,'admin',%s,'admin'),(2,'existing',%s,'user')",(hashed,hashed))
        cur.execute("INSERT INTO grower_memberships (user_id,Grower_ID,role,status) VALUES (1,1,'admin','active'),(2,2,'viewer','active')")
        conn.commit();cur.close();conn.close()
        self.mocks[-1].reset_mock();self.mocks[-1].side_effect=None
        self.client=main.app.test_client()
        with self.client.session_transaction() as sess:
            sess['_user_id']='1';sess['_fresh']=True;sess['access_csrf']='test-csrf'
            sess['password_version']=main.password_version(hashed)

    def invite(self, **kwargs):
        data=dict(email='person@unl.edu',role='viewer',csrf_token='test-csrf',action='invite')
        data.update(kwargs)
        return self.client.post('/users/invitations',data=data)

    def token(self):
        return self.mocks[-1].call_args.args[-1]

    def accept(self, token, **kwargs):
        data=dict(mode='new',username='newuser',password='password123',confirm_password='password123',csrf_token='test-csrf')
        data.update(kwargs)
        return self.client.post('/invitations/'+token,data=data)

    def test_create_accept_and_replay(self):
        self.assertEqual(self.invite().status_code,302)
        token=self.token()
        row=self.sql('SELECT * FROM user_invitations')[0]
        self.assertEqual(row['token_hash'],hashlib.sha256(token.encode()).hexdigest())
        response=self.client.get('/invitations/'+token)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers['Referrer-Policy'],'no-referrer')
        self.assertEqual(self.sql('SELECT status FROM user_invitations')[0]['status'],'pending')
        self.assertIn(b'grower access is active',self.accept(token).data)
        self.assertEqual(self.accept(token).status_code,410)
        self.assertEqual(self.sql('SELECT email FROM user_emails')[0]['email'],'person@unl.edu')

    def test_domain_roles_and_csrf(self):
        for email in ('x@gmail.com','x@unl.edu.evil.com','x\n@unl.edu','x@huskers.unl.edu'):
            self.invite(email=email)
        self.mocks[-1].assert_not_called()
        self.assertEqual(self.invite(role='owner').status_code,400)
        self.assertEqual(self.invite(csrf_token='bad').status_code,400)
        self.invite()
        self.assertEqual(self.accept(self.token(),csrf_token='bad').status_code,400)

    def test_admin_and_grower_boundaries(self):
        self.invite(); row=self.sql('SELECT id FROM user_invitations')[0]
        with self.client.session_transaction() as sess:
            sess['_user_id']='2'
        self.assertEqual(self.invite().status_code,403)
        self.sql("UPDATE grower_memberships SET role='admin' WHERE user_id=2")
        self.assertEqual(self.invite(action='revoke',invitation_id=row['id']).status_code,404)
        self.assertEqual(self.sql('SELECT status FROM user_invitations')[0]['status'],'pending')

    def test_resend_expiration_revocation(self):
        self.invite(); old=self.token(); row=self.sql('SELECT id FROM user_invitations')[0]
        self.sql('UPDATE user_invitations SET created_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.invite(action='resend',invitation_id=row['id']); new=self.token()
        self.assertNotEqual(old,new)
        self.assertEqual(self.accept(old).status_code,410)
        self.invite(action='revoke',invitation_id=row['id'])
        self.assertEqual(self.accept(new).status_code,410)
        self.sql('UPDATE user_invitations SET created_at=UTC_TIMESTAMP()-INTERVAL 2 MINUTE')
        self.invite(action='resend',invitation_id=row['id'])
        self.sql('UPDATE user_invitations SET expires_at=UTC_TIMESTAMP()-INTERVAL 1 DAY')
        self.assertEqual(self.accept(self.token()).status_code,410)

    def test_delivery_failure_and_duplicate(self):
        self.mocks[-1].side_effect=OSError('test failure')
        self.invite()
        self.assertEqual(self.sql('SELECT status FROM user_invitations')[0]['status'],'failed')
        self.assertEqual(self.accept(self.token()).status_code,410)
        self.mocks[-1].side_effect=None
        self.invite();self.invite()
        self.assertEqual(self.mocks[-1].call_count,2)

    def test_existing_account_and_wrong_email(self):
        self.invite(role='editor')
        self.assertIn(b'Invalid username',self.accept(self.token(),mode='existing',username='existing',password='wrongpassword').data)
        self.assertIn(b'grower access is active',self.accept(self.token(),mode='existing',username='existing').data)
        rows=self.sql('SELECT role FROM grower_memberships WHERE user_id=2 AND Grower_ID=1')
        self.assertEqual(rows[0]['role'],'editor')
        self.assertEqual(self.client.post('/login',data=dict(username='existing',password='password123')).status_code,302)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['active_grower_id'],1)

    def test_email_conflict_rolls_back_new_user(self):
        self.sql("INSERT INTO user_emails VALUES (2,'person@unl.edu',UTC_TIMESTAMP())")
        self.invite()
        self.assertIn(b'different account',self.accept(self.token()).data)
        self.assertFalse(self.sql("SELECT id FROM users WHERE username='newuser'"))
        self.assertEqual(self.sql('SELECT status FROM user_invitations')[0]['status'],'pending')

    def test_password_attempt_limit(self):
        self.invite()
        for _ in range(10):
            self.accept(self.token(),mode='existing',username='existing',password='wrongpassword')
        self.assertEqual(self.accept(self.token(),mode='existing',username='existing').status_code,410)

    def test_user_access_page_and_existing_actions_csrf(self):
        self.invite()
        response=self.client.get('/users')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'person@unl.edu',response.data)
        self.assertEqual(self.client.post('/users',data=dict(action='approve_admin',membership_id=2)).status_code,400)

    def test_existing_active_role_is_preserved(self):
        self.invite(role='viewer')
        self.sql("INSERT INTO grower_memberships (user_id,Grower_ID,role,status) VALUES (2,1,'admin','active')")
        self.accept(self.token(),mode='existing',username='existing')
        self.assertEqual(self.sql('SELECT role FROM grower_memberships WHERE user_id=2 AND Grower_ID=1')[0]['role'],'admin')

    def test_email_message_and_config_failure(self):
        # Exercise MIME creation and the sendmail arguments without invoking mail.
        self.patches[-1].stop()
        try:
            with main.app.test_request_context('/'), patch.object(inv.subprocess,'run') as run:
                inv.send_invitation('person@unl.edu','Test Farm','viewer','test-token')
                self.assertEqual(run.call_args.args[0], ['/sbin/sendmail','-i','-f','approved@unl.edu','--','person@unl.edu'])
                self.assertIn(b'https://example.invalid/invitations/test-token',run.call_args.kwargs['input'])
                self.assertNotIn('shell',run.call_args.kwargs)
        finally:
            self.mocks[-1] = self.patches[-1].start()
        with patch.object(inv,'mail_config',side_effect=ValueError('Email is not configured')):
            self.invite()
            self.assertFalse(self.sql('SELECT id FROM user_invitations'))


if __name__ == '__main__':
    unittest.main()
