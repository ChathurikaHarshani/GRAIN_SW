import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from jinja2 import ChoiceLoader, DictLoader, FileSystemLoader
import correction_views


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test-only'
        self.app.jinja_loader = ChoiceLoader([
            DictLoader({'base.html': '{% block content %}{% endblock %}'}),
            FileSystemLoader('templates'),
        ])
        self.app.add_url_rule('/harvest', endpoint='harvest_query', view_func=lambda: '')
        self.app.register_blueprint(correction_views.bp)
        self.user = SimpleNamespace(can_edit=True, grower_id=1, id=2, is_authenticated=True)
        self.calls = []
        self.cur = SimpleNamespace(execute=lambda sql, params=(): self.calls.append((sql, params)),
                                   fetchone=lambda: None, fetchall=lambda: [], close=lambda: None)
        self.conn = SimpleNamespace(cursor=lambda **kwargs: self.cur,
                                    commit=lambda: self.calls.append(('COMMIT', ())),
                                    rollback=lambda: None, close=lambda: None)
        self.addCleanup(patch.stopall)
        patch.object(correction_views, 'get_conn', return_value=self.conn).start()
        patch.object(correction_views, 'current_user', self.user).start()
        self.app.jinja_env.globals.update(current_user=self.user, access_csrf_token=lambda: 'token')

    def invoke(self, method='GET', data=None):
        with self.app.test_request_context('/harvest/corrections', method=method, data=data):
            from flask import session
            session['access_csrf'] = 'token'
            return correction_views.review.__wrapped__()

    def test_empty_review_renders_and_queries_only_current_grower(self):
        html = self.invoke()
        self.assertIn('No tracked manual corrections', html)
        scoped = [(sql, params) for sql, params in self.calls if 'd.Grower_ID=%s' in sql]
        self.assertEqual(len(scoped), 3)
        self.assertTrue(all(params == (1,) for _, params in scoped))

    def test_viewer_cannot_reset(self):
        self.user.can_edit = False
        from werkzeug.exceptions import Forbidden
        with self.assertRaises(Forbidden):
            self.invoke('POST', {'attribute': 'MC', 'action': 'raven', 'csrf_token': 'token'})
        self.assertEqual(self.calls, [])

    def test_csrf_and_attribute_are_required(self):
        from werkzeug.exceptions import BadRequest
        for data in ({'attribute': 'MC'},
                     {'attribute': 'Gross_Weight', 'csrf_token': 'token'}):
            with self.assertRaises(BadRequest):
                self.invoke('POST', data)
        self.assertEqual(self.calls, [])

    def test_reset_uses_latest_raven_and_removes_only_selected_override(self):
        self.cur.fetchone = lambda: dict(Harvest_ID=12, MC=16, Crop_ID=1,
                                        Gross_Weight=56000, Tare_Weight=0)
        patch.object(correction_views, 'read_state', return_value=(
            {'MC': 20}, {'MC', 'Truck_ID'})).start()
        # A crop lookup is the second fetchone after the load lock.
        from unittest.mock import Mock
        self.cur.fetchone = Mock(side_effect=[dict(Harvest_ID=12, MC=16, Crop_ID=1,
                                                  Gross_Weight=56000, Tare_Weight=0),
                                              dict(Weight_PerBushel=56, Base_MC=15.5)])
        save = patch.object(correction_views, 'save_source').start()
        result = self.invoke('POST', dict(attribute='MC', action='raven',
                                         harvest_id='12', csrf_token='token'))
        self.assertEqual(result.status_code, 302)
        save.assert_called_once_with(self.cur, 12, {'MC': 20}, {'Truck_ID'})
        self.assertIn(('UPDATE Harvest SET MC=%s WHERE Harvest_ID=%s', (20, 12)), self.calls)
        self.assertIn(('UPDATE Harvest SET Bushels=%s WHERE Harvest_ID=%s', (946.75, 12)), self.calls)
        self.assertIn(('COMMIT', ()), self.calls)


if __name__ == '__main__':
    unittest.main()
