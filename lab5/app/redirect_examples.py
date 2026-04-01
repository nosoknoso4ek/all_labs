from redirect_output import Redirect, RedirectStringIO
import sys
import io


def example_1_basic():
    """Пример 1: Перенаправление stdout в файл"""
    print("\n" + "="*50)
    print("Пример 1: Перенаправление stdout в файл")
    print("="*50)
    
    with open('stdout.txt', 'w') as f:
        with Redirect(stdout=f):
            print("Это сообщение попадет в файл stdout.txt")
    
    print("Это сообщение в консоль")
    
    # Показываем содержимое файла
    with open('stdout.txt', 'r') as f:
        print(f"Содержимое stdout.txt: {f.read()}")


def example_2_stderr():
    """Пример 2: Перенаправление stderr в файл"""
    print("\n" + "="*50)
    print("Пример 2: Перенаправление stderr в файл")
    print("="*50)
    
    with open('stderr.txt', 'w') as f:
        with Redirect(stderr=f):
            sys.stderr.write("Это сообщение попадет в файл stderr.txt\n")
    
    sys.stderr.write("Это сообщение в консоль\n")
    
    with open('stderr.txt', 'r') as f:
        print(f"Содержимое stderr.txt: {f.read()}")


def example_3_both():
    """Пример 3: Перенаправление обоих потоков"""
    print("\n" + "="*50)
    print("Пример 3: Перенаправление обоих потоков")
    print("="*50)
    
    with open('both_stdout.txt', 'w') as stdout_f, open('both_stderr.txt', 'w') as stderr_f:
        with Redirect(stdout=stdout_f, stderr=stderr_f):
            print("Это в stdout файл")
            sys.stderr.write("Это в stderr файл\n")
    
    print("Вывод в консоль после контекста")


def example_4_exception():
    """Пример 4: Исключение внутри контекста"""
    print("\n" + "="*50)
    print("Пример 4: Исключение внутри контекста")
    print("="*50)
    
    with open('exception_stderr.txt', 'w') as f:
        try:
            with Redirect(stderr=f):
                raise ValueError("Это исключение попадет в файл")
        except ValueError:
            print("Исключение перехвачено")
    
    with open('exception_stderr.txt', 'r') as f:
        print(f"Содержимое файла с ошибкой:\n{f.read()}")


def example_5_stringio():
    """Пример 5: Использование StringIO для захвата вывода"""
    print("\n" + "="*50)
    print("Пример 5: Использование StringIO для захвата вывода")
    print("="*50)
    
    with RedirectStringIO() as redirect:
        print("Это сообщение будет захвачено")
        print("И это тоже")
        sys.stderr.write("И это сообщение об ошибке\n")
    
    print(f"Захваченный stdout:\n{redirect.get_stdout()}")
    print(f"Захваченный stderr:\n{redirect.get_stderr()}")


def example_6_nested():
    """Пример 6: Вложенные перенаправления"""
    print("\n" + "="*50)
    print("Пример 6: Вложенные перенаправления")
    print("="*50)
    
    outer_buffer = io.StringIO()
    inner_buffer = io.StringIO()
    
    with Redirect(stdout=outer_buffer):
        print("Внешний уровень")
        
        with Redirect(stdout=inner_buffer):
            print("Внутренний уровень")
        
        print("Снова внешний уровень")
    
    print("Внешний буфер:")
    print(outer_buffer.getvalue())
    print("Внутренний буфер:")
    print(inner_buffer.getvalue())


if __name__ == '__main__':
    example_1_basic()
    example_2_stderr()
    example_3_both()
    example_4_exception()
    example_5_stringio()
    example_6_nested()