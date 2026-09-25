"""Add and verify recovery email without granting grower access."""
import hashlib
import secrets
import re
import subprocess
from datetime import datetime,timedelta
from email.message import EmailMessage
from pathlib import Path
import bcrypt
from flask import Blueprint, request, render_template, url_for, current_app
from flask_login import current_user, login_required
from mysql.connector import IntegrityError
from db import get_conn
from invitations import check_csrf, unl_email, mail_config

bp=Blueprint('email_verification',__name__)

def ensure_schema(cur):
    cur.execute((Path(__file__).parent/'migrations/010_email_verification.sql').read_text())

def send_verification(email,token):
    sender,base,executable=mail_config()
    message=EmailMessage()
    message['From'],message['To']=sender,email
    message['Subject']='Verify your GMS email'
    message.set_content('Verify the email for your GMS account within 24 hours:\n\n'
        +base+url_for('email_verification.verify',token=token)
        +'\n\nYou must sign in to the account that requested verification. If you did not request this, ignore this email.')
    subprocess.run([executable,'-i','-f',sender,'--',email],input=message.as_bytes(),
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=20)

def issue_verification(user_id,email):
    email=unl_email(email)
    conn=get_conn();cur=conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id FROM users WHERE id=%s AND is_active=1 FOR UPDATE',(user_id,))
        if not cur.fetchone():
            raise ValueError('Account unavailable.')
        cur.execute('SELECT * FROM user_emails WHERE user_id=%s OR email=%s',(user_id,email))
        if cur.fetchall():
            raise ValueError('This account or email is already verified. Contact your administrator if it needs updating.')
        cur.execute('SELECT * FROM email_verifications WHERE user_id=%s FOR UPDATE',(user_id,))
        old=cur.fetchone();now=datetime.utcnow()
        within=old and now-old['window_started']<timedelta(hours=1)
        if old and (now-old['requested_at']<timedelta(minutes=1) or (within and old['request_count']>=5)):
            raise ValueError('Please wait before requesting another verification email. Limit: one per minute and five per hour.')
        token=secrets.token_urlsafe(32);digest=hashlib.sha256(token.encode()).hexdigest()
        cur.execute("""INSERT INTO email_verifications
            (user_id,email,token_hash,expires_at,requested_at,window_started,request_count)
            VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE email=VALUES(email),token_hash=VALUES(token_hash),
            expires_at=VALUES(expires_at),requested_at=VALUES(requested_at),window_started=VALUES(window_started),request_count=VALUES(request_count)""",
            (user_id,email,digest,now+timedelta(hours=24),now,old['window_started'] if within else now,old['request_count']+1 if within else 1))
        conn.commit()
        try:
            send_verification(email,token)
        except (ValueError,OSError,subprocess.SubprocessError):
            cur.execute('UPDATE email_verifications SET token_hash=NULL WHERE token_hash=%s',(digest,));conn.commit()
            current_app.logger.warning('Email verification submission failed; check mail configuration.')
            return 'Your email is saved but verification email could not be sent. Contact your administrator or try resending later.'
        return 'Verification email submitted. Open the link within 24 hours, sign in to this account, then confirm verification.'
    finally:
        conn.rollback();cur.close();conn.close()

@bp.route('/account/email',methods=['GET','POST'])
@login_required
def account():
    notice=None;error=None
    if request.method=='POST':
        check_csrf()
        password=request.form.get('password','')
        if not password or len(password.encode())>72 or not bcrypt.checkpw(password.encode(),current_user.password_hash.encode()):
            error='Enter your current password to add or verify an email.'
        else:
            try:
                notice=issue_verification(int(current_user.id),request.form.get('email',''))
            except ValueError as exc:
                error=str(exc)
    conn=get_conn();cur=conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT email FROM user_emails WHERE user_id=%s',(current_user.id,));verified=cur.fetchone()
        cur.execute('SELECT email FROM email_verifications WHERE user_id=%s',(current_user.id,));pending=cur.fetchone()
    finally:
        cur.close();conn.close()
    return render_template('account_email.html',verified=verified,pending=pending,notice=notice,error=error)

@bp.route('/verify-email/<token>',methods=['GET','POST'])
def verify(token):
    invalid='This verification link is expired, already used, or unavailable. Request another from Add/Verify Email.'
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}',token):
        return render_template('verify_email.html',error=invalid),410
    if not current_user.is_authenticated:
        return render_template('verify_email.html',signin=True)
    if request.method=='POST':
        check_csrf()
    conn=get_conn();cur=conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id FROM users WHERE id=%s AND is_active=1 FOR UPDATE',(current_user.id,));cur.fetchone()
        cur.execute('SELECT * FROM email_verifications WHERE user_id=%s AND token_hash=%s FOR UPDATE',
            (current_user.id,hashlib.sha256(token.encode()).hexdigest()))
        row=cur.fetchone()
        if not row or row['expires_at']<=datetime.utcnow():
            return render_template('verify_email.html',error=invalid),410
        if request.method=='POST':
            cur.execute('INSERT INTO user_emails (user_id,email,verified_at) VALUES (%s,%s,UTC_TIMESTAMP())',(current_user.id,row['email']))
            cur.execute('UPDATE email_verifications SET token_hash=NULL WHERE user_id=%s',(current_user.id,))
            conn.commit()
            return render_template('verify_email.html',complete=True)
        return render_template('verify_email.html',email=row['email'])
    except IntegrityError:
        conn.rollback()
        return render_template('verify_email.html',error='This account or email is already verified. Contact your administrator.'),409
    finally:
        conn.rollback();cur.close();conn.close()

@bp.after_request
def private_response(response):
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['Cache-Control']='no-store'
    return response
