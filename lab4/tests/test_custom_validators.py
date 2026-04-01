import unittest
import sys
import os

# Добавляем путь к папке app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from custom_validators import number_length, NumberLength
from registration import app


class TestForm(FlaskForm):
    # Тестирование функционального валидатора
    phone_func = StringField('Phone', validators=[
        number_length(min=10, max=10, message='Телефон должен быть 10 цифр')
    ])
    
    # Тестирование классового валидатора
    index_class = StringField('Index', validators=[
        NumberLength(min=5, max=7, message='Индекс должен быть от 5 до 7 цифр')
    ])
    
    # Тестирование с разными параметрами
    short_field = StringField('Short', validators=[
        number_length(min=2, max=3)
    ])
    
    long_field = StringField('Long', validators=[
        NumberLength(min=4, max=6)
    ])


class TestCustomValidators(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    # ========== ТЕСТЫ ДЛЯ ФУНКЦИОНАЛЬНОГО ВАЛИДАТОРА ==========
    
    def test_func_validator_valid(self):
        """Тест: функциональный валидатор - валидное значение"""
        with app.test_request_context():
            form = TestForm(phone_func='1234567890')
            self.assertTrue(form.validate())
    
    def test_func_validator_too_short(self):
        """Тест: функциональный валидатор - слишком короткое"""
        with app.test_request_context():
            form = TestForm(phone_func='12345')
            self.assertFalse(form.validate())
            self.assertIn('phone_func', form.errors)
            self.assertIn('Телефон должен быть 10 цифр', form.errors['phone_func'])
    
    def test_func_validator_too_long(self):
        """Тест: функциональный валидатор - слишком длинное"""
        with app.test_request_context():
            form = TestForm(phone_func='123456789012')
            self.assertFalse(form.validate())
            self.assertIn('phone_func', form.errors)
    
    def test_func_validator_with_custom_message(self):
        """Тест: функциональный валидатор - кастомное сообщение"""
        with app.test_request_context():
            form = TestForm(phone_func='123')
            self.assertFalse(form.validate())
            self.assertEqual(form.errors['phone_func'][0], 'Телефон должен быть 10 цифр')
    
    def test_func_validator_empty(self):
        """Тест: функциональный валидатор - пустое значение (необязательное)"""
        with app.test_request_context():
            form = TestForm(phone_func='')
            self.assertTrue(form.validate())
    
    # ========== ТЕСТЫ ДЛЯ КЛАССОВОГО ВАЛИДАТОРА ==========
    
    def test_class_validator_valid(self):
        """Тест: классовый валидатор - валидное значение"""
        with app.test_request_context():
            form = TestForm(index_class='123456')
            self.assertTrue(form.validate())
    
    def test_class_validator_too_short(self):
        """Тест: классовый валидатор - слишком короткое"""
        with app.test_request_context():
            form = TestForm(index_class='123')
            self.assertFalse(form.validate())
            self.assertIn('index_class', form.errors)
    
    def test_class_validator_too_long(self):
        """Тест: классовый валидатор - слишком длинное"""
        with app.test_request_context():
            form = TestForm(index_class='12345678')
            self.assertFalse(form.validate())
            self.assertIn('index_class', form.errors)
    
    def test_class_validator_custom_message(self):
        """Тест: классовый валидатор - кастомное сообщение"""
        with app.test_request_context():
            form = TestForm(index_class='12')
            self.assertFalse(form.validate())
            self.assertEqual(form.errors['index_class'][0], 'Индекс должен быть от 5 до 7 цифр')
    
    def test_class_validator_empty(self):
        """Тест: классовый валидатор - пустое значение"""
        with app.test_request_context():
            form = TestForm(index_class='')
            self.assertTrue(form.validate())
    
    # ========== ТЕСТЫ С РАЗНЫМИ ПАРАМЕТРАМИ ==========
    
    def test_func_with_min_2_max_3_valid(self):
        """Тест: валидатор с min=2, max=3 - валидное значение"""
        with app.test_request_context():
            form = TestForm(short_field='123')
            self.assertTrue(form.validate())
    
    def test_func_with_min_2_max_3_too_short(self):
        """Тест: валидатор с min=2, max=3 - слишком короткое"""
        with app.test_request_context():
            form = TestForm(short_field='1')
            self.assertFalse(form.validate())
            self.assertIn('short_field', form.errors)
    
    def test_func_with_min_2_max_3_too_long(self):
        """Тест: валидатор с min=2, max=3 - слишком длинное"""
        with app.test_request_context():
            form = TestForm(short_field='1234')
            self.assertFalse(form.validate())
            self.assertIn('short_field', form.errors)
    
    def test_class_with_min_4_max_6_valid(self):
        """Тест: валидатор с min=4, max=6 - валидное значение"""
        with app.test_request_context():
            form = TestForm(long_field='12345')
            self.assertTrue(form.validate())
    
    def test_class_with_min_4_max_6_too_short(self):
        """Тест: валидатор с min=4, max=6 - слишком короткое"""
        with app.test_request_context():
            form = TestForm(long_field='123')
            self.assertFalse(form.validate())
            self.assertIn('long_field', form.errors)
    
    def test_class_with_min_4_max_6_too_long(self):
        """Тест: валидатор с min=4, max=6 - слишком длинное"""
        with app.test_request_context():
            form = TestForm(long_field='1234567')
            self.assertFalse(form.validate())
            self.assertIn('long_field', form.errors)
    
    # ========== ТЕСТЫ С РАЗНЫМИ ТИПАМИ ДАННЫХ ==========
    
    def test_with_negative_number(self):
        """Тест: отрицательное число (длина без знака минус)"""
        with app.test_request_context():
            # Создаем форму с IntegerField для проверки отрицательных чисел
            class NegativeTestForm(FlaskForm):
                number = IntegerField('Number', validators=[
                    NumberLength(min=2, max=3)
                ])
            
            form = NegativeTestForm(number=-123)
            self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main(verbosity=2)