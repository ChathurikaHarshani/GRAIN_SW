"""Preview or apply missing storage links using the Raven destination mapping."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from db import get_conn
from import_grc import destination_to_bin_code, normalize_storage_lookup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cur.execute('SELECT StorLoc_ID, Grower_ID, Bin_Code, Bin_Name FROM Storage_Location')
        storage = cur.fetchall()
        cur.execute('''SELECT h.*, d.Grower_ID AS Mapping_Grower_ID
            FROM Harvest h JOIN Field f ON f.Field_ID=h.Field_ID
            JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            WHERE h.StorLoc_ID IS NULL FOR UPDATE''')
        rows = cur.fetchall()
        changes, unresolved = [], Counter()
        for row in rows:
            code = destination_to_bin_code(row['Destination'])
            key = normalize_storage_lookup(code)
            matches = {s['StorLoc_ID'] for s in storage
                       if s['Grower_ID'] == row['Mapping_Grower_ID'] and key
                       and key in {normalize_storage_lookup(s['Bin_Code']),
                                   normalize_storage_lookup(s['Bin_Name'])}}
            if len(matches) == 1:
                changes.append({'before': row, 'storage_id': next(iter(matches))})
            else:
                unresolved[row['Destination'] or '(missing destination)'] += 1
        print(f'Missing links: {len(rows)}; clear matches: {len(changes)}')
        print('Unresolved:', dict(unresolved))
        if args.apply and changes:
            folder = ROOT / 'backups'
            folder.mkdir(exist_ok=True)
            path = folder / ('harvest-storage-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json')
            with path.open('x', encoding='utf-8') as backup:
                json.dump(changes, backup, default=str, indent=2)
            for change in changes:
                cur.execute('''UPDATE Harvest SET StorLoc_ID=%s
                    WHERE Harvest_ID=%s AND StorLoc_ID IS NULL''',
                    (change['storage_id'], change['before']['Harvest_ID']))
                if cur.rowcount != 1:
                    raise RuntimeError('Record changed; rolling back.')
            conn.commit()
            print(f'Updated {len(changes)} storage links. Backup: {path}')
        else:
            conn.rollback()
            print('No data changed. Use --apply to apply clear matches.')
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    main()
