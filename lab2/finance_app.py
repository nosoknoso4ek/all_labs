from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# Хранилище расходов
# Структура: storage[год][месяц][день] = сумма
storage = {}

def parse_date(date_str):
    """Парсим дату YYYYMMDD в числа: год, месяц, день"""
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return year, month, day

@app.route('/add/<date>/<int:amount>')
def add_expense(date, amount):
    try:
        year, month, day = parse_date(date)
    except Exception:
        return "Неверный формат даты", 400

    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += amount
    return f"Добавлено: {amount} руб. за {escape(date)}"

@app.route('/calculate/<int:year>')
@app.route('/calculate/<int:year>/<int:month>')
def calculate_expense(year, month=None):
    if year not in storage:
        return f"Нет данных за {year}"
    
    total = 0
    if month is None:
        # Суммируем все месяцы
        for m in storage[year]:
            for d in storage[year][m]:
                total += storage[year][m][d]
        return f"Суммарные траты за {year}: {total} руб."
    else:
        if month not in storage[year]:
            return f"Нет данных за {year}/{month}"
        for d in storage[year][month]:
            total += storage[year][month][d]
        return f"Суммарные траты за {year}/{month}: {total} руб."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
