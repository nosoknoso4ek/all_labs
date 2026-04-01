import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app


class TestPsEndpoint(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_ps_no_arguments(self):
        response = self.client.get('/ps')
        self.assertEqual(response.status_code, 400)
    
    def test_ps_with_arguments(self):
        response = self.client.get('/ps?arg=a&arg=u&arg=x')
        self.assertEqual(response.status_code, 200)
    
    def test_ps_returns_pre_tag(self):
        response = self.client.get('/ps?arg=a')
        text = response.get_data(as_text=True)
        self.assertIn('<pre>', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)