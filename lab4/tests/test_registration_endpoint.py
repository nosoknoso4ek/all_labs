import unittest
import sys
import os

# Добавляем путь к папке app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from registration import app


class TestRegistrationEndpoint(unittest.TestCase):
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ EMAIL ====================
    
    def test_email_valid(self):
        """Тест: валидный email - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456',
            'comment': 'Тест'
        }, follow_redirects=True)
        
        # Проверяем, что нет ошибок для email
        self.assertNotIn('Email', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_email_empty(self):
        """Тест: пустой email - не проходит"""
        response = self.client.post('/registration', data={
            'email': '',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Email обязателен для заполнения', response.get_data(as_text=True))
    
    def test_email_invalid_format(self):
        """Тест: неверный формат email - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'invalid-email',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Введите корректный email адрес', response.get_data(as_text=True))
    
    def test_email_no_at_symbol(self):
        """Тест: email без @ - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test.example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Введите корректный email адрес', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ PHONE ====================
    
    def test_phone_valid(self):
        """Тест: валидный телефон (10 цифр) - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        }, follow_redirects=True)
        
        self.assertNotIn('Телефон', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_phone_empty(self):
        """Тест: пустой телефон - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Телефон обязателен для заполнения', response.get_data(as_text=True))
    
    def test_phone_too_short(self):
        """Тест: телефон слишком короткий (меньше 10 цифр) - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '12345',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Телефон должен содержать ровно 10 цифр', response.get_data(as_text=True))
    
    def test_phone_too_long(self):
        """Тест: телефон слишком длинный (больше 10 цифр) - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '123456789012',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Телефон должен содержать ровно 10 цифр', response.get_data(as_text=True))
    
    def test_phone_with_letters(self):
        """Тест: телефон содержит буквы - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': 'abc1234567',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Телефон должен содержать только цифры', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ NAME ====================
    
    def test_name_valid(self):
        """Тест: валидное имя - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        }, follow_redirects=True)
        
        self.assertNotIn('Имя', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_name_empty(self):
        """Тест: пустое имя - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': '',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        })
        
        self.assertIn('Имя обязательно для заполнения', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ ADDRESS ====================
    
    def test_address_valid(self):
        """Тест: валидный адрес - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, д. 1, кв. 10',
            'index': '123456'
        }, follow_redirects=True)
        
        self.assertNotIn('Адрес', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_address_empty(self):
        """Тест: пустой адрес - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': '',
            'index': '123456'
        })
        
        self.assertIn('Адрес обязателен для заполнения', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ INDEX ====================
    
    def test_index_valid_5_digits(self):
        """Тест: индекс из 5 цифр - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '12345'
        }, follow_redirects=True)
        
        self.assertNotIn('Индекс', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_index_valid_7_digits(self):
        """Тест: индекс из 7 цифр - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '1234567'
        }, follow_redirects=True)
        
        self.assertNotIn('Индекс', response.get_data(as_text=True))
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_index_empty(self):
        """Тест: пустой индекс - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': ''
        })
        
        self.assertIn('Индекс обязателен для заполнения', response.get_data(as_text=True))
    
    def test_index_too_short(self):
        """Тест: индекс слишком короткий (4 цифры) - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '1234'
        })
        
        self.assertIn('Индекс должен содержать от 5 до 7 цифр', response.get_data(as_text=True))
    
    def test_index_too_long(self):
        """Тест: индекс слишком длинный (8 цифр) - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '12345678'
        })
        
        self.assertIn('Индекс должен содержать от 5 до 7 цифр', response.get_data(as_text=True))
    
    def test_index_with_letters(self):
        """Тест: индекс содержит буквы - не проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': 'abc123'
        })
        
        self.assertIn('Индекс должен содержать только цифры', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ ДЛЯ ПОЛЯ COMMENT ====================
    
    def test_comment_optional_empty(self):
        """Тест: комментарий пустой - проходит (опциональное поле)"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456',
            'comment': ''
        }, follow_redirects=True)
        
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_comment_optional_not_provided(self):
        """Тест: комментарий не передан - проходит (опциональное поле)"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456'
        }, follow_redirects=True)
        
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    def test_comment_with_text(self):
        """Тест: комментарий с текстом - проходит"""
        response = self.client.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван Петров',
            'address': 'г. Москва, ул. Ленина, 1',
            'index': '123456',
            'comment': 'Это мой комментарий к регистрации'
        }, follow_redirects=True)
        
        self.assertIn('Регистрация успешна', response.get_data(as_text=True))
    
    # ==================== ТЕСТЫ С НЕСКОЛЬКИМИ ОШИБКАМИ ====================
    
    def test_multiple_errors(self):
        """Тест: несколько полей с ошибками одновременно"""
        response = self.client.post('/registration', data={
            'email': 'invalid',
            'phone': '123',
            'name': '',
            'address': '',
            'index': 'abc'
        })
        
        text = response.get_data(as_text=True)
        # Проверяем, что есть ошибки для всех полей
        self.assertIn('Email', text)
        self.assertIn('Телефон', text)
        self.assertIn('Имя', text)
        self.assertIn('Адрес', text)
        self.assertIn('Индекс', text)
    
    # ==================== ТЕСТЫ ДЛЯ GET-ЗАПРОСА ====================
    
    def test_get_registration_page(self):
        """Тест: GET запрос к странице регистрации"""
        response = self.client.get('/registration')
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('Регистрация', text)
        self.assertIn('Email', text)
        self.assertIn('Телефон', text)
    
    def test_root_redirect(self):
        """Тест: корневой путь '/' перенаправляет на '/registration'"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main(verbosity=2)
        def test_uptime_endpoint_exists(self):
        """Тест: endpoint /uptime существует"""
        response = self.client.get('/uptime')
        self.assertEqual(response.status_code, 200)