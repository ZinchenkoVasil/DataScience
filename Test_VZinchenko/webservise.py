from flask import Flask, request, jsonify
from test_task_mmk import get_paraphrase_classes


app = Flask(__name__)


@app.route('/get_paraphrase_classes/', methods=['POST'])
def num_text():
    json_data = request.get_json()
    # Проверяем наличие необходимого ключа в запросе
    if 'phrase1' not in json_data:
        return jsonify(str='The key phrase1 doesn`t exist')
    if 'phrase2' not in json_data:
        return jsonify(str='The key phrase2 doesn`t exist')

    # Достаем пришедшие данные из запроса
    phrase1 = json_data['phrase1']
    phrase2 = json_data['phrase2']
    # Начало блока по обработке пришедших данных. Здесь пишем свой код
    # Конеч блока обработки данных
    paraphrase_class = get_paraphrase_classes(phrase1, phrase2)
    if paraphrase_class:
        text = "свободные или строгие перефразы"
    else:
        text = 'не являются перефразами'
    return jsonify(str=text)


if __name__ == '__main__':
    app.run(debug=True)
