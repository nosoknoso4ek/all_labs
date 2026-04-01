import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app


class TestUptimeEndpoint(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_uptime_returns_200(self):
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 200)
    
    def test_uptime_contains_current_uptime(self):
        response = self.client.get('/uptime')
        text = response.get_data(as_text=True)
        self.assertIn('Current uptime is', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)