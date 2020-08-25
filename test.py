"""
Суть теста:
Метод ping() подменяется таким образом, что он ходит по заданной строке.
Если в данной строке стоит 1 - пинг прошел ок
Если 0 - пинг отвалился по таймауту
Если D - хост недоступен
"""

import icmplib
import main
import config


class MockPing:
    # имитируем ответ от пинга
    def __init__(self, is_alive, sent_packets, received_packets):
        self.is_alive = is_alive
        self.sent_packets = sent_packets
        self.received_packets = received_packets


class Pinger:
    def __init__(self, ping_series):
        self.ping_series = ping_series
        self.counter = 0

    def __call__(self, *args, **kwargs):
        # Моделируем системный пинг
        if self.counter == len(self.ping_series):  # остановка теста
            response = None
        elif self.ping_series[self.counter] == '1':  # пинг прошел
            response = MockPing(is_alive=True, sent_packets=1, received_packets=1)
        elif self.ping_series[self.counter] == '0':  # пинг не прошел
            response = MockPing(is_alive=True, sent_packets=1, received_packets=0)
        elif self.ping_series[self.counter] == 'D':  # хост отвалился
            response = MockPing(is_alive=False, sent_packets=1, received_packets=0)
        self.counter += 1
        return response


def launch_test(ping_series):
    icmplib.ping = Pinger(ping_series)
    try:
        main.main()
    except AttributeError:  # 'NoneType' object has no attribute 'is_alive'
        pass  # остановка программы


def entry():
    config.TIMEOUTS_BEFORE_SUCCESS = 4
    config.TIMEOUTS_BEFORE_FAILURE = 6
    config.PROGRAM_TO_LAUNCH_ON_SUCCESS = R'cmd /c echo Hello World!'
    print('Тест № 1\n-----')
    launch_test('111000001')  # должен напечатать "Hello World!"
    print()
    print('Тест № 2\n-----')
    launch_test('11100000001')  # должен не напечатать ничего
    print()
    print('Тест № 3\n-----')
    launch_test('1D')  # должен напечатать "Хост недоступен"
    print()


if __name__ == '__main__':
    entry()
