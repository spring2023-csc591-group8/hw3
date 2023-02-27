#!/usr/bin/env python3
from pyfirmata import Arduino, util
from time import sleep


def main():
    board = Arduino("/dev/ttyACM0")
    led = 13

    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()

    while True:
        value = board.analog[0].read()
        print(value)
        if value is not None and value > 0.5:
            board.digital[led].write(1)
        else:
            board.digital[led].write(0)
        sleep(0.2)


if __name__ == "__main__":
    main()


