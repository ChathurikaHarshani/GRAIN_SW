import unittest
import app as main


class YieldRenderTest(unittest.TestCase):
    def test_section_with_field_renders_highlight_data_on_body_row(self):
        row = dict(Field_Name='3070', Acres=67, Total_Bushels=10319.4,
                   Yield_bu_per_acre=154.02, Irr_Type='Irrigated', Hybrid_Variety='DK59-82',
                   Avg_MC=13.77, Total_WetBushels=10319.4, Total_DryBushels=10319.4)
        section = dict(crop_name='Corn', crop_year=2026, rows=[row],
                       total_acres=67, total_bushels=10319.4, avg_yield=154.02,
                       type_summary=[], hybrid_summary=[], notes=[], silage_rows=[])
        with main.app.test_request_context('/yield'):
            result = main.render_template('yield.html', yield_sections=[section],
                active_filters=dict(crop_year='2026', grower='', department='', field='', crop=''),
                filter_options=dict(crop_years=[2026], growers=[], departments=[], fields=[], crops=[]))
        self.assertIn('data-acres="67"', result)
        field_table = result.split('yield-field-table', 1)[1]
        head, body = field_table.split('<tbody>', 1)
        self.assertNotIn('data-yield-field', head)
        self.assertIn('data-yield-field', body)


if __name__ == '__main__':
    unittest.main()
