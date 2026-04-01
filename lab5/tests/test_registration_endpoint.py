import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app


class TestRegistrationEndpoint(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
    
    def test_get_registration_page(self):
        response = self.client.get('/registration')
        self.assertEqual(response.status_code, 200)
    
    def test_root_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
    
    def test_post_valid_data(self):
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Адрес',
            'index': '123456'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main(verbosity=2)