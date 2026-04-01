import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from flask_wtf import FlaskForm
from wtforms import StringField
from custom_validators import number_length, NumberLength
from registration import app


class TestForm(FlaskForm):
    phone_func = StringField('Phone', validators=[
        number_length(min=10, max=10, message='Телефон должен быть 10 цифр')
    ])
    index_class = StringField('Index', validators=[
        NumberLength(min=5, max=7, message='Индекс должен быть от 5 до 7 цифр')
    ])


class TestCustomValidators(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_func_validator_valid(self):
        with app.test_request_context():
            form = TestForm(phone_func='1234567890')
            self.assertTrue(form.validate())
    
    def test_func_validator_too_short(self):
        with app.test_request_context():
            form = TestForm(phone_func='12345')
            self.assertFalse(form.validate())
    
    def test_class_validator_valid(self):
        with app.test_request_context():
            form = TestForm(index_class='123456')
            self.assertTrue(form.validate())
    
    def test_class_validator_too_short(self):
        with app.test_request_context():
            form = TestForm(index_class='123')
            self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main(verbosity=2)