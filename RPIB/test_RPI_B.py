import time
import paho.mqtt.client as mqtt

Broker_ip = '192.168.1.198'
Port_num = 1883
Keep_alive = 60

Light_status_topic = "IoT/Light_status"
Rpi_A_topic = "IoT/RpiA"
Rpi_C_topic = "IoT/RpiC"

client = mqtt.Client("RPiA")
client.connect(Broker_ip, Port_num, Keep_alive)

while True:
    # test the Light_status_topic
    client.publish(Light_status_topic, "turnon")
    time.sleep(1)
    client.publish(Light_status_topic, "turnoff")
    time.sleep(1)

    # test the Rpi_A_topic
    client.publish(Rpi_A_topic, "online")
    time.sleep(1)
    client.publish(Rpi_A_topic, "offline")
    time.sleep(1)

    # test the Rpi_C_topic
    client.publish(Rpi_C_topic, "online")
    time.sleep(1)
    client.publish(Rpi_C_topic, "offline")
    time.sleep(1)

client.disconnect()
