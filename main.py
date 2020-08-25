import icmplib
from time import sleep
import subprocess
import config
import enum


class PingState(enum.Enum):
    # Начальное состояние либо сеть отвалилась
    INITIAL_STATE = enum.auto()
    # Серия успешных пингов, но батник еще не запускаем
    SUCCESS_IN_PROGRESS = enum.auto()
    # Запустили батник и мониторим сеть
    SUCCESSFUL = enum.auto()


class PingProgress:
    def __init__(self, timeouts_before_failure, timeouts_before_success):
        self.max_failed_pings = timeouts_before_failure
        self.max_successful_pings = timeouts_before_success
        self.state = PingState.INITIAL_STATE
        self.failed_pings = 0
        self.successful_pings = 0

    def on_network_up(self):
        pass

    def on_network_down(self):
        pass

    def fail(self):
        self.failed_pings += 1
        if self.failed_pings == self.max_failed_pings:  # сеть упала
            self.state = PingState.INITIAL_STATE
            self.failed_pings = 0
            self.successful_pings = 0
            self.on_network_down()

    def success(self):
        self.failed_pings = 0  # единственный успешный пинг прерывает серию фейлов

        if self.state == PingState.SUCCESS_IN_PROGRESS and self.successful_pings + 1 == self.max_successful_pings:
            # запускаем батник
            self.state = PingState.SUCCESSFUL
            self.successful_pings += 1
            self.on_network_up()
        elif self.state == PingState.SUCCESSFUL:
            pass  # ничего не делаем, с сетью и так всё ок
        else:
            self.state = PingState.SUCCESS_IN_PROGRESS
            self.successful_pings += 1


def on_network_up():
    subprocess.run(config.PROGRAM_TO_LAUNCH_ON_SUCCESS)


def main():
    # Довольно громоздкий вызов получается имхо, поэтому я параметры в словарик вытащил
    # Они всё равно не меняются сейчас
    ping_parameters = {
        'address': config.SERVER_TO_PING,
        'interval': config.INTERVAL_BETWEEN_PINGS,
        'count': 1,
        'timeout': config.TIMEOUT_SECONDS
    }
    progress = PingProgress(config.TIMEOUTS_BEFORE_FAILURE, config.TIMEOUTS_BEFORE_SUCCESS)
    progress.on_network_up = on_network_up
    while True:
        try:
            ping_result = icmplib.ping(**ping_parameters)
            if not ping_result.is_alive:
                progress.fail()
                print('Хост недоступен')
            if ping_result.received_packets == 0:
                progress.fail()
                # print('Fail')
            else:
                progress.success()
                # print('Success')
        except KeyboardInterrupt:
            print('Ctrl-C')
            break


if __name__ == '__main__':
    main()
