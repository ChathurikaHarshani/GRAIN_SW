"""Grower-scoped correction review and explicit return to Raven ownership."""
import json
from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from db import get_conn
from invitations import check_csrf
from harvest_corrections import (PROTECTED, conflicts, corrected_bushels, encode,
                                 read_state, save_source)

bp = Blueprint('corrections', __name__)
LABELS = dict(Load_Num='Load number', Field_ID='Field / crop year',
              Harvest_Date='Date', Crop_ID='Crop', MC='Moisture',
              StorLoc_ID='Storage', Truck_ID='Truck')


@bp.route('/harvest/corrections', methods=['GET', 'POST'])
@login_required
def review():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            if not current_user.can_edit:
                abort(403)
            check_csrf()
            attribute = request.form.get('attribute')
            if attribute not in PROTECTED:
                abort(400)
            cur.execute('''SELECT h.* FROM Harvest h
                JOIN Field f ON f.Field_ID=h.Field_ID
                JOIN Department d ON d.Dpt_ID=f.Dpt_ID
                WHERE h.Harvest_ID=%s AND d.Grower_ID=%s FOR UPDATE''',
                (request.form.get('harvest_id'), current_user.grower_id))
            current = cur.fetchone()
            if not current:
                abort(404)
            source, overrides = read_state(cur, current['Harvest_ID'])
            if attribute not in overrides or attribute not in source:
                abort(400, description='No Raven value is available for this correction.')
            action = request.form.get('action')
            if action == 'raven':
                value = source[attribute]
                if attribute in ('Field_ID', 'StorLoc_ID') and value is not None:
                    if attribute == 'Field_ID':
                        cur.execute('''SELECT f.Dpt_ID FROM Field f JOIN Department d
                            ON d.Dpt_ID=f.Dpt_ID WHERE f.Field_ID=%s AND d.Grower_ID=%s''',
                            (value, current_user.grower_id))
                    else:
                        cur.execute('SELECT StorLoc_ID FROM Storage_Location '
                                    'WHERE StorLoc_ID=%s AND Grower_ID=%s',
                                    (value, current_user.grower_id))
                    target = cur.fetchone()
                    if not target:
                        abort(400, description='The Raven assignment is no longer available.')
                    if attribute == 'Field_ID':
                        cur.execute('UPDATE Harvest SET Dpt_ID=%s WHERE Harvest_ID=%s',
                                    (target['Dpt_ID'], current['Harvest_ID']))
                # Attribute is constrained to PROTECTED above, never arbitrary SQL.
                cur.execute('UPDATE Harvest SET ' + attribute + '=%s WHERE Harvest_ID=%s',
                            (value, current['Harvest_ID']))
                cur.execute('''INSERT INTO Harvest_Correction_History
                    (Harvest_ID, User_ID, Attribute_Name, Previous_Value, Corrected_Value)
                    VALUES (%s,%s,%s,%s,%s)''',
                    (current['Harvest_ID'], int(current_user.id), attribute,
                     encode(current[attribute]), encode(value)))
                current[attribute] = value
                overrides.remove(attribute)
                if attribute in ('MC', 'Crop_ID'):
                    cur.execute('SELECT Weight_PerBushel, Base_MC FROM Crop WHERE Crop_ID=%s',
                                (current['Crop_ID'],))
                    crop = cur.fetchone()
                    if not crop:
                        abort(400)
                    cur.execute('UPDATE Harvest SET Bushels=%s WHERE Harvest_ID=%s',
                                (corrected_bushels(current, crop['Weight_PerBushel'],
                                                   crop['Base_MC']), current['Harvest_ID']))
                save_source(cur, current['Harvest_ID'], source, overrides)
            elif action != 'manual':
                abort(400)
            conn.commit()
            return redirect(url_for('corrections.review'))

        cur.execute('''SELECT h.*, s.Source_Values, s.Override_Fields
            FROM Harvest h JOIN Harvest_Raven_State s ON s.Harvest_ID=h.Harvest_ID
            JOIN Field f ON f.Field_ID=h.Field_ID
            JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            WHERE d.Grower_ID=%s ORDER BY h.Harvest_Date DESC, h.Harvest_ID DESC''',
            (current_user.grower_id,))
        loads = cur.fetchall()
        cur.execute('''SELECT f.Field_ID, f.Field_Name, f.Crop_Year FROM Field f
            JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s''',
            (current_user.grower_id,))
        labels = {'Field_ID': {str(f['Field_ID']): '{} ({})'.format(f['Field_Name'], f['Crop_Year'])
                               for f in cur.fetchall()}}
        cur.execute('SELECT Crop_ID, Crop_Name FROM Crop')
        labels['Crop_ID'] = {str(c['Crop_ID']): c['Crop_Name'] for c in cur.fetchall()}
        cur.execute('SELECT StorLoc_ID, Bin_Code, Bin_Name FROM Storage_Location WHERE Grower_ID=%s',
                    (current_user.grower_id,))
        labels['StorLoc_ID'] = {str(s['StorLoc_ID']): s['Bin_Code'] or s['Bin_Name']
                                for s in cur.fetchall()}
        def display(attribute, value):
            if value is None:
                return '(blank)'
            return labels.get(attribute, {}).get(str(value), value)
        rows = []
        for load in loads:
            source = json.loads(load['Source_Values'])
            overrides = set(json.loads(load['Override_Fields']))
            differences = conflicts(source, load, overrides)
            for attribute in sorted(overrides):
                rows.append(dict(harvest_id=load['Harvest_ID'], load=load['Load_Num'],
                                 date=load['Harvest_Date'], attribute=attribute,
                                 label=LABELS[attribute], manual=display(attribute, load.get(attribute)),
                                 raven=display(attribute, source.get(attribute)), available=attribute in source,
                                 conflict=attribute in differences))
        cur.execute('''SELECT c.*, u.username FROM Harvest_Correction_History c
            JOIN Harvest h ON h.Harvest_ID=c.Harvest_ID
            JOIN Field f ON f.Field_ID=h.Field_ID
            JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            LEFT JOIN users u ON u.id=c.User_ID WHERE d.Grower_ID=%s
            ORDER BY c.Change_ID DESC LIMIT 200''', (current_user.grower_id,))
        history = cur.fetchall()
        for item in history:
            item['Previous_Value'] = display(item['Attribute_Name'], json.loads(item['Previous_Value']))
            item['Corrected_Value'] = display(item['Attribute_Name'], json.loads(item['Corrected_Value']))
            item['Attribute_Name'] = LABELS.get(item['Attribute_Name'], item['Attribute_Name'])
        return render_template('harvest_corrections.html', rows=rows, history=history)
    finally:
        conn.rollback()
        cur.close()
        conn.close()
