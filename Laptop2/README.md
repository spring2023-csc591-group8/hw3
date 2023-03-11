# IoT_Assignment_3 - Laptop 2

## Environment
- macOS Catalina Version 10.15.7
- Python 3.7.3

## Software
- Python3 3.7.3
- paho-mqtt 

```
pip install paho-mqtt
pip install RPi.GPIO
```

## Procedure
Initially update the `Broker_ip` and `Port_num`in the code file laptop2.py to the Ip_address and Port of device where the Broker is currently running. 

Run the Laptop 2 code by executing the below command on a new terminal window
```
python3 laptop2.py
```

The detail logs will be saved in the `LogFile` file with the below fields:

```
TimeStamp,Device,Topic,Message Received
