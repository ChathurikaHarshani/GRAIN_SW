"""UNL invitations: hashed one-use tokens and local Postfix submission."""
import hashlib
import os
import re
import secrets
import subprocess
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlsplit

import bcrypt
from flask import (Blueprint, abort, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required
from mysql.connector import IntegrityError
from db import get_conn

bp = Blueprint('invitations', __name__)


def ensure_schema(cur):
    sql = (Path(__file__).parent / 'migrations/007_user_invitations.sql').read_text()
    for statement in sql.split(';'):
        if statement.strip():
            cur.execute(statement)


def csrf_token():
    if 'access_csrf' not in session:
        session['access_csrf'] = secrets.token_urlsafe(32)
    return session['access_csrf']


def check_csrf():
    if not secrets.compare_digest(session.get('access_csrf', ''), request.form.get('csrf_token', '')) or not session.get('access_csrf'):
        abort(400, description='This form expired. Reload the page and try again.')


def unl_email(value):
    value = value.strip().lower()
    if len(value) > 254 or not re.fullmatch(r"[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@unl\.edu", value):
        raise ValueError('Enter an @unl.edu email address.')
    local = value.split('@')[0]
    if len(local) > 64 or local.startswith('.') or local.endswith('.') or '..' in local:
        raise ValueError('Enter a valid @unl.edu email address.')
    return value


def mail_config():
    sender = os.getenv('GMS_MAIL_FROM', '').strip().lower()
    local, separator, domain = sender.rpartition('@')
    if not separator or len(sender) > 254 or domain not in ('unl.edu', 'lagad-grainms-prod.unl.edu'):
        raise ValueError('Configure GMS_MAIL_FROM with a UNL or GMS server sender address.')
    unl_email(local + '@unl.edu')
    base = os.getenv('GMS_PUBLIC_URL', '').rstrip('/')
    parsed = urlsplit(base)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
        raise ValueError('Configure GMS_PUBLIC_URL with the HTTPS app URL.')
    executable = os.getenv('GMS_SENDMAIL_PATH', '/sbin/sendmail')
    if not Path(executable).is_file():
        raise ValueError('The local email service is not configured.')
    return sender, base, executable


def email_ready():
    try:
        mail_config()
        return True
    except ValueError:
        return False


def send_invitation(email, grower, role, token):
    sender, base, executable = mail_config()
    message = EmailMessage()
    message['From'] = sender
    message['To'] = email
    message['Subject'] = 'Invitation to GMS'
    link = base + url_for('invitations.accept', token=token)
    message.set_content(f'You have been invited to {grower} in GMS as {role.title()}.\n\n'
                        f'Accept your invitation within seven days:\n{link}\n\n'
                        'If you did not expect this invitation, you can ignore it.\n')
    subprocess.run([executable, '-i', '-f', sender, '--', email],
                   input=message.as_bytes(), stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=True, timeout=20)


@bp.post('/users/invitations')
@login_required
def invite():
    if not current_user.is_admin:
        abort(403)
    check_csrf()
    action = request.form.get('action', 'invite')
    if action not in ('invite', 'resend', 'revoke'):
        abort(400)
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        # Serialize invitation changes for this grower, including duplicate sends.
        cur.execute('SELECT Grower_ID FROM Grower WHERE Grower_ID=%s FOR UPDATE', (current_user.grower_id,))
        cur.fetchone()
        if action == 'invite':
            email = unl_email(request.form.get('email', ''))
            role = request.form.get('role', 'viewer')
            if role not in ('viewer', 'editor', 'admin'):
                abort(400)
            cur.execute('SELECT * FROM user_invitations WHERE Grower_ID=%s AND email=%s FOR UPDATE',
                        (current_user.grower_id, email))
            previous = cur.fetchone()
            if previous and previous['status'] in ('pending', 'sending') and previous['expires_at'] > datetime.utcnow():
                raise ValueError('An invitation already exists. Use Resend or Revoke.')
        else:
            cur.execute('SELECT * FROM user_invitations WHERE id=%s AND Grower_ID=%s FOR UPDATE',
                        (request.form.get('invitation_id', type=int), current_user.grower_id))
            previous = cur.fetchone()
            if not previous:
                abort(404)
            if previous['status'] == 'accepted':
                raise ValueError('This invitation was accepted. Manage the user’s access below.')
            if action == 'revoke':
                cur.execute("UPDATE user_invitations SET status='revoked' WHERE id=%s", (previous['id'],))
                conn.commit()
                flash('Invitation revoked.', 'success')
                return redirect(url_for('manage_users'))
            email, role = previous['email'], previous['role']
            if datetime.utcnow() - previous['created_at'] < timedelta(minutes=1):
                raise ValueError('Wait one minute before resending this invitation.')
        mail_config()
        cur.execute("""SELECT gm.id FROM user_emails e JOIN grower_memberships gm ON gm.user_id=e.user_id
            WHERE e.email=%s AND gm.Grower_ID=%s AND gm.status='active'""", (email, current_user.grower_id))
        if cur.fetchone():
            raise ValueError('This email already has active access. Manage the user’s role below.')
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode()).hexdigest()
        cur.execute("""INSERT INTO user_invitations
            (Grower_ID,email,role,invited_by,token_hash,status,expires_at)
            VALUES (%s,%s,%s,%s,%s,'sending',%s)
            ON DUPLICATE KEY UPDATE role=VALUES(role),invited_by=VALUES(invited_by),
            token_hash=VALUES(token_hash),status='sending',expires_at=VALUES(expires_at),
            created_at=UTC_TIMESTAMP(),accepted_at=NULL,failed_attempts=0""",
            (current_user.grower_id, email, role, current_user.id, digest, datetime.utcnow()+timedelta(days=7)))
        conn.commit()
        try:
            send_invitation(email, current_user.grower_name, role, token)
        except (OSError, subprocess.SubprocessError):
            cur.execute("UPDATE user_invitations SET status='failed' WHERE token_hash=%s AND status='sending'", (digest,))
            conn.commit()
            flash('Email submission failed. Check the server email configuration, then resend.', 'danger')
        else:
            cur.execute("UPDATE user_invitations SET status='pending' WHERE token_hash=%s AND status='sending'", (digest,))
            conn.commit()
            flash('Invitation submitted to the email service. Delivery may take a few minutes.', 'success')
    except ValueError as exc:
        conn.rollback()
        flash(str(exc), 'warning')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('manage_users'))


@bp.route('/invitations/<token>', methods=['GET', 'POST'])
def accept(token):
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}', token):
        abort(404)
    if request.method == 'POST':
        check_csrf()
    digest = hashlib.sha256(token.encode()).hexdigest()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    error = None
    try:
        cur.execute("""SELECT i.*,g.Grower_Name FROM user_invitations i
            JOIN Grower g ON g.Grower_ID=i.Grower_ID WHERE token_hash=%s FOR UPDATE""", (digest,))
        invitation = cur.fetchone()
        if not invitation or invitation['status'] != 'pending' or invitation['expires_at'] <= datetime.utcnow() or invitation['failed_attempts'] >= 10:
            return render_template('invitation_accept.html', invitation=None, error='This invitation is expired, revoked, or already used. Ask your administrator for a new invitation.'), 410
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            mode = request.form.get('mode')
            if not username or len(username) > 80 or not 1 <= len(password.encode()) <= 72:
                raise ValueError('Enter a username (up to 80 characters) and a password of 8–72 bytes.')
            cur.execute('SELECT * FROM users WHERE username=%s FOR UPDATE', (username,))
            user = cur.fetchone()
            if mode == 'existing':
                if not user or not user['is_active'] or not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
                    cur.execute('UPDATE user_invitations SET failed_attempts=failed_attempts+1 WHERE id=%s', (invitation['id'],))
                    conn.commit()
                    raise ValueError('Invalid username or password. After ten failed attempts, request a new invitation.')
                user_id = user['id']
            elif mode == 'new':
                if len(password) < 8:
                    raise ValueError('New passwords must contain at least eight characters.')
                if user:
                    raise ValueError('Username already exists. Choose another or select Existing account.')
                if password != request.form.get('confirm_password'):
                    raise ValueError('Passwords do not match.')
                cur.execute("INSERT INTO users (username,password_hash,role,is_active) VALUES (%s,%s,'user',1)",
                            (username,bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()))
                user_id = cur.lastrowid
            else:
                abort(400)
            cur.execute('SELECT * FROM user_emails WHERE user_id=%s OR email=%s FOR UPDATE', (user_id,invitation['email']))
            identities = cur.fetchall()
            if any(r['user_id'] != user_id or r['email'] != invitation['email'] for r in identities):
                raise ValueError('This invitation email belongs to a different account. Use the matching account or contact your administrator.')
            if not identities:
                cur.execute('INSERT INTO user_emails (user_id,email,verified_at) VALUES (%s,%s,UTC_TIMESTAMP())', (user_id,invitation['email']))
            # Do not let an old invitation change an already-active member's role.
            cur.execute("""INSERT INTO grower_memberships (user_id,Grower_ID,role,status,approved_at,approved_by)
                VALUES (%s,%s,%s,'active',UTC_TIMESTAMP(),%s)
                ON DUPLICATE KEY UPDATE
                role=IF(status='active',role,VALUES(role)),
                approved_at=IF(status='active',approved_at,VALUES(approved_at)),
                approved_by=IF(status='active',approved_by,VALUES(approved_by)),status='active'""",
                (user_id,invitation['Grower_ID'],invitation['role'],invitation['invited_by']))
            cur.execute("UPDATE user_invitations SET status='accepted',accepted_at=UTC_TIMESTAMP() WHERE id=%s", (invitation['id'],))
            conn.commit()
            # Sign in through the usual login page after acceptance, retaining the selected grower.
            from flask_login import logout_user
            logout_user()
            session['active_grower_id'] = invitation['Grower_ID']
            return render_template('invitation_accept.html', invitation=None, accepted=True)
    except ValueError as exc:
        conn.rollback()
        error = str(exc)
    except IntegrityError:
        conn.rollback()
        error = 'That username or email was just registered. Try Existing account or contact your administrator.'
    finally:
        conn.rollback()
        cur.close()
        conn.close()
    return render_template('invitation_accept.html', invitation=invitation, error=error)


@bp.after_request
def private_invitation_response(response):
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Cache-Control'] = 'no-store'
    return response
