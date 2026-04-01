import freezegun
from app.username import get_username, extract_weekday

def test_extract_weekday():
    # Проверяем, что функция извлекает день недели
    assert extract_weekday("Хорошей среды") == "среды"
    assert extract_weekday("Привет") is None

@freezegun.freeze_time("2024-03-20")  # зафиксируем дату на среду
def test_correct_weekday_inserted():
    # Проверяем, что функция добавляет правильный день недели
    result = get_username("Хорошего дня")
    assert "среды" in result.lower()

def test_user_provided_weekday_not_changed():
    # Если пользователь сам указал день недели — ничего не меняем
    result = get_username("Хорошей среды")
    assert result == "Хорошей среды"