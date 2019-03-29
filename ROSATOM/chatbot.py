# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:27:06 2019

@author: Федор
"""
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat


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
    pprint(rocket.im_list().json())
    print("delete")
    pprint(rocket.im_close('bZ4uJ45GBehdk9L7GoyJLq8BjyvnsrhsjD').json())
    #run()
    pprint(rocket.chat_get_message('FPmpMLZCknytFzPr3').json())
    run()
    

def run():
    jsonData = rocket.im_list().json()
    idd = []
    msg = []
    text = []
    for i in range(0, len(jsonData['ims'])):
        idd.append(jsonData['ims'][i]['_id'])
        msg.append(jsonData['ims'][i]['lastMessage']['_id'])
        text.append(rocket.im_history(str(idd[i]), count=1).json()['messages'][0]['msg'])
        
    print(idd)
    print(msg)
    print(text)


if __name__ == '__main__':
    main()