import time
from threading import Thread, Event

class Check:
    def __init__(self):
        self.event = Event()  # Создаем событие
        self.event.set()      # Устанавливаем событие в состояние "разрешено"

    def start(self):
        for row in range(1, 1001):  # Печатаем числа от 1 до 1000
            print(row)
            self.event.wait()  # Ожидаем, пока событие установлено
            time.sleep(1)      # Задержка 1 секунда

    def pause(self):
        self.event.clear()  # Устанавливаем событие в состояние "приостановлено"

    def resume(self):
        self.event.set()    # Устанавливаем событие в состояние "разрешено"

# Словарь для хранения потоков
threads = {}
check = Check()  # Создаем экземпляр класса Check
c = Thread(target=check.start)  # Создаем поток для выполнения метода start
c.start()  # Запускаем поток
threads['1'] = check  # Сохраняем экземпляр Check в словаре

print("Поток запущен. Введите 'pause' для паузы и 'resume' для возобновления.")

while True:
    command = input(': ')  # Ожидаем ввода команды
    if command == 'pause':
        threads['1'].pause()  # Приостанавливаем выполнение
        print("Выполнение приостановлено.")
    elif command == 'resume':
        threads['1'].resume()  # Возобновляем выполнение
        print("Выполнение возобновлено.")
    elif command == 'exit':
        break  # Выход из цикла
