import subprocess
import shlex
import tempfile
import os
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CodeExecutionForm(FlaskForm):
    """Форма для выполнения кода"""
    code = StringField('Code', validators=[
        DataRequired(message='Код обязателен для заполнения')
    ])
    timeout = IntegerField('Timeout', validators=[
        DataRequired(message='Тайм-аут обязателен для заполнения'),
        NumberRange(min=1, max=30, message='Тайм-аут должен быть от 1 до 30 секунд')
    ])


def execute_code_with_timeout(code, timeout):
    """
    Выполняет Python код с ограничением по времени
    
    Returns:
        tuple: (output, error_message, success)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Формируем команду с ограничением ресурсов
        cmd = f'prlimit --nproc=1:1 python3 {temp_file}'
        
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode == 0:
                return stdout, None, True
            else:
                return stdout, stderr, False
                
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return None, f"Исполнение кода не уложилось в {timeout} секунд", False
            
    except Exception as e:
        return None, f"Ошибка выполнения: {str(e)}", False
        
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


def execute_code_safely(code, timeout):
    """
    Безопасное выполнение кода
    
    Returns:
        tuple: (output, error_message)
    """
    dangerous_patterns = [
        '__import__', 'exec(', 'eval(', 'compile(', 'open(', 'file(',
        '__builtins__', 'subprocess', 'os.system', 'os.popen', 'os.spawn',
        'os.fork', 'pty.spawn', 'socket'
    ]
    
    for pattern in dangerous_patterns:
        if pattern in code:
            return None, f"Обнаружена потенциально опасная конструкция: {pattern}"
    
    output, error, success = execute_code_with_timeout(code, timeout)
    
    if success:
        return output, None
    else:
        return None, error