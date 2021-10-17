# Программа клиента для отправки приветствия серверу и получения ответа
from socket import *
import json
import sys
import time

from Log.client_log_config import *

# Обратите внимание, логгер уже создан в модуле log_config,
# теперь нужно его просто получить
#logger = logging.getLogger('client.main')

message_from_client = {
        "action": "presence",
        "time": "",
        "type": "status",
        "user": {
                "account_name":  "Vasia",
                "status":      "Yep, I am here!"
        }
}

quit_session = {
    "action": "quit"
}

try:
    addr = sys.argv[1]
except IndexError:
    addr = 'localhost'

try:
    port  = int(sys.argv[2])
except:
    port = 7777

logger.info('Запуск клиента-------------------------------------------------------------')

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
logger.debug("Создать сокет TCP")
try:
    s.connect((addr, port))   # Соединиться с сервером
    logger.debug("Соединиться с сервером")
    message_from_client['time'] = time.ctime(time.time())
    s.send(json.dumps(message_from_client).encode())
    logger.debug("Послали сообщение серверу")
    data = s.recv(1000000)
    logger.debug("Приняли сообщение от сервера")
    response = json.loads(data.decode('utf-8'))
    if int(response["response"]) == 200:
        print("OK")
    print(response["alert"])
    s.send(json.dumps(quit_session).encode())
    logger.debug("Послали серверу на закрытие соединения")
except:
    logger.critical('You can not connect with server! No address was supplied.')
s.close()
