"""Apply Vehicles schema and the requested historical cleanup; safe to rerun.

Run after a full database backup and with imports stopped.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from db import get_conn
from import_grc import get_or_create_vehicle, find_storage_location


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', required=True)
    parser.parse_args()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    class Adapter:
        def cursor(self):
            return conn.cursor(dictionary=True)

    try:
        # MySQL DDL commits independently; each step checks the live schema.
        cur.execute((ROOT / 'migrations/003_vehicles.sql').read_text())
        cur.execute("SHOW COLUMNS FROM Vehicles LIKE 'Load_Cell_Date'")
        if not cur.fetchone():
            cur.execute((ROOT / 'migrations/005_vehicle_load_cell_date.sql').read_text())
        cur.execute("SHOW COLUMNS FROM Harvest LIKE 'Cart_ID'")
        if cur.fetchone()['Null'] != 'YES':
            cur.execute((ROOT / 'migrations/004_optional_harvest_cart.sql').read_text())
        conn.commit()
        conn.start_transaction()
        snapshot = {}
        for table in ('Cart', 'Vehicles', 'Harvest', 'Storage_Location'):
            cur.execute(f'SELECT * FROM `{table}` FOR UPDATE')
            snapshot[table] = cur.fetchall()
        folder = ROOT / 'backups'
        folder.mkdir(exist_ok=True, mode=0o700)
        path = folder / ('vehicle-deployment-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.json')
        with path.open('x', encoding='utf-8') as output:
            json.dump(snapshot, output, default=str, indent=2)
        path.chmod(0o600)
        print(f'Data recovery snapshot: {path}', flush=True)
        vehicle_codes = {'05A', '186A', '214A', '460A', '461A', 'A05'}
        obsolete_codes = vehicle_codes | {'55:88', '58:95'}
        for cart in snapshot['Cart']:
            if cart['Cart_Code'] in vehicle_codes:
                cur.execute('SELECT Vehicle_ID FROM Vehicles WHERE Grower_ID=%s AND Vehicle_Code=%s',
                            (cart['Grower_ID'], cart['Cart_Code']))
                if not cur.fetchone():
                    cur.execute('INSERT INTO Vehicles (Grower_ID,Vehicle_Code,Vehicle_Name) VALUES (%s,%s,%s)',
                                (cart['Grower_ID'], cart['Cart_Code'], cart['Cart_Name']))
        cur.execute('''SELECT h.*,d.Grower_ID AS Mapping_Grower_ID FROM Harvest h
            JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            ORDER BY h.Harvest_Date,h.Harvest_ID''')
        loads = cur.fetchall()
        linked = 0
        for row in loads:
            get_or_create_vehicle(Adapter(), row['Truck_ID'], row['Mapping_Grower_ID'],
                                  row['Load_Cell'], row['Harvest_Date'])
            if row['StorLoc_ID'] is None:
                sid = find_storage_location(Adapter(), row['Destination'], row['Mapping_Grower_ID'])
                if sid is not None:
                    cur.execute('UPDATE Harvest SET StorLoc_ID=%s WHERE Harvest_ID=%s AND StorLoc_ID IS NULL',
                                (sid, row['Harvest_ID']))
                    linked += cur.rowcount
        deleted = unlinked = 0
        for cart in snapshot['Cart']:
            if cart['Cart_Code'] in obsolete_codes:
                cur.execute('UPDATE Harvest SET Cart_ID=NULL WHERE Cart_ID=%s', (cart['Cart_ID'],))
                unlinked += cur.rowcount
                cur.execute('DELETE FROM Cart WHERE Cart_ID=%s', (cart['Cart_ID'],))
                deleted += cur.rowcount
        cur.execute('SELECT * FROM Harvest')
        after = {r['Harvest_ID']: r for r in cur.fetchall()}
        assert len(after) == len(snapshot['Harvest']), 'Harvest count changed'
        for old in snapshot['Harvest']:
            for key in ('Gross_Weight', 'Tare_Weight', 'MC', 'Bushels', 'Truck_ID',
                        'Load_Cell', 'Field_ID', 'Crop_ID', 'Destination'):
                assert old[key] == after[old['Harvest_ID']][key], f'Unexpected change: {key}'
        conn.commit()
        print(f'SUCCESS: {linked} storage links filled; {deleted} obsolete carts removed; '
              f'{unlinked} cart links cleared. All harvest loads preserved.')
    except Exception:
        conn.rollback()
        print('Data transaction rolled back. Additive schema changes may remain.')
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    main()
