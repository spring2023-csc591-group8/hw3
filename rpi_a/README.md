# Raspberry Pi A

## Environment

The code was tested with Python 3.11 installed on Raspbian 11 running on Raspberry Pi 4b.

### Create Python venv (optional)

If you don't want to affect your global Python installation, you can create a virtual environment and activate it:

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
```

### Install required packages

Install the packages using the following command:

```bash
$ pip3 install -r requirements.txt
```

## Arduino setup

Since we are using Arduino to obtain values from the sensors, a special sketch needs to be uploaded
to it. Follow the instructions here to do this: 
https://mryslab.github.io/telemetrix/telemetrix4arduino/

There is no need to change any parameters, the default parameters should be sufficient.

## Running the code

After setting up and connecting the Arduino to the Raspberry Pi, you can run the code using the
following command:

```bash
./rpi_a -b BROKER_ADDRESS
```

The script assumes that the broker is running at `BROKER_ADDRESS` and is listening on the default
port (1883).
