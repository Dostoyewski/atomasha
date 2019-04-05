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
import datetime
import time
import bs4 as bs4
import requests
import sqlite3

global answer
global file
file = 'data.db'

conn = sqlite3.connect(file)
cursor = conn.cursor()
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
        self.rocket = RocketChat(login, password, server_url='http://172.20.10.2:3000')
        self.connectMQTT()
        print('Bot initialized')
        
    def updateUserData(self):
        print('Starting updating user data')
        global user_data
        user_data = pd.read_excel('user_data.xlsx')
        jsonData = self.rocket.im_list().json()
        #pprint(jsonData)
        for i in range(0, len(jsonData['ims'])):
            if not (jsonData['ims'][i]['_id'] in user_data['imid'].values):
                if (jsonData['ims'][i]['usernames'][0]=='tot' or jsonData['ims'][i]['usernames'][0]=='FeDOS'):
                    user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'admin'}, ignore_index=True)
                    #onload([jsonData['ims'][i]['_id'], jsonData['ims'][i]['usernames'][0]], 'admin')
                else:
                    user_data = user_data.append({'imid': jsonData['ims'][i]['_id'], 'uname': jsonData['ims'][i]['usernames'][0], 'role': 'user'}, ignore_index=True)
                    #onload([jsonData['ims'][i]['_id'], jsonData['ims'][i]['usernames'][0]], 'user')
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
                    
                elif all(c in text[i] for c in ('отправь всем').split()):
                    print(user_data, user[i]['username'])
                    if (user_data.loc[user_data['uname'] == user[i]['username']]['role'].values[0]=='admin'):
                        rr = print(search(user[i]['username']))
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
                
                elif all(c in text[i] for c in ('статистика').split()):
                    print('Получен запрос на статистику')
                    try:
                        mes = text[i].split('\n', maxsplit=1)[1]
                    except:
                        pass
                    print(user_data, user[i]['username'])
                    if (user_data.loc[user_data['uname'] == user[i]['username']]['role'].values[0]=='admin'):
                        try:
                            conduit = pd.read_excel('conduit.xlsx')
                            fail = 0
                            for i in range(0, len(conduit[mes])):
                                if(conduit[mes][i] == 0):
                                    fail += 1
                            print(fail)
                            self.send('Статистика: \n' + 'Количество пропусков: ' + fail,  ch=str(tid[i]))
                        except:
                            self.send('Знаешь, ты изменился...', ch=str(tid[i]))
                    else:
                        conduit = pd.read_excel('conduit.xlsx')
                        fail = 0
                        mes = user[i]['username']
                        for jj in range(0, len(conduit[mes])):
                            if(conduit[mes][jj] == 0):
                                fail += 1
                        print(fail)
                        self.send('Статистика: \n' + 'Количество пропусков: ' + str(fail),  ch=str(tid[i]))
                    
                elif any(c in text[i] for c in ('найти найди поиск').split()):
                    mes = text[i].split('\n', maxsplit=1)[1]
                    print(docs.loc[docs['docname'] == mes].values)
                    m = ''
                    for doc in docs.values:
                        if(mes.lower() in doc[0].lower()):
                            m += doc[0] +'\n'
                    if(m != ''):
                        self.send('Вот что я нашла:\n'+m, ch=str(tid[i]))
                    else:
                        self.send('Я ничего не нашла. Запрос может быть некорректен.', ch=str(tid[i]))
                        
                elif any(c in text[i] for c in ('Информация Скажи').split()):
                    mes = text[i].split('\n', maxsplit=1)[1]
                    udata = pd.read_excel('user_data.xlsx')
                    m = ''
                    s = ''
                    a = ''
                    num = []
                    for az in range(0, len(udata['uname'])):
                        if(mes.lower() in udata['uname'][az].lower()):
                            m += udata['uname'][az].lower() +'\n'
                            num.append(az)
                            if(udata['state'][az] == 0):
                                s = 'Отсутсвует'
                            else:
                                s = 'Присутствует'
                    if(m != ''):
                        self.send('Вот что я нашла:\n' + 'Имя: ' + udata['uname'][num[0]] + '\n' + 
                              'Зарплата: ' + str(udata['salary'][num[0]]) + '\n' +
                              'Должность: ' + udata['position'][num[0]] + '\n' +
                              'Статус: ' + s + '\n', ch=str(tid[i]))
                        
                    else:
                        self.send('Я ничего не нашла. Запрос может быть некорректен.', ch=str(tid[i]))
                    
                elif any(c in text[i] for c in ('погода погоды погоде').split()):
                    self.send(get_weather(), ch=str(tid[i]))
                    
                elif any(c in text[i] for c in ('задание напоминание').split()):
                    print('Получен запрос на создание напоминания')
                    name =  text[i].split('\n', maxsplit=3)[1]
                    date = text[i].split('\n', maxsplit=3)[2]
                    mes = text[i].split('\n', maxsplit=3)[3]
                    print(name, date, mes)
                    self.setTask(name, mes, date)
                    self.send('Сделано!', ch=str(tid[i]))
                else:
                    self.send(textMessage(text[i], tid[i]), ch=str(tid[i]))
                self.checkTask(user[i]['name'], tid[i])
                
                
                    
    def sendEveryone(self, txt):
        tid, msg, text, user = self.getLastMessages()
        for i in range(len(tid)):
            self.send(txt, ch=str(tid[i]))
    def setTask(self, username, task, date):
        global tasks
        print('Adding task...')
        tasks = tasks.append(pd.DataFrame([[username, task, date]], columns=['username','task', 'time']), ignore_index=True)
        tasks.to_excel('tasks.xlsx')
        print('Finished!')
        pass
    def checkTask(self, name, tid):
        global tasks
        now = datetime.date.today()
        n =  str(now).split('-')
        n.reverse()
        for task in tasks.loc[tasks['username'] == name].values:
            if (task[2]=='.'.join(n)):
                self.send('Напоминание:\n'+task[1], ch=tid)
        
    def setRole(self, uname, role):
        global user_data
        print(user_data.loc[user_data['uname'] == uname].index.values[0])
        user_data.at[str(user_data.loc[user_data['uname'] == uname].index.values[0]), 'role'] = role
        user_data.to_excel('user_data.xlsx')
        self.updateUserData()
        
    def connectMQTT(self):
        import paho.mqtt.client as mqtt
        broker="sandbox.rightech.io"
        clientID = "cardid2"
        userd = {"login": "admin", "pw": "admin"}
        
        def on_connect(client, userdata, flags, rc):
            if rc==0:
                client.connected_flag=True 
                print("Bot connected OK")
                #client.publish("rb_online", 1, qos=2)
                print("subscribing ")
                client.subscribe("cid")
            else:
                print("Bad connection Returned code=",rc)
                
                
        def on_disconnect(client, userdata, rc):
            #client.publish("rb_online", 0, qos=2)
            print("Disconnected")
        
        def on_publish(client, userdata, rc):
            print("Data published")
            
        def on_message(client, userdata, message):
            #time.sleep(1)
            msg=str(message.payload.decode("utf-8"))
            print("Received message =",msg)
   
        sub = mqtt.Client(client_id=clientID)
        sub.username_pw_set(username=userd["login"],password=userd["pw"])
        sub.on_connect=on_connect 
        sub.on_disconnect=on_disconnect
        sub.on_publish = on_publish
        sub.on_message = on_message
        sub.loop_start()
        print("Connecting to broker ",broker)
        sub.connect(broker)
        
def get_weather(city: str = "санкт-петербург") -> list:
    request = requests.get("https://sinoptik.com.ru/погода-" + city)
    b = bs4.BeautifulSoup(request.text, "html.parser")
    p3 = b.select('.temperature .p3')
    weather1 = p3[0].getText()
    p4 = b.select('.temperature .p4')
    weather2 = p4[0].getText()
    p5 = b.select('.temperature .p5')
    weather3 = p5[0].getText()
    p6 = b.select('.temperature .p6')
    weather4 = p6[0].getText()

    result = ''
    result = result + ('Утром :' + weather1 + ' ' + weather2) + '\n'
    result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
    temp = b.select('.rSide .description')
    weather = temp[0].getText()
    result = result + weather.strip()

    return result

def onload(id, uname, role):
    data1 = [(id, uname, role)]
    cursor.executemany("INSERT INTO idd(uid, uname, role) VALUES (?,?,?)", data1)
    conn.commit()
    
def search(arg):
    sql = "SELECT * FROM idd WHERE uname=?"
    cursor.execute(sql, [(str(arg))])
    return(cursor.fetchall())    
    
tot = Bot('tot_bot', '2128506q')
tot.loop()
conn.close()
