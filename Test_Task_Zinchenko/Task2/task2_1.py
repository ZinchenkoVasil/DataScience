# -*- coding: utf-8 -*-
"""Task2_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xLR6awafSm18zqDz-f6jE9771AQBMqFM
"""

!pip install pymorphy2

!pip install stop_words

import re
import string
import pandas as pd
import pymorphy2
from stop_words import get_stop_words 
import numpy as np

df = pd.read_excel('./sample_data/Incidents.xlsx')

df['Контент'].head(10).reset_index()

"""Обработка данных"""

len(df['Тема'].unique())

df2 = pd.Series(df['Тема'].unique()).reset_index()
df2.columns = ['index_subject','Тема']
df2

df = df.merge(df2, on='Тема')

df.head()

#вычисление target label (выходных меток для обучения)
#61 класс
labels = np.array(df['index_subject'])

sw = set(get_stop_words("ru"))
stpwrds = list(sw) + list(string.punctuation)

morph = pymorphy2.MorphAnalyzer()

corpus = []
# регулярка для поиска слов
regular_expr = r'\w+'
reg_expr_compiled = re.compile(regular_expr)

for raw_text in df['Контент'].values:
    # приводим к нижнему регистру
    # разбиваем текст на слова
    text_by_words = reg_expr_compiled.findall(raw_text)
    raw_text = [i for i in text_by_words if i not in stpwrds]
    raw_text_lower = [morph.parse(i.lower())[0].normal_form for i in raw_text]
    corpus.append(" ".join([i for i in raw_text_lower]))
print(corpus[1])

texts = corpus
len(texts)

"""Конструирование нейронной сети"""

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

maxlen = 100
training_samples = 7000
validation_samples = 3607
max_words = 10000

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=maxlen)

labels = np.asarray(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

x_train = data[:training_samples]
y_train = labels[:training_samples]
x_val = data[training_samples: training_samples + validation_samples]
y_val = labels[training_samples: training_samples + validation_samples]

y_train = to_categorical(y_train)
y_val = to_categorical(y_val)

embedding_dim = 100

from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, Dropout
from sklearn.metrics import roc_auc_score, roc_curve

model = Sequential()
model.add(Embedding(max_words, embedding_dim, input_length=maxlen))
model.add(Flatten())
model.add(Dense(61, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(61, activation='softmax'))
model.summary()

model.compile(optimizer='rmsprop', 
             loss='categorical_crossentropy',
             metrics=['acc'])

history = model.fit(x_train, y_train,
                    epochs=5,
                    batch_size=32,
                    validation_data=(x_val, y_val))

import matplotlib.pyplot as plt

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(loss) + 1)

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

plt.clf()
acc = history.history['acc']
val_acc = history.history['val_acc']

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation acc')
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()

plt.show()

"""Вывод: в случае случайного выбора темы точность случайного классификатора была бы 1/60 (всего 61 класс). Получившаяся точность - 0.3. Это в 20 раз лучше случайного.  """

y_hat = model.predict_proba(x_val)

y_hat.shape

y_val.shape

"""Вычислим ROC AUC по теме "Строительство" (класс 0)"""

y_hat[:,0]

pct_auc = roc_auc_score(y_val[:,0], y_hat[:,0])*100
print("ROC AUC по теме 'Строительство': ", pct_auc)

"""Вывод: получился хороший результат 79%, в случае случайного классификатора площадь под кривой AUC была бы 50%.  """

class_message = list(df2["Тема"])
roc_auc = []
for i in range(50):
    pct_auc = roc_auc_score(y_val[:,i], y_hat[:,i])*100
    print(f"ROC AUC по теме '{class_message[i]}': {pct_auc}")
    roc_auc.append(pct_auc)

#определить предсказанные темы 
#в данном случае нет тестового файла поэтому возьмем исходный файл
class_message = list(df2["Тема"])
doc_ids = list(df["ID"])
predictions = []
ids = []
for i in range(len(df)):
    try:
        n = np.argmax(y_val[i,:])
        pred_class_message =  class_message[n]
        predictions.append(pred_class_message)
        ids.append(doc_ids[i])
    except:
        n = 0
      
result_df = pd.DataFrame({
    'ID': ids,
    'Тема': predictions
})  
result_df

"""2 часть задания:
выявить, в каких обращениях упоминается ФИО (имена, фамилии) и сколько раз;
В этом задании надо найти ФИО. Используя регулярные выражения можно найти все слова, начинающиеся с заглавных букв
"""

df = pd.read_excel('sample_data/Incidents.xlsx')

df['Контент'].head(10).reset_index()

def search_names(raw_text, reg_expr):
# регулярка
    words = [] 
# компилируем регулярное выражение
    reg_expr_compiled = re.compile(reg_expr)
    for word in list(reg_expr_compiled.findall(raw_text)):
        word = word[2:]
        words.append(word)
    return words

# регулярка
reg_expr = r'[A-Я][а-я]+ [A-Я][а-я]+'
# компилируем регулярное выражение
reg_expr_compiled = re.compile(reg_expr)

for raw_text in df['Контент'].values:
# применяем выражение к тексту
    for g in reg_expr_compiled.findall(raw_text):
        print(g)

# регулярка
reg_expr = r'[A-Я][а-я]+ [A-Я][а-я]+ [A-Я][а-я]+'
# компилируем регулярное выражение
reg_expr_compiled = re.compile(reg_expr)

for raw_text in df['Контент'].values:
# применяем выражение к тексту
    for g in reg_expr_compiled.findall(raw_text):
        print(g)

df['1_спец_слово'] = df.apply(lambda x: search_names(x['Контент'], r'[^(.&!&?)] [A-Я][а-я]+'),axis=1)
df['2_подряд_спец_слова'] = df.apply(lambda x: search_names(x['Контент'], r'[^(.&!&?)] [A-Я][а-я]+ [A-Я][а-я]+'),axis=1)
df['3_подряд_спец_слова'] = df.apply(lambda x: search_names(x['Контент'], r'[^(.&!&?)] [A-Я][а-я]+ [A-Я][а-я]+ [A-Я][а-я]+'),axis=1)

df[['1_спец_слово', '2_подряд_спец_слова', '3_подряд_спец_слова']].head(20)

"""Примечание: спец слово - слово с заглавной буквой."""

df[['1_спец_слово']].values[0]

"""выявить географические наименования в каждой тематике и ранжировать"""

#в данной задаче опять можно прибегнуть к такому же способу. Можно найти с помощью регулярки все слова с заглавными буквами. 
def get_names(df, reg_expr = r'[^(.&!&?)] [A-Я][а-я]+'):
    spec_words = {}
    for raw_text in df['Контент'].values:
        reg_expr_compiled = re.compile(reg_expr)
        for word in list(reg_expr_compiled.findall(raw_text)):
            word = word[2:]
            if word in spec_words:
                spec_words[word] += 1
            else:
                spec_words[word] = 1
    #ранжировать по частоте встречаемости    
    result_df = pd.DataFrame({
    'Спец_слово': spec_words.keys(),
    'Частота встречаемости': spec_words.values()})     
    return result_df.sort_values(by='Частота встречаемости', ascending=False)

df_groupby_class = df.groupby(['Тема']).apply(get_names) 
df_groupby_class

#в данной задаче опять можно прибегнуть к такому же способу. Можно найти с помощью регулярки все слова с заглавными буквами. 
def get_names2(df, reg_expr = r'[^(.&!&?)] [A-Я][а-я]+'):
    spec_words = {}
    for raw_text in df['Контент'].values:
        reg_expr_compiled = re.compile(reg_expr)
        for word in list(reg_expr_compiled.findall(raw_text)):
            word = word[2:]
            if word in spec_words:
                spec_words[word] += 1
            else:
                spec_words[word] = 1
    #ранжировать по частоте встречаемости    
    result_df = pd.DataFrame({
    'Спец_слово': spec_words.keys(),
    'Частота встречаемости': spec_words.values()})     
    return list(result_df.sort_values(by='Частота встречаемости', ascending=False)['Спец_слово'].values)

df_groupby_class = df.groupby(['Тема']).apply(get_names2).reset_index() 
df_groupby_class.columns = ['Тема','Список спец_слов']
df_groupby_class

list(df_groupby_class[df_groupby_class['Тема'] == 'Архитектура и строительство']['Список спец_слов'])#.values[0]

