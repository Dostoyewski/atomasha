# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:27:06 2019

@author: tot
"""

from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
import apiai
import json

rocket = RocketChat('atomasha', 'selena', server_url='http://178.70.218.84:3000')
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
    
pprint(rocket.channels_history('GENERAL', count=5).json()['messages'])

class Bot:
    def __init__(self, login, password):
        rocket = RocketChat(login, password, server_url='http://178.70.218.84:3000')
    def getLastMessage(self):
        user = rocket.channels_history('GENERAL', count=5).json()['messages'][0]['u']
        msg = rocket.channels_history('GENERAL', count=5).json()['messages'][0]['msg']
        return user, msg
    def loop(self):
        while True:
            user, msg = self.getLastMessage()
            if ('привет, маша' in msg.lower()):
                rocket.chat_post_message('Привет, '+user['name'], channel='GENERAL')
    
atomasha = Bot('atomasha', 'selena')
print(atomasha.getLastMessage())
atomasha.loop()