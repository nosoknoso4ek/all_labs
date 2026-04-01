import unittest
import sys
import os

# Добавляем путь к папке app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app
import subprocess
from unittest.mock import patch


class TestUptimeEndpoint(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_uptime_endpoint_returns_200(self):
        """Тест: endpoint /uptime возвращает статус 200"""
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 200)
    
    def test_uptime_returns_string(self):
        """Тест: endpoint /uptime возвращает строку"""
        response = self.client.get('/uptime')
        text = response.get_data(as_text=True)
        self.assertIsInstance(text, str)
    
    def test_uptime_contains_current_uptime(self):
        """Тест: ответ содержит фразу 'Current uptime is'"""
        response = self.client.get('/uptime')
        text = response.get_data(as_text=True)
        self.assertIn('Current uptime is', text)
    
    def test_uptime_contains_time_info(self):
        """Тест: ответ содержит информацию о времени"""
        response = self.client.get('/uptime')
        text = response.get_data(as_text=True)
        # Проверяем, что в ответе есть цифры (время)
        self.assertTrue(any(c.isdigit() for c in text))
    
    def test_uptime_not_empty(self):
        """Тест: ответ не пустой"""
        response = self.client.get('/uptime')
        text = response.get_data(as_text=True)
        self.assertTrue(len(text) > 0)
    
    @patch('subprocess.run')
    def test_uptime_command_error(self, mock_run):
        """Тест: обработка ошибки при выполнении команды uptime"""
        # Мокаем ошибку выполнения команды
        mock_run.side_effect = Exception('Command failed')
        
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 500)
        text = response.get_data(as_text=True)
        self.assertIn('Error getting uptime', text)
    
    @patch('subprocess.run')
    def test_uptime_empty_output(self, mock_run):
        """Тест: обработка пустого вывода команды"""
        # Мокаем пустой вывод
        mock_result = unittest.mock.Mock()
        mock_result.returncode = 0
        mock_result.stdout = ''
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 500)
        text = response.get_data(as_text=True)
        self.assertIn('Unable to get system uptime', text)
    
    @patch('subprocess.run')
    def test_uptime_successful_output(self, mock_run):
        """Тест: успешное получение uptime"""
        # Мокаем успешный вывод
        mock_result = unittest.mock.Mock()
        mock_result.returncode = 0
        mock_result.stdout = '10:30:00 up 5 days, 2:30, 3 users'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertEqual(text, 'Current uptime is 10:30:00 up 5 days, 2:30, 3 users')


if __name__ == '__main__':
    unittest.main(verbosity=2)