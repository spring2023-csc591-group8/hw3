import paho.mqtt.client as mqtt

broker_IP = ['10.42.0.1', '10.42.0.210']
port = 1883
keep_alive = 60

threshold_value = None
ldr_value = None
previous_decision = None

topics = [("lightSensor", 2), ("threshold", 2)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.publish("Status/RaspberryPiC", "online", 2, True)
        print("Connected to the Broker with result code " + str(rc))
    else:
        print("Did not connect to the Broker with result code " + str(rc))

def on_message(client, userdata, message):
    global threshold_value, ldr_value, previous_decision
    payload = message.payload.decode("utf-8")

    if message.topic == topics[1][0]:
        threshold_value = float(payload)
    else:
        ldr_value = float(payload)

    print(f"LDR value: {ldr_value}")
    if threshold_value is not None and ldr_value is not None:
        # Compare LDR value with threshold and generate binary result
        if ldr_value >= threshold_value:
            result = "TurnOff"
        else:
            result = "TurnOn"
        # Compare result with previous decision and publish updated decision if changed
        if result != previous_decision:
            previous_decision = result
            client.publish("LightStatus", result, 2, True)
            print("Published result")

def run():
    client = mqtt.Client("RPiC")
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set("Status/RaspberryPiC", "offline", 2, True)
    try:
        client.connect(broker_IP[0], port, keep_alive)
    except:
        client.connect(broker_IP[1], port, keep_alive)
    client.loop_forever()
    client.subscribe(topics)

if __name__ == "__main__":
    run()
