# tests/test_finance.py
import unittest
import sys
import os

# Добавляем путь к папке app для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from finance import app, storage


class TestFinanceApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def setUp(self):
        storage.clear()

    def test_add_valid_expense_success(self):
        """Тест 1: Успешное добавление траты"""
        response = self.client.get('/add/20260326/1000')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добавлена трата 1000 руб. за 20260326', response.get_data(as_text=True))
        self.assertIn(2026, storage)
        self.assertIn(3, storage[2026])
        self.assertEqual(storage[2026][3], 1000)

    def test_add_accumulates_in_same_month(self):
        """Тест 2: Накопление трат за один месяц"""
        self.client.get('/add/20260326/1000')
        self.client.get('/add/20260326/500')
        self.client.get('/add/20260326/250')
        # Исправлено: 2026 вместо 2024
        self.assertEqual(storage[2026][3], 1750)

    def test_add_rejects_invalid_date_format(self):
        """Тест 3: Проверка отклонения невалидных дат"""
        invalid_dates = [
            '202603',
            '202603260',
            '2026-03-26',
            'abcd0326',
            '20261301',
            '20260026',
            '20260132',
            '20260100',
        ]
        for bad_date in invalid_dates:
            with self.subTest(bad_date=bad_date):
                response = self.client.get(f'/add/{bad_date}/1000')
                self.assertEqual(
                    response.status_code, 400,
                    f'Дата "{bad_date}" должна быть отклонена'
                )
                response_text = response.get_data(as_text=True)
                self.assertTrue(
                    'Неверный формат' in response_text or 'Неверная дата' in response_text,
                    f'Ответ для "{bad_date}" должен содержать сообщение об ошибке'
                )

    def test_calculate_year_with_expenses(self):
        """Тест 4: Расчет за год с существующими тратами"""
        storage[2026] = {1: 1000, 3: 2000, 6: 1500, 12: 500}
        response = self.client.get('/calculate/2026')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Суммарные траты за 2026 год: 5000 руб.', response.get_data(as_text=True))

    def test_calculate_year_empty_storage(self):
        """Тест 5: Расчет за год с пустым хранилищем"""
        response = self.client.get('/calculate/2023')
        self.assertEqual(response.status_code, 200)
        self.assertIn('За 2023 год трат не зарегистрировано', response.get_data(as_text=True))

    def test_calculate_year_via_api_workflow(self):
        """Тест 6: Расчет за год через API workflow"""
        self.client.get('/add/20260115/1000')
        self.client.get('/add/20260220/2000')
        self.client.get('/add/20260228/500')

        response = self.client.get('/calculate/2026')
        self.assertEqual(response.status_code, 200)
        self.assertIn('3500 руб.', response.get_data(as_text=True))

    def test_calculate_month_with_expenses(self):
        """Тест 7: Расчет за месяц с существующими тратами"""
        storage[2026] = {3: 2500}
        response = self.client.get('/calculate/2026/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Суммарные траты за 2026-03: 2500 руб.', response.get_data(as_text=True))

    def test_calculate_month_empty_storage(self):
        """Тест 8: Расчет за месяц с пустым хранилищем"""
        response = self.client.get('/calculate/2026/5')
        self.assertEqual(response.status_code, 200)
        self.assertIn('За 2026-05 трат не зарегистрировано', response.get_data(as_text=True))

    def test_calculate_month_via_api_workflow(self):
        """Тест 9: Расчет за месяц через API workflow"""
        self.client.get('/add/20260315/1000')
        self.client.get('/add/20260320/500')
        self.client.get('/add/20260410/9999')

        response = self.client.get('/calculate/2026/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1500 руб.', response.get_data(as_text=True))
        self.assertNotIn('9999', response.get_data(as_text=True))

    def test_month_formatting_with_leading_zero(self):
        """Тест 10: Проверка форматирования месяцев с ведущим нулем"""
        storage[2026] = {1: 100, 9: 200}

        for month, expected in [(1, '2026-01'), (9, '2026-09'), (12, '2026-12')]:
            with self.subTest(month=month):
                response = self.client.get(f'/calculate/2026/{month}')
                self.assertIn(expected, response.get_data(as_text=True))

    def test_storage_isolation_between_tests(self):
        """Тест 11: Проверка изоляции storage между тестами"""
        self.client.get('/add/20260101/100')
        self.assertIn(2026, storage)
        storage.clear()
        self.assertNotIn(2026, storage)


if __name__ == '__main__':
    unittest.main(verbosity=2)