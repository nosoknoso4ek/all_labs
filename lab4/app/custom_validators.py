from wtforms.validators import ValidationError
from typing import Optional


# ========== ФУНКЦИОНАЛЬНЫЙ ВАЛИДАТОР ==========

def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Валидатор для проверки длины числа (количества цифр)
    
    Args:
        min: минимальная длина числа
        max: максимальная длина числа
        message: сообщение об ошибке (опционально)
    """
    def _number_length(form, field):
        # Получаем значение поля
        value = field.data
        
        # Если значение пустое, пропускаем валидацию (другой валидатор проверит обязательность)
        if value is None or value == '':
            return
        
        # Преобразуем в строку для подсчета длины
        str_value = str(value)
        
        # Убираем знак минуса для отрицательных чисел (если нужно)
        if str_value.startswith('-'):
            str_value = str_value[1:]
        
        # Проверяем длину
        if not (min <= len(str_value) <= max):
            if message is None:
                raise ValidationError(f'Длина числа должна быть от {min} до {max} цифр')
            else:
                raise ValidationError(message)
    
    return _number_length


# ========== КЛАССОВЫЙ ВАЛИДАТОР ==========

class NumberLength:
    """
    Класс-валидатор для проверки длины числа (количества цифр)
    """
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        """
        Args:
            min: минимальная длина числа
            max: максимальная длина числа
            message: сообщение об ошибке (опционально)
        """
        self.min = min
        self.max = max
        self.message = message
    
    def __call__(self, form, field):
        """
        Метод вызывается при валидации
        """
        value = field.data
        
        # Если значение пустое, пропускаем валидацию
        if value is None or value == '':
            return
        
        # Преобразуем в строку для подсчета длины
        str_value = str(value)
        
        # Убираем знак минуса для отрицательных чисел
        if str_value.startswith('-'):
            str_value = str_value[1:]
        
        # Проверяем длину
        if not (self.min <= len(str_value) <= self.max):
            if self.message is None:
                raise ValidationError(f'Длина числа должна быть от {self.min} до {self.max} цифр')
            else:
                raise ValidationError(self.message)