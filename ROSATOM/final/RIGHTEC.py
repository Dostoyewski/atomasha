# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:38:38 2019

@author: Федор
"""

import paho.mqtt.client as mqtt
import time
import serial
try:
    ser = serial.Serial("COM8", 115200)
except:
    pass


broker="sandbox.rightech.io"
clientID = "cardid"
userd = {"login": "admin", "pw": "admin"}

def on_connect(client, userdata, flags, rc):
    pass
    if rc==0:
        print("Bot connected OK")
    else:
        print("Bad connection Returned code=",rc)
        
def on_disconnect(client, userdata, rc):
    pass

def on_publish(client, userdata, rc):
    print("Data published")

# Работа с сообщениями
client = mqtt.Client(client_id=clientID)            
client.username_pw_set(username=userd["login"],password=userd["pw"])
client.on_connect=on_connect 
client.on_disconnect=on_disconnect
client.on_publish = on_publish
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker) 

while True:
    if ser.isOpen():
      
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output
            
            #time.sleep(1)
      
            
            string = ser.readline()
            #time.sleep(11)
            print("read data:",string)
            client.publish('cid', string.decode('utf-8'))
      
        except Exception as e1:
            print ("error communicating...: " + str(e1))
            
    else:
        print( "cannot open serial port ")

client.loop_stop()
client.disconnect() 
ser.close()
input()