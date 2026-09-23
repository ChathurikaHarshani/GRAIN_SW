"""Apply cart/invitation schema updates, preserving existing cart settings.

Run with imports stopped: python scripts/deploy_invitations.py --apply
Add --configure-email on the UNL server to set missing email configuration.
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from db import get_conn
from dotenv import dotenv_values, set_key
from invitations import ensure_schema, mail_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', required=True)
    parser.add_argument('--configure-email', action='store_true')
    args = parser.parse_args()
    if args.configure_email:
        if not Path('/sbin/sendmail').is_file():
            raise SystemExit('Run email configuration on the UNL server with /sbin/sendmail installed.')
        defaults = {
            'GMS_PUBLIC_URL': 'https://lagad-grainms-prod.unl.edu',
            'GMS_SENDMAIL_PATH': '/sbin/sendmail',
            'GMS_MAIL_FROM': 'lagad-grainms@lagad-grainms-prod.unl.edu',
        }
        env_path = ROOT / '.env'
        configured = dotenv_values(env_path)
        for key, value in defaults.items():
            if not os.getenv(key) and not configured.get(key):
                set_key(str(env_path), key, value)
                os.environ[key] = value
        mail_config()
        print('Email configuration validated. No email was sent.')

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT * FROM Cart')
        before = cur.fetchall()
        folder = ROOT / 'backups'
        folder.mkdir(exist_ok=True)
        backup = folder / ('cart-before-invitations-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json')
        with backup.open('x', encoding='utf-8') as output:
            json.dump(before, output, default=str, indent=2)
        backup.chmod(0o600)
        print('Cart recovery snapshot:', backup)
        cur.execute('SHOW COLUMNS FROM Cart')
        columns = {row['Field'] for row in cur.fetchall()}
        new_load_cell = 'Load_Cell' not in columns
        for column, definition in (('Load_Cell', 'VARCHAR(100) NULL'), ('Load_Cell_Date', 'DATE NULL')):
            if column not in columns:
                cur.execute(f'ALTER TABLE Cart ADD COLUMN {column} {definition}')
        # Backfill only when adding Load_Cell for the first time; reruns preserve edits.
        if new_load_cell:
            migration = (ROOT / 'migrations/006_cart_load_cell.sql').read_text()
            cur.execute(migration[migration.index('UPDATE Cart c'):])
            conn.commit()
        ensure_schema(cur)
        conn.commit()
        cur.execute('SELECT * FROM Cart')
        after = {row['Cart_ID']: row for row in cur.fetchall()}
        assert len(after) == len(before), 'Cart count changed during deployment.'
        assert all(all(after[row['Cart_ID']][key] == value for key, value in row.items()) for row in before), 'Existing cart values changed.'
        print('Schema ready. Existing cart values preserved. No harvest records were modified.')
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    main()
