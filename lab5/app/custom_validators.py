from wtforms.validators import ValidationError
from typing import Optional


def number_length(min: int, max: int, message: Optional[str] = None):
    """Функциональный валидатор для проверки длины числа"""
    def _number_length(form, field):
        value = field.data
        if value is None or value == '':
            return
        str_value = str(value)
        if str_value.startswith('-'):
            str_value = str_value[1:]
        if not (min <= len(str_value) <= max):
            if message is None:
                raise ValidationError(f'Длина числа должна быть от {min} до {max} цифр')
            else:
                raise ValidationError(message)
    return _number_length


class NumberLength:
    """Классовый валидатор для проверки длины числа"""
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message
    
    def __call__(self, form, field):
        value = field.data
        if value is None or value == '':
            return
        str_value = str(value)
        if str_value.startswith('-'):
            str_value = str_value[1:]
        if not (self.min <= len(str_value) <= self.max):
            if self.message is None:
                raise ValidationError(f'Длина числа должна быть от {self.min} до {self.max} цифр')
            else:
                raise ValidationError(self.message)