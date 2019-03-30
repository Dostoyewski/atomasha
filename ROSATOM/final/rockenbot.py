# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:31:43 2019

@author: Федор
"""

import os
from RocketChatBot import RocketChatBot

botname = 'atomasha'
botpassword = 'selena'
server_url = 'http://rosatom-chat.ml:3000'

bot = RocketChatBot(botname, botpassword, server_url)
bot.send_message('starting bot...', channel_id='GENERAL')

def greet(msg, user, channel_id):
    bot.send_message('Привет, @' + user, channel_id)
    
bot.add_dm_handler(['привет', 'Привет', ], greet)
bot.run()