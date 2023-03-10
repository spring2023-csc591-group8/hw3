#!/usr/bin/env python3
import asyncio

from telemetrix_aio.telemetrix_aio import TelemetrixAIO
from time import sleep


async def process_value(data):
    _, _, value, _ = data
    print(value, flush=True)




async def main():
    board = TelemetrixAIO("/dev/ttyACM0", loop=asyncio.get_running_loop(), autostart=False)
    await board.start_aio()
    await board.set_analog_scan_interval(100)
    await board.set_pin_mode_analog_input(0, callback=process_value)

    all_tasks = asyncio.all_tasks()
    current_task = asyncio.current_task()
    all_tasks.remove(current_task)
    await asyncio.wait(all_tasks)


if __name__ == "__main__":
    asyncio.run(main())


