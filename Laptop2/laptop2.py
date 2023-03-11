import os
import sys
import time
from datetime import datetime
from paho.mqtt import client as mqtt

Broker_ip = '10.42.0.1'
Port_num = 1883
Keep_alive = 60

Broker_Topics = [("lightSensor",2), ("threshold",2), ("LightStatus",2), ("Status/RaspberryPiA",2), ("Status/RaspberryPiC",2)]

filename = 'LogFile'

def appendFile(content):
    file = open(filename, "a")
    file.write(content + "\n")
    file.close()

def on_connect(client, userdata, flags, rc):
    print("Connected to the Broker with result code "+str(rc))

def on_message(client, userdata, message):
    Device = None
    Info = ""
    Time_Stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
    Msg = str(message.payload.decode("utf-8"))
    
    if message.topic == Broker_Topics[0][0]:
        Device = "Rpi_A"
        Info = "LDR Value"
    elif message.topic == Broker_Topics[1][0]:
        Device = "Rpi_A"
        Info = "Threshold Value"
    elif message.topic == Broker_Topics[2][0]:
        Device = "Rpi_C"
        Info = "Light Status"
    elif message.topic == Broker_Topics[3][0]:
        Device = "Rpi_A"
        Info = "Rpi_A Status"
    elif message.topic == Broker_Topics[4][0]:
        Device = "Rpi_C" 
        Info = "Rpi_C Status"

    content = Time_Stamp + '         ' + Device + '         ' + Info + '        ' + Msg
    appendFile(content)


def run():

    file = open(filename, "w")
    file.write("    TimeStamp                 Device            Topic           Message Received" + "\n")
    file.close()
    
    subscriber = mqtt.Client("Laptop2")
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    subscriber.connect(host = Broker_ip, port = Port_num, keepalive = Keep_alive)
    subscriber.loop_start()
    subscriber.subscribe(Broker_Topics)

    while True:
        continue

if __name__ == '__main__':
    run()
