# Программа клиента для отправки приветствия серверу и получения ответа
import argparse
from socket import *
import json
import sys
import time
from threading import Thread
import uuid

#from Log.client_log_config import *

# Обратите внимание, логгер уже создан в модуле log_config,
# теперь нужно его просто получить
#logger = logging.getLogger('client.main')

PORT1 = 8000
PORT2 = 8001

message_from_client = {
        "action": "presence",
        "user": {
                "guid":  None,
                "unique_code": None,
                "password": None },
        "message": ""
}

#def read_thread(sock):
#    while True:
        # необходимо сделать поток на чтение!
#        try:
#            data = sock.recv(1024)
#            response = json.loads(data.decode('utf-8'))
#            if int(response["response"]) == 200:
#                print('\t\t\t\t'+response["alert"])
#        except:
#            pass



def write_thread(sock):
    while True:
        # необходимо сделать поток на запись!
        key = input('message - key [1], exit - key [2]: ')
        if key == '2':
            message_from_client['action'] = "logout"
            sock.send(json.dumps(message_from_client).encode())
            break
        if key == '1':
            msg = input('Input your message: ')
        else:
            continue
        message_from_client['action'] = "message"
        message_from_client['message'] = msg
        message_from_client['password'] = "" #очищаем поле пароля для следующих пакетов по порту 8001

        sock.send(json.dumps(message_from_client).encode())


def echo_client(addr, port1, port2):

    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock: # Создать сокет TCP
        sock.connect((addr, port1))   # Соединиться с сервером
        user = uuid.uuid1()
        while True:
            password = input('Input server password: ')
            message_from_client["user"]["guid"] = str(user)
            message_from_client["user"]["password"] = password
            message_from_client['action'] = "presence"

            sock.send(json.dumps(message_from_client).encode())
            data = sock.recv(1024)
            response = json.loads(data.decode('utf-8'))
            print(f"Hello, I am the server {addr}")
            print(response["alert"])
            if int(response["response"]) == 200:
                code = response["alert"]
                message_from_client["user"]["unique_code"] = code
                with socket(AF_INET, SOCK_STREAM) as sock2:  # Создать сокет TCP
                    sock2.connect((addr, port2))  # Соединиться с сервером по другому порту
                    write_thread(sock2)
                    time.sleep(10)
                    break


if __name__ == '__main__':
#    logger.info('Запуск клиента-------------------------------------------------------------')
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='addr', action='store', type=str, required=False, help='IP-address', default='localhost')
    args = parser.parse_args(sys.argv[1:])

    print("адрес сервера: ", args.addr)
    echo_client(args.addr, PORT1, PORT2)


