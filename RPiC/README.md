# Raspberry Pi C

## Introduction
This Raspberry Pi controls whether Raspberry Pi B turns the led light on or off. If the LDR value received from Raspberry Pi A is greater than or equal to the threshold, then a `TurnOn` message is published. If not, a `TurnOff` message is published.

## Setup
To setup Raspberry Pi C, `cd` inside the `RPiC` folder and run
```
pip install -r requirements.txt
```

Once the required packages are installed, simply run:
```
python3 RPi_C.py
```

Please note `RPi_C.py` must be run after the broker has started, otherwise a connection error will occur.
