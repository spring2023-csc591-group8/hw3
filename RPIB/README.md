# IoT_Assignment_3 - Raspberry Pi B

## Environment
- macOS Catalina Version 10.15.7
- Python 3.7.3
- Raspberry PI OS

## Software
- Python3 3.7.3
- paho-mqtt
- RPi.GPIO

```
pip install paho-mqtt
pip install RPi.GPIO
```

## Hardware
- Raspberry PI 4 Model B
- 3 LEDS
- 3 Resistors
- Jumper Wires
- BreadBoard

## Procedure
### Hardware setup for Raspeberry PI B

We have used GPIO 23, 24, and 25 which are pin 16, 18 and 22 respectively on the RPI board.

LED1 is connected to GPIO 25 
LED2 is connected to GPIO 24
LED3 is connected to GPIO 23

The schematic for this implementation can be seen in the file "RPI_B_sch.jpg".


### Software run for Raspeberry PI B

Initially update the `Broker_ip ` and `Port_num `in the code file RPI_B.py to the IP_ADDRESS and PORT of device where the Broker is currently running. 

Run the Raspberry Pi B code by executing the below command on the Raspberry Pi

```
python3 RPI_B.py
```
