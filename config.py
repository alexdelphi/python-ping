# Какой сервер пингуем
SERVER_TO_PING = 'google.com'
# Количество секунд, в течении которых пинг ждет ответ
TIMEOUT_SECONDS = 1
# Количество таймаутов подряд, которое считается за отвал сети
TIMEOUTS_BEFORE_FAILURE = 8
# Количество успешных пингов подряд, которое считается за нормальную работу сети
TIMEOUTS_BEFORE_SUCCESS = 1
# Интервал пинга в секундах
INTERVAL_BETWEEN_PINGS = 1
# Батник, который запускается при успехе
PROGRAM_TO_LAUNCH_ON_SUCCESS = r"D:\temp\hello.bat"
