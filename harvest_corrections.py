"""Raven snapshots and per-attribute corrections, using the caller's transaction.

Apply migration 011 before use. Field_ID identifies both field and crop year;
Dpt_ID follows the effective field. Source identity stays on Harvest unchanged
when users edit display values.
"""
import json
from decimal import Decimal

PROTECTED = ('Load_Num', 'Field_ID', 'Harvest_Date', 'Crop_ID', 'MC',
             'StorLoc_ID', 'Truck_ID')


def canonical(value):
    if value is None or value == '':
        return None
    if isinstance(value, (float, Decimal)):
        return format(Decimal(str(value)).normalize(), 'f')
    return str(value)


def encode(value):
    return json.dumps(value, default=str, sort_keys=True)


def read_state(cur, harvest_id):
    cur.execute('SELECT Source_Values, Override_Fields FROM Harvest_Raven_State '
                'WHERE Harvest_ID=%s FOR UPDATE', (harvest_id,))
    row = cur.fetchone()
    if not row:
        return {}, set()
    if isinstance(row, dict):
        row = (row['Source_Values'], row['Override_Fields'])
    return json.loads(row[0]), set(json.loads(row[1]))


def save_source(cur, harvest_id, source, overrides):
    cur.execute('''INSERT INTO Harvest_Raven_State
        (Harvest_ID, Source_Values, Override_Fields) VALUES (%s,%s,%s)
        ON DUPLICATE KEY UPDATE Source_Values=VALUES(Source_Values),
        Override_Fields=VALUES(Override_Fields)''',
        (harvest_id, encode(source), encode(sorted(overrides))))


def record_edit(cur, harvest_id, user_id, before, after):
    """Mark only changed attributes; an intentional NULL is an override too."""
    source, overrides = read_state(cur, harvest_id)
    for name in PROTECTED:
        if canonical(before.get(name)) != canonical(after.get(name)):
            overrides.add(name)
            cur.execute('''INSERT INTO Harvest_Correction_History
                (Harvest_ID, User_ID, Attribute_Name, Previous_Value, Corrected_Value)
                VALUES (%s,%s,%s,%s,%s)''',
                (harvest_id, user_id, name, encode(before.get(name)), encode(after.get(name))))
    save_source(cur, harvest_id, source, overrides)


def merge_source(source, current, overrides):
    result = dict(source)
    # Missing Raven values historically leave these effective attributes intact.
    for name in ('MC', 'StorLoc_ID', 'Truck_ID'):
        if result.get(name) is None:
            result[name] = current.get(name)
    for name in overrides:
        if name in PROTECTED:
            result[name] = current[name]
    if 'Field_ID' in overrides:
        result['Dpt_ID'] = current['Dpt_ID']
    return result


def conflicts(source, current, overrides):
    def comparable(name, value):
        if name == 'MC' and value is not None:
            return Decimal(str(value))
        return canonical(value)
    return {name: {'raven': source[name], 'manual': current.get(name)}
            for name in overrides if name in source
            and comparable(name, source[name]) != comparable(name, current.get(name))}


def corrected_bushels(values, weight_per_bushel, base_mc):
    gross = values.get('Gross_Weight')
    if gross is None or not weight_per_bushel:
        return None
    wet = (float(gross) - float(values.get('Tare_Weight') or 0)) / float(weight_per_bushel)
    mc = values.get('MC')
    if mc is not None and base_mc is not None and float(mc) > float(base_mc):
        wet *= (100 - float(mc)) / (100 - float(base_mc))
    return round(wet, 2)
