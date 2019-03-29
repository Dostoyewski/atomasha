# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:27:06 2019

@author: Федор
"""
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
import apiai, json

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



def main():
    #pprint(rocket.im_list().json())
    #print("delete")
    #pprint(rocket.im_close('bZ4uJ45GBehdk9L7GoyJLq8BjyvnsrhsjD').json())
    #run()
    #pprint(rocket.chat_get_message('FPmpMLZCknytFzPr3').json())
    run()
    

def run():
    while True:
        jsonData = rocket.im_list().json()
        idd = []
        msg = []
        text = []
        name = []
        for i in range(0, len(jsonData['ims'])):
            idd.append(jsonData['ims'][i]['_id'])
            msg.append(jsonData['ims'][i]['lastMessage']['_id'])
            text.append(rocket.im_history(str(idd[i]), count=1).json()['messages'][0]['msg'])
            name.append(rocket.im_history(str(idd[i]), count=1).json()['messages'][0]['u'])
            #print(textMessage(text[i]))
            #if('привет' in text[i].lower()):
             #   if(str(name[i]['name']) != 'ATOMASHA'):
              #      rocket.chat_post_message('Иди нахуй, ' + str(name[i]['name']), channel=str(idd[i]))
            if(str(name[i]['name']) != 'ATOMASHA'):
                rocket.chat_post_message(textMessage(text[i], idd[i]), channel=str(idd[i]))
        print(idd)
        print(msg)
        print(text)


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
    

if __name__ == '__main__':
    main()