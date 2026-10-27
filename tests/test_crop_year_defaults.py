"""Crop-year defaults preserve explicit all-year and historical requests."""
import ast
from datetime import date
from pathlib import Path
from unittest.mock import patch
import unittest

import app as main


class CropYearDefaultsTest(unittest.TestCase):
    def test_omitted_explicit_all_and_previous_year(self):
        for query, expected in [('', str(date.today().year)),
                                ('?crop_year=', ''), ('?crop_year=2025', '2025')]:
            with self.subTest(query=query), main.app.test_request_context('/yield' + query):
                self.assertEqual(main.crop_year_filter(), expected)

    def test_year_rollover(self):
        with patch.object(main, 'date') as clock, main.app.test_request_context('/inventory'):
            clock.today.return_value = date(2027, 1, 1)
            self.assertEqual(main.crop_year_filter(), '2027')

    def test_all_crop_year_filter_routes_use_shared_default(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        names = set()
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and any(
                    isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                    and call.func.id == 'crop_year_filter' for call in ast.walk(node)):
                names.add(node.name)
        self.assertEqual(names, {'list_fields', 'harvest_query', 'harvest_summary',
                                 'yield_report', 'yield_export', 'inventory_report', 'inventory_export'})

    def test_filter_templates_compile(self):
        for name in ('fields.html', 'harvest_query.html', 'yield.html', 'inventory.html'):
            with self.subTest(name=name):
                main.app.jinja_env.get_template(name)


if __name__ == '__main__':
    unittest.main()
