import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    
    def test_ignore_specific_error(self):
        """Тест 1: Ошибка игнорируется (ZeroDivisionError)"""
        err_types = {ZeroDivisionError, TypeError}
        
        with BlockErrors(err_types):
            a = 1 / 0
        
        # Если дошли сюда, значит ошибка проигнорирована
        self.assertTrue(True)
    
    def test_ignore_error_with_else(self):
        """Тест 1.1: Ошибка игнорируется, выполняется код после блока"""
        err_types = {ZeroDivisionError, TypeError}
        executed = False
        
        with BlockErrors(err_types):
            a = 1 / 0
        
        executed = True
        self.assertTrue(executed)
    
    def test_propagate_error(self):
        """Тест 2: Ошибка прокидывается выше (TypeError не в списке)"""
        err_types = {ZeroDivisionError}
        
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'
    
    def test_nested_blocks_inner_propagate_outer_ignore(self):
        """Тест 3: Ошибка прокидывается во внутреннем блоке, игнорируется во внешнем"""
        outer_err_types = {TypeError}
        result = []
        
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            try:
                with BlockErrors(inner_err_types):
                    a = 1 / '0'  # TypeError - не в inner_err_types
            except TypeError:
                result.append("inner_propagated")
            
            result.append("outer_continued")
        
        self.assertIn("inner_propagated", result)
        self.assertIn("outer_continued", result)
    
    def test_ignore_child_error(self):
        """Тест 4: Дочерние ошибки игнорируются (ZeroDivisionError - дочерний ArithmeticError)"""
        err_types = {ArithmeticError}
        
        with BlockErrors(err_types):
            a = 1 / 0  # ZeroDivisionError - дочерний ArithmeticError
        
        self.assertTrue(True)
    
    def test_ignore_multiple_errors(self):
        """Тест 5: Игнорирование нескольких типов ошибок"""
        err_types = {ZeroDivisionError, TypeError}
        
        # Проверяем игнорирование ZeroDivisionError
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)
        
        # Проверяем игнорирование TypeError
        with BlockErrors(err_types):
            a = 1 / '0'
        self.assertTrue(True)
    
    def test_no_error(self):
        """Тест 6: Без ошибок - все работает нормально"""
        err_types = {ZeroDivisionError}
        result = []
        
        with BlockErrors(err_types):
            result.append("inside")
        
        result.append("after")
        self.assertEqual(result, ["inside", "after"])
    
    def test_ignore_exception_class(self):
        """Тест 7: Игнорирование базового класса исключений"""
        err_types = {Exception}
        
        with BlockErrors(err_types):
            a = 1 / '0'  # TypeError - дочерний Exception
        
        self.assertTrue(True)
    
    def test_nested_blocks_both_ignore(self):
        """Тест 8: Вложенные блоки, оба игнорируют"""
        outer_err_types = {Exception}
        inner_err_types = {ZeroDivisionError}
        
        with BlockErrors(outer_err_types):
            with BlockErrors(inner_err_types):
                a = 1 / 0  # ZeroDivisionError игнорируется
        
        self.assertTrue(True)
    
    def test_nested_blocks_both_propagate(self):
        """Тест 9: Вложенные блоки, ошибка прокидывается через оба"""
        outer_err_types = {ZeroDivisionError}
        inner_err_types = {ValueError}
        
        with self.assertRaises(TypeError):
            with BlockErrors(outer_err_types):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'  # TypeError - не в списках
    
    def test_error_with_message_preserved(self):
        """Тест 10: Сообщение об ошибке сохраняется при пробрасывании"""
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / '0'
        except TypeError as e:
            self.assertIn("unsupported operand", str(e))
        else:
            self.fail("Ошибка не была проброшена")
    
    def test_empty_error_set(self):
        """Тест 11: Пустой набор ошибок - все ошибки пробрасываются"""
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(set()):
                a = 1 / 0
    
    def test_ignore_with_multiple_exceptions(self):
        """Тест 12: Игнорирование нескольких исключений в одном блоке"""
        err_types = {ZeroDivisionError, TypeError, ValueError}
        
        # Проверяем ZeroDivisionError
        with BlockErrors(err_types):
            a = 1 / 0
        
        # Проверяем TypeError
        with BlockErrors(err_types):
            a = 1 / '0'
        
        # Проверяем ValueError
        with BlockErrors(err_types):
            a = int('abc')
        
        self.assertTrue(True)
    
    def test_context_manager_returns_self(self):
        """Тест 13: Контекстный менеджер возвращает себя"""
        err_types = {ZeroDivisionError}
        
        with BlockErrors(err_types) as manager:
            self.assertIsInstance(manager, BlockErrors)
    
    def test_exception_not_raised_when_ignored(self):
        """Тест 14: Исключение не поднимается когда игнорируется"""
        err_types = {ZeroDivisionError}
        exception_occurred = False
        
        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except Exception:
            exception_occurred = True
        
        self.assertFalse(exception_occurred)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    