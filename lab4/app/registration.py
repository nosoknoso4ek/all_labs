from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional
from custom_validators import number_length, NumberLength
import subprocess
import shlex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'


class RegistrationForm(FlaskForm):
    # Email - обязательный, с валидацией формата
    email = StringField('Email', validators=[
        DataRequired(message='Email обязателен для заполнения'),
        Email(message='Введите корректный email адрес')
    ])
    
    # Телефон - обязательный, проверка длины через наш валидатор (функциональный)
    phone = StringField('Phone', validators=[
        DataRequired(message='Телефон обязателен для заполнения'),
        Regexp(r'^\d+$', message='Телефон должен содержать только цифры'),
        number_length(min=10, max=10, message='Телефон должен содержать ровно 10 цифр')
    ])
    
    # Имя - обязательное
    name = StringField('Name', validators=[
        DataRequired(message='Имя обязательно для заполнения')
    ])
    
    # Адрес - обязательный
    address = StringField('Address', validators=[
        DataRequired(message='Адрес обязателен для заполнения')
    ])
    
    # Индекс - обязательный, проверка длины через наш валидатор (классовый)
    index = StringField('Index', validators=[
        DataRequired(message='Индекс обязателен для заполнения'),
        Regexp(r'^\d+$', message='Индекс должен содержать только цифры'),
        NumberLength(min=5, max=7, message='Индекс должен содержать от 5 до 7 цифр')
    ])
    
    # Комментарий - необязательный
    comment = TextAreaField('Comment', validators=[
        Optional()
    ])


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        flash(f'Регистрация успешна! Добро пожаловать, {form.name.data}!', 'success')
        return redirect(url_for('registration'))
    
    return render_template('registration.html', form=form)


@app.route('/uptime', methods=['GET'])
def uptime():
    """
    Endpoint для получения uptime системы
    """
    try:
        # Выполняем команду uptime
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        
        # Получаем вывод команды
        uptime_output = result.stdout.strip()
        
        # Если команда выполнилась успешно
        if result.returncode == 0 and uptime_output:
            return f"Current uptime is {uptime_output}", 200
        else:
            return "Unable to get system uptime", 500
            
    except Exception as e:
        return f"Error getting uptime: {str(e)}", 500


@app.route('/ps', methods=['GET'])
def ps_command():
    """
    Endpoint для выполнения команды ps с аргументами
    Пример: /ps?arg=a&arg=u&arg=x
    """
    try:
        # Получаем список аргументов из запроса
        args = request.args.getlist('arg')
        
        # Проверяем, что аргументы есть
        if not args:
            return "<pre>No arguments provided. Example: /ps?arg=a&arg=u&arg=x</pre>", 400
        
        # Формируем команду
        # Первый аргумент всегда 'ps'
        command_parts = ['ps']
        
        # Добавляем аргументы с экранированием для безопасности
        for arg in args:
            # Экранируем каждый аргумент для защиты от инъекций
            command_parts.append(shlex.quote(arg))
        
        # Собираем команду в строку
        command_str = ' '.join(command_parts)
        
        # Разбиваем команду на части для subprocess
        # Используем shlex.split для правильной обработки экранированных аргументов
        command = shlex.split(command_str)
        
        # Выполняем команду
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Форматируем вывод в HTML с тегом <pre>
        if result.returncode == 0:
            output = f"<pre>Command: ps {' '.join(args)}\n\n{result.stdout}</pre>"
            return output, 200
        else:
            error_output = f"<pre>Command failed with return code {result.returncode}\n\nError: {result.stderr}</pre>"
            return error_output, 500
            
    except Exception as e:
        return f"<pre>Error executing command: {str(e)}</pre>", 500


@app.route('/')
def index():
    return redirect(url_for('registration'))


if __name__ == '__main__':
    app.run(debug=True)