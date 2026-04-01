class BlockErrors:
    """
    Контекстный менеджер для игнорирования определенных типов исключений
    
    Args:
        err_types: множество типов исключений, которые нужно игнорировать
    """
    
    def __init__(self, err_types):
        self.err_types = err_types
    
    def __enter__(self):
        """Вход в контекстный менеджер"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекстного менеджера
        
        Returns:
            True - если исключение нужно подавить
            False - если исключение нужно пробросить дальше
        """
        # Если исключения нет, выходим
        if exc_type is None:
            return False
        
        # Проверяем, нужно ли игнорировать это исключение
        # Проверяем точное совпадение или наследование
        for err_type in self.err_types:
            if issubclass(exc_type, err_type):
                return True  # Игнорируем исключение
        
        # Если исключение не в списке игнорируемых, пробрасываем дальше
        return False