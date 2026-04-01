import unittest
import sys
import os
import io
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from redirect_output import Redirect, RedirectStringIO


class TestRedirectOutput(unittest.TestCase):
    
    def setUp(self):
        # Сохраняем оригинальные потоки
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def tearDown(self):
        # Восстанавливаем потоки
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def test_redirect_stdout_to_file(self):
        """Тест: перенаправление stdout в файл"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            temp_file = f.name
        
        try:
            with Redirect(stdout=open(temp_file, 'w')):
                print("Hello, redirected stdout!")
            
            # Проверяем содержимое файла
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn("Hello, redirected stdout!", content)
        finally:
            os.unlink(temp_file)
    
    def test_redirect_stderr_to_file(self):
        """Тест: перенаправление stderr в файл"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            temp_file = f.name
        
        try:
            with Redirect(stderr=open(temp_file, 'w')):
                sys.stderr.write("Error message!\n")
            
            # Проверяем содержимое файла
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn("Error message!", content)
        finally:
            os.unlink(temp_file)
    
    def test_redirect_both_to_files(self):
        """Тест: перенаправление stdout и stderr в разные файлы"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f1:
            stdout_file = f1.name
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f2:
            stderr_file = f2.name
        
        try:
            with Redirect(
                stdout=open(stdout_file, 'w'),
                stderr=open(stderr_file, 'w')
            ):
                print("stdout message")
                sys.stderr.write("stderr message\n")
            
            # Проверяем stdout файл
            with open(stdout_file, 'r') as f:
                self.assertIn("stdout message", f.read())
            
            # Проверяем stderr файл
            with open(stderr_file, 'r') as f:
                self.assertIn("stderr message", f.read())
        finally:
            os.unlink(stdout_file)
            os.unlink(stderr_file)
    
    def test_redirect_only_stdout(self):
        """Тест: перенаправление только stdout"""
        stdout_buffer = io.StringIO()
        original_stdout = sys.stdout
        
        with Redirect(stdout=stdout_buffer):
            print("Redirected stdout")
            sys.stderr.write("This goes to original stderr\n")
        
        # Проверяем, что stdout был перенаправлен
        self.assertIn("Redirected stdout", stdout_buffer.getvalue())
        
        # Проверяем, что stderr остался оригинальным
        self.assertEqual(sys.stdout, original_stdout)
    
    def test_redirect_only_stderr(self):
        """Тест: перенаправление только stderr"""
        stderr_buffer = io.StringIO()
        original_stderr = sys.stderr
        
        with Redirect(stderr=stderr_buffer):
            sys.stderr.write("Redirected stderr\n")
            print("This goes to original stdout")
        
        # Проверяем, что stderr был перенаправлен
        self.assertIn("Redirected stderr", stderr_buffer.getvalue())
        
        # Проверяем, что stdout остался оригинальным
        self.assertEqual(sys.stderr, original_stderr)
    
    def test_restore_after_context(self):
        """Тест: восстановление потоков после выхода из контекста"""
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        with Redirect(stdout=stdout_buffer, stderr=stderr_buffer):
            print("Inside context")
            sys.stderr.write("Inside context stderr\n")
        
        # Проверяем, что потоки восстановлены
        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)
        
        # Проверяем, что вывод попал в буферы
        self.assertIn("Inside context", stdout_buffer.getvalue())
        self.assertIn("Inside context stderr", stderr_buffer.getvalue())
    
    def test_nested_redirects(self):
        """Тест: вложенные перенаправления"""
        outer_buffer = io.StringIO()
        inner_buffer = io.StringIO()
        
        with Redirect(stdout=outer_buffer):
            print("Outer level")
            
            with Redirect(stdout=inner_buffer):
                print("Inner level")
            
            print("Back to outer")
        
        outer_content = outer_buffer.getvalue()
        inner_content = inner_buffer.getvalue()
        
        self.assertIn("Outer level", outer_content)
        self.assertIn("Back to outer", outer_content)
        self.assertIn("Inner level", inner_content)
        self.assertNotIn("Inner level", outer_content)
    
    def test_redirect_with_exception(self):
        """Тест: перенаправление при возникновении исключения"""
        stderr_buffer = io.StringIO()
        
        try:
            with Redirect(stderr=stderr_buffer):
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        stderr_content = stderr_buffer.getvalue()
        self.assertIn("ValueError", stderr_content)
        self.assertIn("Test exception", stderr_content)
    
    def test_no_arguments(self):
        """Тест: контекстный менеджер без аргументов"""
        original_stdout = sys.stdout
        
        with Redirect():
            print("This goes to original stdout")
        
        self.assertEqual(sys.stdout, original_stdout)
    
    def test_redirect_with_stringio(self):
        """Тест: перенаправление в StringIO"""
        stdout_buffer = io.StringIO()
        
        with Redirect(stdout=stdout_buffer):
            print("Message 1")
            print("Message 2")
        
        output = stdout_buffer.getvalue()
        self.assertIn("Message 1", output)
        self.assertIn("Message 2", output)
    
    def test_redirect_stdout_to_same_file_twice(self):
        """Тест: перенаправление stdout в один файл дважды"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            temp_file = f.name
        
        try:
            with Redirect(stdout=open(temp_file, 'w')):
                print("First message")
            
            with Redirect(stdout=open(temp_file, 'a')):
                print("Second message")
            
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertIn("First message", content)
                self.assertIn("Second message", content)
        finally:
            os.unlink(temp_file)
    
    def test_redirect_stringio_both(self):
        """Тест: RedirectStringIO для обоих потоков"""
        with RedirectStringIO(stdout=True, stderr=True) as redirect:
            print("stdout message")
            sys.stderr.write("stderr message\n")
            
            self.assertIn("stdout message", redirect.get_stdout())
            self.assertIn("stderr message", redirect.get_stderr())
    
    def test_redirect_stringio_stdout_only(self):
        """Тест: RedirectStringIO только для stdout"""
        with RedirectStringIO(stdout=True) as redirect:
            print("stdout message")
            sys.stderr.write("stderr message\n")
            
            self.assertIn("stdout message", redirect.get_stdout())
            self.assertIsNone(redirect.get_stderr())
    
    def test_redirect_stringio_stderr_only(self):
        """Тест: RedirectStringIO только для stderr"""
        with RedirectStringIO(stderr=True) as redirect:
            print("stdout message")
            sys.stderr.write("stderr message\n")
            
            self.assertIn("stderr message", redirect.get_stderr())
            self.assertIsNone(redirect.get_stdout())


if __name__ == '__main__':
    # Запуск тестов с выводом в файл для избежания конфликтов
    with open('test_results.txt', 'w') as test_file:
        runner = unittest.TextTestRunner(stream=test_file, verbosity=2)
        unittest.main(testRunner=runner, exit=False)
    
    # Также выводим в консоль
    print("\n" + "="*50)
    print("Тесты завершены. Результаты сохранены в test_results.txt")
    print("="*50)