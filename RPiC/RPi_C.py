import paho.mqtt.client as mqtt

broker_IP = 'broker.mqttdashboard.com'
port = 8000
keep_alive = 60

topics = [("IoT/lightSensor", 2), ("IoT/threshold", 2), ("IoT/Light_status", 2)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.publish("Status/RaspberryPiC", "online", 2, True)
        print("Connected to the Broker with result code " + str(rc))
    else:
        print("Did not connect to the Broker with result code " + str(rc))

def on_message(client, userdata, message):
    print("message received: " , str(message.payload.decode("utf-8")))
    print("message topic = ", message.topic)
    print("message qos = ", message.qos)
    print("message retain flag = ", message.retain)

def run():
    client = mqtt.Client("RPiC", transport = "websockets")
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set("Status/RaspberryPiC", "offline", 2, True)
    client.connect(broker_IP, port, keep_alive)
    client.loop_start()
    client.subscribe(topics)

    while True:
        continue

if __name__ == "__main__":
    run()
