import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app, RegistrationForm


class TestRegistrationForm(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_valid_form_data(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@example.com',
                phone='1234567890',
                name='Иван Петров',
                address='г. Москва, ул. Ленина, 1',
                index='123456',
                comment='Тест'
            )
            self.assertTrue(form.validate())
    
    def test_empty_email(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='',
                phone='1234567890',
                name='Иван',
                address='Адрес',
                index='123456'
            )
            self.assertFalse(form.validate())
            self.assertIn('email', form.errors)
    
    def test_empty_phone(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@test.com',
                phone='',
                name='Иван',
                address='Адрес',
                index='123456'
            )
            self.assertFalse(form.validate())
            self.assertIn('phone', form.errors)
    
    def test_empty_name(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@test.com',
                phone='1234567890',
                name='',
                address='Адрес',
                index='123456'
            )
            self.assertFalse(form.validate())
            self.assertIn('name', form.errors)
    
    def test_empty_address(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@test.com',
                phone='1234567890',
                name='Иван',
                address='',
                index='123456'
            )
            self.assertFalse(form.validate())
            self.assertIn('address', form.errors)
    
    def test_empty_index(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@test.com',
                phone='1234567890',
                name='Иван',
                address='Адрес',
                index=''
            )
            self.assertFalse(form.validate())
            self.assertIn('index', form.errors)
    
    def test_comment_optional(self):
        with app.test_request_context():
            form = RegistrationForm(
                email='test@test.com',
                phone='1234567890',
                name='Иван',
                address='Адрес',
                index='123456',
                comment=''
            )
            self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main(verbosity=2)