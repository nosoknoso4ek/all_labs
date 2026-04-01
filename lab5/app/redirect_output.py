import sys
import io
import traceback


class Redirect:
    """
    Контекстный менеджер для перенаправления stdout и stderr
    
    Args:
        stdout: IO объект для перенаправления stdout (опционально)
        stderr: IO объект для перенаправления stderr (опционально)
    """
    
    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None
    
    def __enter__(self):
        # Сохраняем текущие потоки
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        
        # Перенаправляем stdout если указан
        if self.stdout is not None:
            sys.stdout = self.stdout
        
        # Перенаправляем stderr если указан
        if self.stderr is not None:
            sys.stderr = self.stderr
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Восстанавливаем исходные потоки
        if self.old_stdout is not None:
            sys.stdout = self.old_stdout
        
        if self.old_stderr is not None:
            sys.stderr = self.old_stderr
        
        # Если было исключение, записываем его в stderr если нужно
        if exc_type is not None and self.stderr is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb, file=self.stderr)
        
        # Не подавляем исключение
        return False


class RedirectStringIO:
    """
    Упрощенная версия для перенаправления в строковые буферы
    """
    def __init__(self, stdout=False, stderr=False):
        """
        Args:
            stdout: если True, перенаправляем stdout в StringIO
            stderr: если True, перенаправляем stderr в StringIO
        """
        self.redirect_stdout = stdout
        self.redirect_stderr = stderr
        self.stdout_buffer = None
        self.stderr_buffer = None
        self.old_stdout = None
        self.old_stderr = None
    
    def __enter__(self):
        # Сохраняем текущие потоки
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        
        # Создаем буферы и перенаправляем stdout если нужно
        if self.redirect_stdout:
            self.stdout_buffer = io.StringIO()
            sys.stdout = self.stdout_buffer
        
        # Создаем буферы и перенаправляем stderr если нужно
        if self.redirect_stderr:
            self.stderr_buffer = io.StringIO()
            sys.stderr = self.stderr_buffer
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Восстанавливаем исходные потоки
        if self.old_stdout is not None:
            sys.stdout = self.old_stdout
        
        if self.old_stderr is not None:
            sys.stderr = self.old_stderr
        
        return False
    
    def get_stdout(self):
        """Возвращает содержимое stdout буфера"""
        if self.stdout_buffer:
            return self.stdout_buffer.getvalue()
        return None
    
    def get_stderr(self):
        """Возвращает содержимое stderr буфера"""
        if self.stderr_buffer:
            return self.stderr_buffer.getvalue()
        return None