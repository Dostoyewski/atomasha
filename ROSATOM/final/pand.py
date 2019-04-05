# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:29:39 2019

@author: Федор
"""

import pandas as pd



udata = pd.read_excel('user_data.xlsx')
#names = ''
#for i in range(0, len(udata['uname'])):
#    names += udata['uname'][i] + ' '
#    
#print(names)
#user_data = pd.DataFrame(columns=names.split())
#user_data.to_excel('conduit.xlsx')
user_data = pd.read_excel('conduit.xlsx')
fail = 0
for i in range(0, len(user_data['FeDOS'])):
    if(user_data['FeDOS'][i] == 0):
        fail += 1
print(fail)
m = ''
s = ''
num = []
mes = 'FeDOS'
for i in range(0, len(udata['uname'])):
    if(mes.lower() in udata['uname'][i].lower()):
        m += udata['uname'][i].lower() +'\n'
        num.append(i)
        if(udata['state'][i] == 0):
            s = 'Отсутсвует'
        else:
            s = 'Присутствует'
if(m != ''):
    print('Вот что я нашла:\n')
    print('Имя: ' + udata['uname'][num[0]] + '\n')
    print('Зарплата: ' + str(udata['salary'][num[0]]) + '\n')
    print('Должность: ' + udata['position'][num[0]] + '\n')
    print('Статус: ' + s + '\n')
else:
    print('Я ничего не нашла. Запрос может быть некорректен.')
    