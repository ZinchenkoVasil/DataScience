#ответ сервера на запрос установления соединения
from decorators import *
import uuid
import json
import datetime
import os


PASSWORD = 'Admin'
OUT_DIR = 'Messages_from_Clients'

user_dict = {}
messages = []

# function to add to JSON
def write_txt(new_data, filename='Messages.txt'):
    OUT_FILENAME = OUT_DIR + os.sep + filename
    fout = open(OUT_FILENAME, 'a', encoding='utf-16')
    print('date:', new_data["date"], file=fout, sep='\n')
    print('message:',new_data['message'], file=fout, sep='\n')
    fout.close()


@log
def get_response(guid, password, data):
    if password == PASSWORD:
        code = str(uuid.uuid4())
        user_dict[guid] = str(code)
        code_error = 200
        return code_error, code
    else:
        code_error = 401
        code = "The password is incorrect!"
        return code_error, code


@log
def get_message(guid, unique_code, data):
    message = {}
    #если гуид и код есть в нашем словаре, то запись в БД
    if guid in user_dict:
        code_ = user_dict[guid]
        if unique_code == code_:
            message['message'] = data
            message['date'] = datetime.datetime.today()
            write_txt(message)
            code_error = 200
            return code_error, data
        else:
            code_error = 401
            return code_error, "The unique code is incorrect!"
    code_error = 401
    return code_error, "The user guid is incorrect!"


@log
def log_out(account_name, unique_code, data):
    if guid in user_dict:
        code_ = user_dict[guid]
        if unique_code == code_:
            user_dict[guid] = ""

    return None


