from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Кортеж дней недели на русском (0 = понедельник)
weekdays = ("понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья")

@app.route('/hello-world/<name>')
def hello_world(name):
    day_index = datetime.today().weekday()
    day_name = weekdays[day_index]
    return f"Привет, {name}. Хорошей {day_name}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
