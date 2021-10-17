# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import json
import sys
import argparse
from Server.text import routes

import logging
import Log.server_log_config

# Обратите внимание, логгер уже создан в модуле log_config,
# теперь нужно его просто получить
logger = logging.getLogger('server.main')
logger.info('Запуск сервера-------------------------------------------------------------')

parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='addr', action='store', type=str, required=False, help='IP-address', default='')
parser.add_argument('-p', dest='port', action='store', type=int, required=False, help='Port', default=7777)
args = parser.parse_args(sys.argv[1:])
s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
logger.debug("Создает сокет TCP")
s.bind((args.addr, args.port))                # Присваивает порт
logger.debug("Присваивает порт")
s.listen(5)                       # Переходит в режим ожидания запросов;
logger.debug("Переходит в режим ожидания запросов")
response_dict = {}                                  # Одновременно обслуживает не более                                  # 5 запросов.
while True:
    client, addr = s.accept()
    logger.debug("сервер принял запрос на соединение от клиента")
    data = client.recv(1000000)
    logger.debug("сервер принял сообщение от клиента")
    request = json.loads(data.decode())
    logger.debug("парсинг сообщения от клиента")
    client_action = request.get('action')
    resolved_routes = list(
        filter(
            lambda itm: itm.get('action') == client_action, routes))
    route = resolved_routes[0] if resolved_routes else None
    if route:
        controller = route.get('controller')
        if "user" in request:
            user = request.get('user')
            response_string = controller(user['account_name'])
        else:
            response_string = controller('')
        response_dict['response'] = 200
        response_dict['alert'] = response_string
    else:
        response_dict['response'] = 401
        response_dict['alert'] = "Action don't support"
        logger.error("Action don't support")
        logger.error("клиент работает по неизвестному протоколу!")
    logger.debug("сервер посылает ответ клиенту")
    try:
        client.send(json.dumps(response_dict).encode())
        logger.debug("сервер послал ссобщение клиенту")
    except:
        logger.critical("Невозможно послать сообщение клиенту! Возможно клиент разорвал соединение.")
    data = client.recv(1000000)
    logger.debug("сервер принял новое сообщение от клиента")
    request = json.loads(data.decode())
    logger.debug("парсинг сообщения от клиента")
    client_action = request.get('action')
    if client_action == "quit":
        logger.debug("клиент послал запрос на завершения сеанса")
        client.close()
        logger.debug("сеанс работы с клиентом завершен")