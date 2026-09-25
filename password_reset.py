"""Email recovery for verified Viewer/Editor accounts only."""
import hashlib
import secrets
import re
import subprocess
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
import bcrypt
from flask import Blueprint, request, render_template, url_for, session
from flask_login import logout_user
from db import get_conn
from invitations import check_csrf, unl_email, mail_config

bp = Blueprint('password_reset', __name__)
NOTICE = 'If this email belongs to an eligible account, a password reset link will be sent. Check your inbox and junk folder.'

def ensure_schema(cur):
    cur.execute((Path(__file__).parent / 'migrations/009_password_resets.sql').read_text())

def password_version(password_hash):
    return hashlib.sha256(password_hash.encode()).hexdigest()

def eligible(cur, user):
    if not user or not user['is_active'] or user['role'] == 'admin':
        return False
    cur.execute('SELECT role,status FROM grower_memberships WHERE user_id=%s FOR UPDATE', (user['id'],))
    memberships = cur.fetchall()
    return not any(m['role'] == 'admin' for m in memberships) and any(
        m['role'] in ('viewer','editor') and m['status'] == 'active' for m in memberships)

def send_reset(email, token):
    sender, base, executable = mail_config()
    message = EmailMessage()
    message['From'], message['To'] = sender, email
    message['Subject'] = 'Reset your GMS password'
    message.set_content('Use this link within 30 minutes to reset your GMS password:\n\n'
        + base + url_for('password_reset.reset', token=token)
        + '\n\nIf you did not request this, ignore this email. Your password has not changed.')
    subprocess.run([executable,'-i','-f',sender,'--',email],input=message.as_bytes(),
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=20)

@bp.route('/forgot-password', methods=['GET','POST'])
def forgot():
    if request.method == 'GET':
        return render_template('password_reset.html', mode='request')
    check_csrf()
    try:
        email = unl_email(request.form.get('email',''))
    except ValueError:
        return render_template('password_reset.html', mode='request', notice=NOTICE)
    conn=get_conn(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT u.* FROM users u JOIN user_emails e ON e.user_id=u.id WHERE e.email=%s AND e.verified_at IS NOT NULL FOR UPDATE', (email,))
        user=cur.fetchone()
        if eligible(cur,user):
            now=datetime.utcnow()
            cur.execute('SELECT * FROM password_resets WHERE user_id=%s FOR UPDATE',(user['id'],))
            previous=cur.fetchone()
            within_hour=previous and now-previous['window_started'] < timedelta(hours=1)
            limited=previous and (now-previous['requested_at'] < timedelta(minutes=1) or (within_hour and previous['request_count'] >= 5))
            if not limited:
                token=secrets.token_urlsafe(32)
                digest=hashlib.sha256(token.encode()).hexdigest()
                cur.execute("""INSERT INTO password_resets
                    (user_id,token_hash,password_version,expires_at,requested_at,window_started,request_count)
                    VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
                    token_hash=VALUES(token_hash),password_version=VALUES(password_version),expires_at=VALUES(expires_at),
                    requested_at=VALUES(requested_at),window_started=VALUES(window_started),request_count=VALUES(request_count)""",
                    (user['id'],digest,password_version(user['password_hash']),now+timedelta(minutes=30),now,
                     previous['window_started'] if within_hour else now,previous['request_count']+1 if within_hour else 1))
                conn.commit()
                try:
                    send_reset(email,token)
                except (ValueError,OSError,subprocess.SubprocessError):
                    cur.execute('UPDATE password_resets SET token_hash=NULL WHERE token_hash=%s',(digest,))
                    conn.commit()
                    from flask import current_app
                    current_app.logger.warning('Password reset email submission failed; check mail configuration.')
    finally:
        conn.rollback();cur.close();conn.close()
    return render_template('password_reset.html', mode='request', notice=NOTICE)

@bp.route('/reset-password/<token>', methods=['GET','POST'])
def reset(token):
    invalid='This reset link is invalid, expired, or unavailable for this account. Request a new link or contact your administrator.'
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}',token):
        return render_template('password_reset.html',mode='invalid',error=invalid),410
    if request.method == 'POST':
        check_csrf()
    digest=hashlib.sha256(token.encode()).hexdigest()
    conn=get_conn();cur=conn.cursor(dictionary=True)
    try:
        # Lock the account first, in the same order as requests.
        cur.execute('SELECT user_id FROM password_resets WHERE token_hash=%s',(digest,))
        reference=cur.fetchone()
        if not reference:
            return render_template('password_reset.html',mode='invalid',error=invalid),410
        cur.execute('SELECT * FROM users WHERE id=%s FOR UPDATE',(reference['user_id'],))
        user=cur.fetchone()
        allowed=eligible(cur,user)
        cur.execute('SELECT * FROM password_resets WHERE user_id=%s FOR UPDATE',(reference['user_id'],))
        row=cur.fetchone()
        if not allowed or row['token_hash'] != digest or row['expires_at'] <= datetime.utcnow() or row['password_version'] != password_version(user['password_hash']):
            return render_template('password_reset.html',mode='invalid',error=invalid),410
        if request.method == 'POST':
            password=request.form.get('password','')
            if len(password)<8 or len(password.encode())>72 or password != request.form.get('confirm_password'):
                return render_template('password_reset.html',mode='reset',error='Passwords must match and contain at least eight characters (maximum 72 bytes).'),400
            hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            cur.execute('UPDATE users SET password_hash=%s WHERE id=%s',(hashed,user['id']))
            cur.execute('UPDATE password_resets SET token_hash=NULL WHERE user_id=%s',(user['id'],))
            conn.commit()
            logout_user()
            session.clear()
            return render_template('password_reset.html',mode='complete')
        return render_template('password_reset.html',mode='reset')
    finally:
        conn.rollback();cur.close();conn.close()

@bp.after_request
def private_response(response):
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['Cache-Control']='no-store'
    return response
