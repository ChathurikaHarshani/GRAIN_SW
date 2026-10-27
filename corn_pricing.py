"""Crop-year corn pricing from recorded cash quotes (no calendar guessing)."""
import calendar
from decimal import Decimal, ROUND_HALF_UP


def price(value, hmc=False):
    value = Decimal(str(value)) + Decimal('0.04')
    return (value * (Decimal('0.95') if hmc else 1)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)


def build_report(records, year):
    months = []
    for offset in range(12):
        month = (offset + 9) % 12 + 1
        calendar_year = year if month >= 10 else year + 1
        quotes = {}
        invalid = False
        for record in records:
            if int(record['Year']) != calendar_year or int(record['Month']) != month:
                continue
            try:
                day = int(str(record['Day']).strip())
                value = Decimal(str(record['Market_Price']))
                if not 1 <= day <= calendar.monthrange(calendar_year, month)[1] or not value.is_finite() or value < 0:
                    raise ValueError
            except (ValueError, TypeError, ArithmeticError):
                invalid = True
                continue
            if day in quotes:
                invalid = True
            quotes[day] = value
        days = sorted(quotes)[:5]
        values = [quotes[day] for day in days]
        complete = len(values) == 5 and not invalid
        average = sum(values) / 5 if complete else None
        months.append(dict(month=calendar.month_name[month], year=calendar_year,
                           days=values + [None] * (5 - len(values)),
                           corn=price(average) if complete else None,
                           hmc=price(average, True) if complete else None,
                           status='Review entries' if invalid else ('Complete' if complete else ('Pending' if not values else f'{len(values)}/5 days'))))
    complete = [row for row in months if row['corn'] is not None]
    averages = {key: (sum(row[key] for row in complete) / len(complete)).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP) if complete else None for key in ('corn', 'hmc')}
    return months, averages, len(complete)
