import paho.mqtt.client as mqtt

broker_IP = 'broker.mqttdashboard.com'
port = 8000
keep_alive = 60

threshold_value = None
previous_decision = None

topics = [("IoT/lightSensor", 2), ("IoT/threshold", 2)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.publish("Status/RaspberryPiC", "online", 2, True)
        print("Connected to the Broker with result code " + str(rc))
    else:
        print("Did not connect to the Broker with result code " + str(rc))

def on_message(client, userdata, message):
    global threshold_value, previous_decision
    payload = message.payload.decode("utf-8")

    if message.topic == topics[1][0]:
        threshold_value = float(payload)
    else:
        # Compare LDR value with threshold and generate binary result
        ldr_value = float(payload)
        if ldr_value >= threshold_value:
            result = "TurnOff"
        else:
            result = "TurnOn"
        # Compare result with previous decision and publish updated decision if changed
        if result != previous_decision:
            previous_decision = result
            client.publish("IoT/Light_status", result, 2, True)

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
