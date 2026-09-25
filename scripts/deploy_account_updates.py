"""Apply additive migrations 008-010 with GMS/imports stopped. Sends no email."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from db import get_conn
from invitations import mail_config, ensure_schema as invitation_schema
from password_reset import ensure_schema as reset_schema
from email_verification import ensure_schema as verification_schema


def apply_schema(conn):
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SHOW COLUMNS FROM Delivery')
        if 'Crop_Year' not in {r['Field'] for r in cur.fetchall()}:
            cur.execute('ALTER TABLE Delivery ADD COLUMN Crop_Year SMALLINT UNSIGNED NULL')
        cur.execute('SHOW INDEX FROM Delivery')
        if 'idx_delivery_grower_crop_year' not in {r['Key_name'] for r in cur.fetchall()}:
            cur.execute('ALTER TABLE Delivery ADD INDEX idx_delivery_grower_crop_year (Grower_ID,Crop_Year)')
        invitation_schema(cur)
        reset_schema(cur)
        verification_schema(cur)
        conn.commit()
        cur.execute('SELECT COUNT(*) AS n FROM Delivery WHERE Crop_Year IS NULL')
        print('Deliveries awaiting crop-year assignment:', cur.fetchone()['n'])
        print('Migrations 008-010 ready. Existing data preserved; no crop years guessed.')
    finally:
        cur.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', required=True)
    parser.add_argument('--check-mail', action='store_true', help='Validate production mail settings without sending email')
    args = parser.parse_args()
    if args.check_mail:
        mail_config()
        print('Mail configuration present. No email sent.')
    conn = get_conn()
    try:
        apply_schema(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
