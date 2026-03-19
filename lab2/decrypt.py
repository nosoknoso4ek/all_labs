import sys

def decrypt(text):
    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i+1] == '.':
            # проверяем, есть ли вторая точка
            if i + 2 < len(text) and text[i+2] == '.':
                # правило двух точек → удалить предыдущий символ
                if result:
                    result.pop()
                i += 3  # пропускаем текущий символ и две точки
                continue
            else:
                # правило одной точки → оставляем текущий символ
                result.append(text[i])
                i += 2  # пропускаем текущий символ и точку
                continue
        else:
            # обычный символ
            result.append(text[i])
            i += 1
    return ''.join(result)

if __name__ == "__main__":
    input_text = sys.stdin.read().strip()  # читаем строку из pipe
    output_text = decrypt(input_text)
    print(output_text)
