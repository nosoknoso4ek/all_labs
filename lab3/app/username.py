
from datetime import datetime

WEEKDAYS = {
    0: "понедельника",
    1: "вторника",
    2: "среды",
    3: "четверга",
    4: "пятницы",
    5: "субботы",
    6: "воскресенья",
}

def get_current_weekday():
    """Возвращает сегодняшний день недели на русском"""
    return WEEKDAYS[datetime.now().weekday()]

def extract_weekday(text):
    """
    Ищет в строке день недели. 
    Если находит — возвращает его, иначе None
    """
    for day in WEEKDAYS.values():
        if day in text.lower():
            return day
    return None

def get_username(username: str) -> str:
    """
    Возвращает username с добавлением сегодняшнего дня недели,
    если пользователь сам не указал день недели.
    """
    weekday = extract_weekday(username)
    if weekday:
        return username
    return f"{username} {get_current_weekday()}"
if __name__ == "__main__":
    username = input("Введите имя пользователя: ")
    result = get_username(username)
    print("Результат:", result)
