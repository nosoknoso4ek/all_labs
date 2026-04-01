import unittest
import sys
import os
from datetime import datetime
from unittest.mock import patch

# Добавляем путь к папке app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from person import Person


class TestPersonInit(unittest.TestCase):
    def test_init_with_required_args(self):
        p = Person('Анна', 1990)
        self.assertEqual(p.name, 'Анна')
        self.assertEqual(p.yob, 1990)
        self.assertEqual(p.address, '')

    def test_init_with_all_args(self):
        p = Person('Борис', 1985, 'г. Москва, ул. Ленина, 10')
        self.assertEqual(p.name, 'Борис')
        self.assertEqual(p.yob, 1985)
        self.assertEqual(p.address, 'г. Москва, ул. Ленина, 10')


class TestPersonGetAge(unittest.TestCase):
    @patch('person.datetime.datetime')
    def test_get_age_calculation(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 6, 15)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        p = Person('Тест', 2000)
        self.assertEqual(p.get_age(), 24)

    @patch('person.datetime.datetime')
    def test_get_age_newborn(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        p = Person('Младенец', 2024)
        self.assertEqual(p.get_age(), 0)


class TestPersonGetName(unittest.TestCase):
    def test_get_name_returns_correct_value(self):
        p = Person('Дмитрий', 1978)
        self.assertEqual(p.get_name(), 'Дмитрий')

    def test_get_name_after_set_name(self):
        p = Person('Старое', 1990)
        p.set_name('Новое')
        self.assertEqual(p.get_name(), 'Новое')


class TestPersonSetName(unittest.TestCase):
    def test_set_name_changes_value(self):
        p = Person('Иван', 1980)
        p.set_name('Пётр')
        self.assertEqual(p.name, 'Пётр')
        self.assertEqual(p.get_name(), 'Пётр')

    def test_set_name_accepts_empty_string(self):
        p = Person('Непустое', 1995)
        p.set_name('')
        self.assertEqual(p.name, '')


class TestPersonGetAddress(unittest.TestCase):
    def test_get_address_default_empty(self):
        p = Person('Тест', 2000)
        self.assertEqual(p.get_address(), '')

    def test_get_address_returns_set_value(self):
        p = Person('Тест', 2000, 'ул. Примерная, 1')
        self.assertEqual(p.get_address(), 'ул. Примерная, 1')


class TestPersonSetAddress(unittest.TestCase):
    def test_set_address_changes_value(self):
        p = Person('Тест', 2000, 'Старый адрес')
        p.set_address('Новый адрес')
        self.assertEqual(p.address, 'Новый адрес')

    def test_set_address_can_clear(self):
        p = Person('Тест', 2000, 'Был адрес')
        p.set_address('')
        self.assertEqual(p.address, '')


class TestPersonIsHomeless(unittest.TestCase):
    def test_is_homeless_when_address_empty(self):
        p = Person('Бездомный', 1990, '')
        self.assertTrue(p.is_homeless())

    def test_is_homeless_when_address_not_set(self):
        p = Person('Без адреса', 1985)
        self.assertTrue(p.is_homeless())

    def test_is_homeless_false_when_address_set(self):
        p = Person('Домосед', 2000, 'Дом, милый дом')
        self.assertFalse(p.is_homeless())

    def test_is_homeless_after_clearing_address(self):
        p = Person('Тест', 2000, 'Есть адрес')
        self.assertFalse(p.is_homeless())
        p.set_address('')
        self.assertTrue(p.is_homeless())


if __name__ == '__main__':
    unittest.main(verbosity=2)
