import os
import sys
import time
from datetime import datetime
import statistics
import collections
from collections import defaultdict
from paho.mqtt import client as mqtt
import RPi.GPIO as GPIO

Broker_ip = '192.168.1.198'
Port_num = 1883
Keep_alive = 60

Broker_Topics = [("IoT/Light_status",2), ("IoT/RpiA",2), ("IoT/RpiC",2)]

Rpi_A_status = 18
Rpi_C_status = 16
Light_status = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Rpi_A_status, GPIO.OUT)
GPIO.setup(Rpi_C_status, GPIO.OUT)
GPIO.setup(Light_status, GPIO.OUT)

GPIO.output(Rpi_A_status, GPIO.LOW)
GPIO.output(Rpi_C_status, GPIO.LOW)
GPIO.output(Light_status, GPIO.LOW)


def on_connect(client, userdata, flags, rc):
    print("Connected to the Broker with result code "+str(rc))

def on_message(client, userdata, message):   
    if message.topic == Broker_Topics[0][0]:
        if message.payload == b"turnoff":
            GPIO.output(Light_status, GPIO.LOW)
        elif message.payload == b"turnon":
            GPIO.output(Light_status, GPIO.HIGH)
    elif message.topic == Broker_Topics[1][0]:
        if message.payload == b"offline":
            GPIO.output(Rpi_A_status, GPIO.LOW)
        elif message.payload == b"online":
            GPIO.output(Rpi_A_status, GPIO.HIGH)
    elif message.topic == Broker_Topics[2][0]:
        if message.payload == b"offline":
            GPIO.output(Light_status, GPIO.LOW)
            GPIO.output(Rpi_C_status, GPIO.LOW)
        elif message.payload == b"online":
            GPIO.output(Rpi_C_status, GPIO.HIGH)
           

def run():
    subscriber = mqtt.Client("RPiB")
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    subscriber.connect(Broker_ip, Port_num, Keep_alive)
    subscriber.loop_start()
    subscriber.subscribe(Broker_Topics)

    try:
        while True:
            continue
    except:
        GPIO.cleanup()


if __name__ == '__main__':
    run()
