# app/finance.py
from flask import Flask

app = Flask(__name__)

storage = {}

@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    if len(date) != 8:
        return 'Неверный формат даты. Используйте YYYYMMDD', 400
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        if not (1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError
    except ValueError:
        return 'Неверная дата', 400

    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number
    return f'Добавлена трата {number} руб. за {date}', 200

@app.route('/calculate/<int:year>')
def calculate_year(year):
    if year not in storage:
        return f'За {year} год трат не зарегистрировано', 200
    total = sum(storage[year].values())
    return f'Суммарные траты за {year} год: {total} руб.', 200

@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    if year not in storage or month not in storage[year]:
        return f'За {year}-{month:02d} трат не зарегистрировано', 200
    total = storage[year][month]
    return f'Суммарные траты за {year}-{month:02d}: {total} руб.', 200

if __name__ == '__main__':
    app.run(debug=True)