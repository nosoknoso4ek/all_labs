import unittest
import sys
import os

# Добавляем путь к папке app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app
from unittest.mock import patch


class TestPsEndpoint(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_ps_no_arguments(self):
        """Тест: запрос без аргументов возвращает ошибку 400"""
        response = self.client.get('/ps')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No arguments provided', response.get_data(as_text=True))
    
    def test_ps_with_single_argument(self):
        """Тест: запрос с одним аргументом"""
        response = self.client.get('/ps?arg=a')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('ps a', text)
    
    def test_ps_with_multiple_arguments(self):
        """Тест: запрос с несколькими аргументами"""
        response = self.client.get('/ps?arg=a&arg=u&arg=x')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('ps a u x', text)
    
    def test_ps_with_aux_arguments(self):
        """Тест: запрос с аргументами aux"""
        response = self.client.get('/ps?arg=a&arg=u&arg=x')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        # Проверяем, что вывод содержит информацию о процессах
        self.assertIn('PID', text)
    
    def test_ps_returns_pre_tag(self):
        """Тест: ответ содержит тег <pre>"""
        response = self.client.get('/ps?arg=a')
        text = response.get_data(as_text=True)
        self.assertIn('<pre>', text)
        self.assertIn('</pre>', text)
    
    def test_ps_with_different_arguments(self):
        """Тест: запрос с разными аргументами"""
        response = self.client.get('/ps?arg=aux')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('ps aux', text)
    
    @patch('subprocess.run')
    def test_ps_command_error(self, mock_run):
        """Тест: обработка ошибки выполнения команды"""
        # Мокаем ошибку
        mock_result = unittest.mock.Mock()
        mock_result.returncode = 1
        mock_result.stdout = ''
        mock_result.stderr = 'Command failed'
        mock_run.return_value = mock_result
        
        response = self.client.get('/ps?arg=a')
        self.assertEqual(response.status_code, 500)
        text = response.get_data(as_text=True)
        self.assertIn('Command failed', text)
    
    @patch('subprocess.run')
    def test_ps_successful_execution(self, mock_run):
        """Тест: успешное выполнение команды"""
        # Мокаем успешное выполнение
        mock_result = unittest.mock.Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'PID TTY TIME CMD\n1234 pts/0 00:00:00 bash'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        response = self.client.get('/ps?arg=aux')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('ps aux', text)
        self.assertIn('PID', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)