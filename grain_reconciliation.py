"""Department settlement totals using crop-year average prices."""
from decimal import Decimal, ROUND_HALF_UP
from corn_pricing import build_report


def crop_group(code, name):
    code, name = (code or '').strip().upper(), (name or '').strip().lower()
    if code in ('C', 'HMC') or name in ('corn', 'hmc', 'high moisture corn'):
        return 'corn'
    if code in ('M', 'MILO') or name in ('milo', 'sorghum', 'grain sorghum'):
        return 'milo'


def settlement(deliveries, quotes, year):
    averages, counts = {}, {}
    for group in ('corn', 'milo'):
        selected = [q for q in quotes if crop_group(q['Crop_Code'], q['Crop_Name']) == group
                    and (q['Crop_Code'] or '').strip().upper() != 'HMC'
                    and (q['Crop_Name'] or '').strip().lower() not in ('hmc', 'high moisture corn')]
        _, avg, count = build_report(selected, year)
        averages[group], counts[group] = avg['corn'], count
    def blank(label):
        return dict(department=label, corn=dict(bushels=Decimal(0), billed=Decimal(0), due=Decimal(0)),
                    milo=dict(bushels=Decimal(0), billed=Decimal(0), due=Decimal(0)), total_due=Decimal(0))
    departments = {}
    for delivery in deliveries:
        group = crop_group(delivery['Crop_Code'], delivery['Crop_Name'])
        if not group:
            continue
        key = delivery['DelLoc_ID']
        row = departments.setdefault(key, blank(delivery['department'] or 'Unassigned destination'))
        item = row[group]
        bu = Decimal(str(delivery['bushels'] or 0))
        billed = delivery['billed']
        item['bushels'] += bu
        if billed is None:
            item['billed'] = None
        elif item['billed'] is not None:
            item['billed'] += Decimal(str(billed))
        rate = averages[group]
        hmc = (delivery['Crop_Code'] or '').strip().upper() == 'HMC' or (delivery['Crop_Name'] or '').strip().lower() in ('hmc', 'high moisture corn')
        if rate is None or billed is None:
            item['due'] = None
        elif item['due'] is not None:
            adjusted = rate * (Decimal('0.95') if hmc else 1)
            item['due'] += bu * adjusted - Decimal(str(billed))
    rows = sorted(departments.values(), key=lambda r: r['department'])
    total = blank('TOTAL')
    for row in rows:
        for group in ('corn', 'milo'):
            for field in ('bushels', 'billed', 'due'):
                value = row[group][field]
                if field != 'bushels' and value is not None:
                    value = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    row[group][field] = value
                if value is None:
                    total[group][field] = None
                elif total[group][field] is not None:
                    total[group][field] += value
        row['total_due'] = None if any(row[g]['due'] is None for g in ('corn', 'milo')) else row['corn']['due'] + row['milo']['due']
    total['total_due'] = None if any(total[g]['due'] is None for g in ('corn', 'milo')) else total['corn']['due'] + total['milo']['due']
    return dict(rows=rows, total=total, averages=averages, counts=counts, year=year)
