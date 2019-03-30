# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:27:06 2019

@author: tot
"""

from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
import apiai
import json
import pandas as pd
import time
#pprint(rocket.me().json())
#pprint(rocket.channels_list().json())
#Со сменой имени
#pprint(rocket.chat_post_message('Ну что, пацаны, хакатон?', channel='GENERAL', alias='ZDAROV').json())

#Все то же, json делает вывод лога
#pprint(rocket.chat_post_message('тест', channel='GENERAL').json())
#pprint(rocket.channels_history('GENERAL', count=5).json())

#Без вывода лога
#rocket.chat_post_message('тест', channel='GENERAL')

#for i in range(0, jsonData['ims'].length):

user_data = pd.read_excel('user_data.xlsx')
tasks = pd.read_excel('tasks.xlsx')
docs= pd.read_excel('docs.xlsx')

def textMessage(update, did):
    request = apiai.ApiAI('76084f44b01a48c2abe6a51cd63476ae').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = did # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        return response
    else:
        return 'Я Вас не совсем понял!'

class Bot:
    def __init__(self, login, password):
        self.login=login
        self.rocket = RocketChat(login, password, server_url='http://178.70.218.84:3000')
        print('Bot initialized')
        
    def updateUserData(self):
        print('Starting updating user data')
        global user_data
        user_data = pd.read_excel('user_data.xlsx')
        jsonData = self.rocket.im_list().json()
        #pprint(jsonData)
        for i in range(0, len(jsonData['ims'])):
            if not (jsonData['ims'][i]['_id'] in user_data['imid'].values):
                if (jsonData['ims'][i]['usernames'][0]=='tot'):
                    user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'admin'}, ignore_index=True)
                else:
                    user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'user'}, ignore_index=True)
                user_data.to_excel('user_data.xlsx')
        print('Finished updating user data')
    def initUserData(self):
        print('Starting initializing user data')
        user_data = pd.DataFrame(columns=['imid', 'uname', 'role'])
        jsonData = self.rocket.im_list().json()
        #pprint(jsonData)
        for i in range(0, len(jsonData['ims'])):
            if (jsonData['ims'][i]['usernames'][0]=='tot'):
                user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'admin'}, ignore_index=True)
            elif (jsonData['ims'][i]['usernames'][0]=='FeDOS'):
                user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'admin'}, ignore_index=True)
            else:
                user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'user'}, ignore_index=True)
            user_data.to_excel('user_data.xlsx')
        
        print('Finished initializing user data')
    def getLastMessage(self):
        user = self.rocket.channels_history('GENERAL', count=5).json()['messages'][0]['u']
        msg = self.rocket.channels_history('GENERAL', count=5).json()['messages'][0]['msg']
        return user, msg
    def getLastMessages(self):
        jsonData = self.rocket.im_list().json()
        tid = []
        msg = []
        text = []
        user = []
        for i in range(0, len(jsonData['ims'])):
            tid.append(jsonData['ims'][i]['_id'])
            try:     
                msg.append(jsonData['ims'][i]['lastMessage']['_id'])
            except KeyError:
                self.send('Твоей маме зять не нужен?', ch=str(tid[i]))
                jsonData = self.rocket.im_list().json()
                msg.append(jsonData['ims'][i]['lastMessage']['_id'])
            history = self.rocket.im_history(str(tid[i]), count=1).json()
            text.append(history['messages'][0]['msg'])
            user.append(history['messages'][0]['u'])
        return tid, msg, text, user
    def oldloop(self):
        while True:
            user, text = self.getLastMessage()
            text = text.lower()
            if all(c in text for c in ['привет', 'маша']):
                msg = 'Привет, '+user['name']
                self.send(msg)
            if all(c in text for c in ['отправь', 'коды запуска ракет']):
                msg = 'Извини, '+user['name']+', но ты не достоин :с'
                self.send(msg)
            
    def send(self, msg, ch='GENERAL'):
        self.rocket.chat_post_message(msg, channel=ch)
    def loop(self):
        global user_data
        global docs
        while True:
            self.updateUserData()
            tid, msg, text, user = self.getLastMessages()
            for i in range(len(tid)):
                mes = ''
                if(str(user[i]['name']).lower() == self.login.lower()): continue
                if all(c in text[i] for c in ['привет']):
                    mes = 'Привет, '+user[i]['name']
                    self.send(mes, ch=str(tid[i]))
                elif all(c in text[i] for c in ['кек']):
                    mes = 'лол'
                    self.send(msg, ch=str(tid[i]))
                elif all(c in text[i] for c in ('аригато в хату').split()):
                    mes = 'Онегай шимасу вашему шалашу'
                    self.send(mes, ch=str(tid[i]))
                elif all(c in text[i] for c in ('отправь всем').split()):
                    if (user_data.loc[user_data['uname'] == user[i]['name']]['role'].values[0]=='admin'):
                        try:
                            mes = text[i].split('\n', maxsplit=1)[1]
                            print(mes)
                            self.sendEveryone(mes)
                            self.send('Сделано!', ch=str(tid[i]))
                        except:
                            self.send('Знаешь, ты изменился...', ch=str(tid[i]))
                    else:
                        self.send('Вы не админ', ch=str(tid[i]))
                elif all(c in text[i] for c in ('инициализируй базу').split()):
                    self.initUserData()
                    self.send('Сделано!', ch=str(tid[i]))
                elif all(c in text[i] for c in ('контакты').split()):
                    self.send('https://www.rosatom.ru/about/contact-info/', ch=str(tid[i]))
                elif all(c in text[i] for c in ('кадровая политика').split()):
                    self.send('https://www.rosatom.ru/career/sotrudnikam/kadrovaya-politika/', ch=str(tid[i]))
                elif any(c in text[i] for c in ('найти', 'найди', 'поиск').split()):
                    mes = text[i].split('\n', maxsplit=1)[1]
                    self.send(docs.loc[mes in docs['docname']], ch=str(tid[i]))
                else:
                    self.send(textMessage(text[i], tid[i]), ch=str(tid[i]))
    def sendEveryone(self, txt):
        tid, msg, text, user = self.getLastMessages()
        for i in range(len(tid)):
            self.send(txt, ch=str(tid[i]))
    def setTask(self, imid, task, time):
        
        pass
    def setRole(self, uname, role):
        global user_data
        print(user_data.loc[user_data['uname'] == uname].index.values[0])
        user_data.at[str(user_data.loc[user_data['uname'] == uname].index.values[0]), 'role'] = role
        user_data.to_excel('user_data.xlsx')
        self.updateUserData()
        

            
    
tot = Bot('tot_bot', '2128506q')
tot.loop()
