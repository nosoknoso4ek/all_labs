# tests/test_decryptor.py
from app.decryptor import decrypt

def test_no_extra_dots():
    assert decrypt("абра-кадабра") == "абра-кадабра"

def test_few_extra_dots_and_dash():
    cases = [
        ("абраа..-кадабра", "абра-кадабра"),
        ("абраа..-.кадабра", "абра-кадабра"),
        ("абра--..кадабра", "абра-кадабра"),
        ("абрау...-кадабра", "абра-кадабра")
    ]
    for input_text, expected in cases:
        assert decrypt(input_text) == expected

def test_only_dots_or_digits():
    cases = [
        ("абра........", ""),
        ("абр......a.", "a"),
        ("1..2.3", "23"),
        (".", ""),
        ("1.......................", "")
    ]
    for input_text, expected in cases:
        assert decrypt(input_text) == expected