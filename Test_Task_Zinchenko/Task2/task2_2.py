# -*- coding: utf-8 -*-
"""Task2_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fq1Vw9gvAXrmbgcAwJ0SgzBonZUeFQ10
"""

import re
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.metrics import f1_score as f1
from sklearn.metrics import roc_auc_score, roc_curve
import missingno as msno
from sklearn.model_selection import train_test_split

df = pd.read_excel('sample_data/Data_sent06.xls')

df.head(10)

"""Обработка данных"""

df.columns

df[['18-19','20-24','25-29','30-34','35-39']] = pd.get_dummies(df['age'])

#удаляем старое поле
features_to_drop = []
features_to_drop.append('age')

df[['вдова','гражд_брак','замужем','не замужем','разведена']] = pd.get_dummies(df['married'])

features_to_drop.append('married')

df[['да','нет','трудно сказать']] = pd.get_dummies(df['plan_married'])

features_to_drop.append('plan_married')

#нейронка лучше кушает нормализованные величины от 0 до 1
df['childrens_fact'] = df['childrens_fact'] / 5

#нейронка лучше кушает нормализованные величины от 0 до 1
df['important_cash'] = df['important_cash'] / 5

#нейронка лучше кушает нормализованные величины от 0 до 1
df['important_rest'] = df['important_rest'] / 5

#нейронка лучше кушает нормализованные величины от 0 до 1
df['important_children'] = df['important_children'] / 5

#нейронка лучше кушает нормализованные величины от 0 до 1
df['important_educ'] = df['important_educ'] / 5

#нейронка лучше кушает нормализованные величины от 0 до 1
df['important_intim'] = df['important_intim'] / 5

df[['chilpdren_plan0', 'chilpdren_plan1', 'chilpdren_plan2', 'chilpdren_plan3', 'chilpdren_plan4', 'chilpdren_plan5', 'chilpdren_plan6', 'chilpdren_plan7']] = pd.get_dummies(df['chilpdren_plan'])
features_to_drop.append('chilpdren_plan')

df[['ideal_family0','ideal_family1','ideal_family2','ideal_family3','ideal_family4','ideal_family5','ideal_family6']] = pd.get_dummies(df['ideal_family'])
features_to_drop.append('ideal_family')

df[['children_plan2_0', 'children_plan2_1', 'children_plan2_2', 'children_plan2_3', 'children_plan2_4', 'children_plan2_5', 'children_plan2_6']] = pd.get_dummies(df['children_plan2'])
features_to_drop.append('children_plan2')

df[['plan_living_останутся прежними,неудовлетворительными','plan_living_станут лучше','plan_living_станут хуже','plan_living_трудно сказать']] = pd.get_dummies(df['plan_living'])
features_to_drop.append('plan_living')

df[['plan_cash_останется прежним, вполне приемлемым','plan_cash_останeтся прежними,неудовлетворительным','plan_cash_станет лучше','plan_cash_станет хуже','plan_cash_трудно сказать']] = pd.get_dummies(df['plan_cash'])
features_to_drop.append('plan_cash')

df[['plan_climat_останется прежним, вполне приемлемым','plan_climat_останeтся прежними,неудовлетворительным','plan_climat_станет лучше','plan_climat_станет хуже','plan_climat_трудно сказать']] = pd.get_dummies(df['plan_climat'])
features_to_drop.append('plan_climat')

df[['plan_economy_останется прежним, вполне приемлемым','plan_economy_останeтся прежними,неудовлетворительным','plan_economy_станет лучше','plan_economy_станет хуже','plan_economy_трудно сказать']] = pd.get_dummies(df['plan_economy'])
features_to_drop.append('plan_economy')

df[['plan_politic_останется прежним, вполне приемлемым','plan_politic_останeтся прежними,неудовлетворительным','plan_politic_станет лучше','plan_politic_станет хуже','plan_politic_трудно сказать']] = pd.get_dummies(df['plan_politic'])
features_to_drop.append('plan_politic')

df[['plan_support_gov_останется прежним, вполне приемлемым','plan_support_gov_останeтся прежними,неудовлетворительным','plan_support_gov_станет лучше','plan_support_gov_станет хуже','plan_support_gov_трудно сказать']] = pd.get_dummies(df['plan_support_gov'])
features_to_drop.append('plan_support_gov')

df[['высш_незак_высш','нач_неполн_ср','среднее']] = pd.get_dummies(df['education'])
features_to_drop.append('education')

df[['occupation1','occupation2','occupation3','occupation4','occupation5','occupation6','occupation7','occupation8','occupation9','occupation10','occupation11','occupation12','occupation13','occupation14']] = pd.get_dummies(df['occupation'])
features_to_drop.append('occupation')

df[['income1','income2','income3','income4','income5']] = pd.get_dummies(df['income'])
features_to_drop.append('income')

df[['квартира','комната','общежитие']] = pd.get_dummies(df['living_conditions'])
features_to_drop.append('living_conditions')

df[['religion_да','religion_нет','religion_трудно сказать']] = pd.get_dummies(df['religion'])
features_to_drop.append('religion')

df = df.drop(features_to_drop, axis=1)

df.head()

df.describe(include=[np.number])

df.describe(include=[np.object])

msno.bar(df)

df.isnull().sum()

#все пустые удаляем из набора
df = df.dropna()

df.isnull().sum()

len(df)

len(df[~df['target'].isnull()])

df = df[~df['target'].isnull()]

#вычисление target label (выходных меток для обучения)
#61 класс
labels = np.array(df['target'] == 'да')

data = df.drop('target', axis=1)

x_train, x_val = train_test_split(
    data, train_size=0.7, random_state=27, shuffle=True
)
y_train, y_val = train_test_split(
    labels, train_size=0.7, random_state=27, shuffle=True
)

"""Конструирование нейронной сети"""

labels = np.asarray(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, Dropout
from sklearn.metrics import roc_auc_score, roc_curve

model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(98,)))
#model.add(Flatten())
#model.add(Dense(16, activation='relu'))
#model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(optimizer='rmsprop', 
             loss='binary_crossentropy',
             metrics=['acc'])

history = model.fit(x_train, y_train,
                    epochs=14,
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

"""Вывод: Получившаяся точность модели (accuracy) - 0.77. Это высокая точность.  """

y_hat = model.predict_proba(x_val)

y_hat.shape

y_val.shape

"""Вычислим ROC AUC"""

y_hat[:10]

pct_auc = roc_auc_score(y_val, y_hat)*100
print("ROC AUC: ", pct_auc)

"""Вывод: получился хороший результат 78%, в случае случайного классификатора площадь под кривой AUC была бы 50%.  """

