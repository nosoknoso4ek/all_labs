# -*- coding: utf-8 -*-
from flask import Flask
import random
from datetime import datetime
from datetime import timedelta 
import os
import re

app = Flask(__name__)

@app.route("/hello_world")
def hello_world():
    return "Привет, мир!"

cars_list = ["Chevrolet", "Renault", "Ford", "Lada"]

@app.route("/cars")
def cars():
    return ", ".join(cars_list)

cats_list = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]

@app.route("/cats")
def cats():
    return random.choice(cats_list) 

@app.route("/get_time/now")
def get_time_now():
    current_time = datetime.now() 
    return f"Точное время: {current_time}"

@app.route("/get_time/future")
def get_time_future():
    current_time_after_hour = datetime.now() + timedelta(hours=1)  # текущее время + 1 час
    return f"Точное время через час будет {current_time_after_hour}"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')


with open(BOOK_FILE, encoding='utf-8') as f:
    text = f.read()


words_list = re.findall(r'\b\w+\b', text, flags=re.UNICODE)

@app.route("/get_random_word")
def get_random_word():
    return random.choice(words_list)

@app.route("/counter")
def counter():
    counter.visits += 1
    return f"Страница была открыта {counter.visits} раз(а)"
counter.visits = 0 
            

if __name__ == "__main__":
    app.run(debug=True)