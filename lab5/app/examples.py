cat > app/examples.py << 'EOF'
from block_errors import BlockErrors

print("=" * 50)
print("Пример 1: Игнорируем ZeroDivisionError и TypeError")
print("=" * 50)

err_types = {ZeroDivisionError, TypeError}
with BlockErrors(err_types):
    a = 1 / 0
print('Выполнено без ошибок\n')


print("=" * 50)
print("Пример 2: TypeError не игнорируется")
print("=" * 50)

try:
    err_types = {ZeroDivisionError}
    with BlockErrors(err_types):
        a = 1 / '0'  # TypeError - вызовет исключение
except TypeError as e:
    print(f"Поймано исключение: {e}\n")


print("=" * 50)
print("Пример 3: Вложенные блоки")
print("=" * 50)

outer_err_types = {TypeError}
with BlockErrors(outer_err_types):
    inner_err_types = {ZeroDivisionError}
    with BlockErrors(inner_err_types):
        a = 1 / '0'  # TypeError - прокидывается во внешний блок
    print('Внутренний блок')  # Не выполнится
print('Внешний блок\n')


print("=" * 50)
print("Пример 4: Игнорируем все исключения")
print("=" * 50)

err_types = {Exception}
with BlockErrors(err_types):
    a = 1 / '0'  # Любое исключение будет проигнорировано
print('Выполнено без ошибок')
EOF