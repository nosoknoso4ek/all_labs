import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app
from code_executor import execute_code_safely


class TestCodeExecutor(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
    
    def test_execute_simple_code(self):
        """Тест: выполнение простого кода"""
        output, error = execute_code_safely('print("Hello")', timeout=5)
        self.assertIsNone(error)
        self.assertIn('Hello', output)
    
    def test_execute_with_timeout(self):
        """Тест: превышение тайм-аута"""
        output, error = execute_code_safely('import time; time.sleep(3)', timeout=1)
        self.assertIsNotNone(error)
        self.assertIn('не уложилось', error)
    
    def test_execute_syntax_error(self):
        """Тест: синтаксическая ошибка"""
        output, error = execute_code_safely('print("Hello', timeout=5)
        self.assertIsNotNone(error)
    
    def test_execute_dangerous_code(self):
        """Тест: опасный код (subprocess)"""
        output, error = execute_code_safely('import subprocess; subprocess.run(["ls"])', timeout=5)
        self.assertIsNotNone(error)
        self.assertIn('Обнаружена потенциально опасная конструкция', error)
    
    def test_endpoint_get_request(self):
        """Тест: GET запрос к endpoint"""
        response = self.client.get('/execute')
        self.assertEqual(response.status_code, 200)
    
    def test_endpoint_post_valid(self):
        """Тест: POST запрос с валидными данными"""
        response = self.client.post('/execute', data={
            'code': 'print("Test")',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('Test', text)
    
    def test_endpoint_post_empty_code(self):
        """Тест: POST запрос с пустым кодом"""
        response = self.client.post('/execute', data={
            'code': '',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        # Проверяем наличие ошибки валидации
        self.assertIn('Код обязателен для заполнения', text)
    
    def test_endpoint_post_invalid_timeout(self):
        """Тест: POST запрос с невалидным тайм-аутом"""
        response = self.client.post('/execute', data={
            'code': 'print("Test")',
            'timeout': 100
        })
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('от 1 до 30', text)
    
    def test_endpoint_post_negative_timeout(self):
        """Тест: POST запрос с отрицательным тайм-аутом"""
        response = self.client.post('/execute', data={
            'code': 'print("Test")',
            'timeout': -5
        })
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('от 1 до 30', text)
    
    def test_endpoint_post_timeout_exceeded(self):
        """Тест: превышение тайм-аута через endpoint"""
        response = self.client.post('/execute', data={
            'code': 'import time; time.sleep(3)',
            'timeout': 1
        })
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('не уложилось', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)