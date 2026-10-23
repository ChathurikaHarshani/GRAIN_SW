"""Correction rules run without Flask, Raven credentials, or a live database."""
import datetime
from decimal import Decimal
import json
import unittest
import ast
from pathlib import Path

from harvest_corrections import (
    canonical, conflicts, corrected_bushels, merge_source, record_edit,
)


class Cursor:
    def __init__(self, overrides=()):
        self.overrides = overrides
        self.calls = []

    def execute(self, sql, params):
        self.calls.append((sql, params))

    def fetchone(self):
        return ('{}', json.dumps(list(self.overrides)))


class CorrectionTests(unittest.TestCase):
    def test_production_import_keeps_identity_corrections_and_blank_storage(self):
        from harvest_corrections import read_state, save_source
        tree = ast.parse(Path('import_grc.py').read_text(encoding='utf-8'))
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                        and n.name == 'insert_harvest_load')
        function.returns = None
        for arg in function.args.args:
            arg.annotation = None
        existing = dict(Harvest_ID=12, Field_ID=99, Dpt_ID=88, Load_Num='corrected',
                        Harvest_Date=datetime.date(2025, 9, 1), Crop_ID=2, MC=16,
                        StorLoc_ID=None, Truck_ID=None, Gross_Weight=56000, Tare_Weight=0)

        class ImportCursor(Cursor):
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def fetchone(self):
                sql = self.calls[-1][0]
                if 'FROM Harvest\n' in sql:
                    return existing
                if 'FROM Crop' in sql:
                    return dict(Weight_PerBushel=56, Base_MC=15.5)
                return ('{}', json.dumps(['Field_ID', 'Load_Num', 'Harvest_Date',
                                         'MC', 'StorLoc_ID', 'Truck_ID']))

        cur = ImportCursor()
        namespace = dict(read_state=read_state, save_source=save_source,
                         merge_source=merge_source, corrected_bushels=corrected_bushels,
                         safe_date=lambda x: datetime.date.fromisoformat(x) if x else None,
                         safe_moisture=lambda x: float(x) if x else None,
                         safe_decimal=lambda x: float(x) if x else None,
                         build_external_load_key=lambda **kwargs: 'original-raven-key')
        for name in ('normalize_field_name', 'normalize_crop_name', 'normalize_cart_code',
                     'normalize_destination', 'normalize_variety'):
            namespace[name] = lambda x: x or ''
        for name in ('get_or_create_grower', 'get_or_create_department', 'get_or_create_field',
                     'get_or_create_crop', 'get_or_create_cart', 'get_or_create_vehicle',
                     'find_storage_location'):
            namespace[name] = lambda *args: 1
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'import_grc.py', 'exec'), namespace)
        from types import SimpleNamespace
        run = namespace['insert_harvest_load']
        for _ in range(2):
            self.assertEqual(run(SimpleNamespace(cursor=lambda: cur),
                dict(grower='G', farm='D', field='Original', crop='Corn'),
                dict(cart_id='C1', date='2026-10-01', moisture=20,
                     weight=56000, load_num='7', truck='A', dest='Bin1'),
                1, 'sample.grc', 1), 'UPDATED')
            update = next(params for sql, params in reversed(cur.calls)
                          if 'UPDATE Harvest' in sql)
            self.assertEqual(update[1:8], (99, 1, 88, None, 'corrected',
                                          datetime.date(2025, 9, 1), 16))
            self.assertIsNone(update[15])
            self.assertEqual(update[22], 'original-raven-key')
            self.assertEqual(update[10], 994.08)

    def test_reimport_preserves_only_corrected_attributes_and_department(self):
        source = dict(Field_ID=1, Dpt_ID=10, MC=19, Truck_ID='A', StorLoc_ID=4,
                      Load_Num='7', Harvest_Date='2026-10-01', Crop_ID=2)
        current = dict(source, Field_ID=3, Dpt_ID=20, MC=16)
        result = merge_source(source, current, {'Field_ID'})
        self.assertEqual((result['Field_ID'], result['Dpt_ID']), (3, 20))
        self.assertEqual(result['MC'], 19)
        self.assertEqual(source['Field_ID'], 1)

    def test_intentionally_cleared_values_survive_reimport(self):
        result = merge_source(dict(Truck_ID='A', StorLoc_ID=9, MC=18),
                              dict(Truck_ID=None, StorLoc_ID=None, MC=None),
                              {'Truck_ID', 'StorLoc_ID', 'MC'})
        self.assertEqual(result, dict(Truck_ID=None, StorLoc_ID=None, MC=None))

    def test_missing_source_values_keep_previous_unedited_values(self):
        self.assertEqual(merge_source(dict(MC=None, Truck_ID=None, StorLoc_ID=None),
                                     dict(MC=15, Truck_ID='A', StorLoc_ID=2), set()),
                         dict(MC=15, Truck_ID='A', StorLoc_ID=2))

    def test_save_marks_only_real_changes_and_keeps_existing_overrides(self):
        cur = Cursor({'Field_ID'})
        before = dict(Load_Num='1', Field_ID=2, Harvest_Date=datetime.date(2026, 10, 1),
                      Crop_ID=3, MC=Decimal('15.00'), StorLoc_ID=4, Truck_ID='A')
        after = dict(before, Harvest_Date='2026-10-01', MC=15.0, Truck_ID=None)
        record_edit(cur, 10, 20, before, after)
        history = [params for sql, params in cur.calls if 'Correction_History' in sql]
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][:3], (10, 20, 'Truck_ID'))
        self.assertEqual(json.loads(cur.calls[-1][1][2]), ['Field_ID', 'Truck_ID'])

    def test_conflicts_include_blank_and_ignore_decimal_format(self):
        self.assertEqual(conflicts({'MC': '15.00', 'Truck_ID': 'A'},
                                   {'MC': Decimal('15.00'), 'Truck_ID': None}, {'Truck_ID'}),
                         {'Truck_ID': {'raven': 'A', 'manual': None}})
        self.assertEqual(canonical(Decimal('15.00')), canonical(15.0))
        self.assertEqual(conflicts({'MC': '15.00'}, {'MC': 15.0}, {'MC'}), {})

    def test_bushels_use_corrected_moisture_and_crop_factor(self):
        values = dict(Gross_Weight=57000, Tare_Weight=1000, MC=20)
        self.assertEqual(corrected_bushels(values, 56, 15.5), 946.75)
        self.assertEqual(corrected_bushels(dict(values, MC=15), 56, 15.5), 1000)
        self.assertIsNone(corrected_bushels(values, None, 15.5))


if __name__ == '__main__':
    unittest.main()
