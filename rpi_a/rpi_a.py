#!/usr/bin/env python3
import argparse
import asyncio
import logging

from traceback import print_exception

import asyncio_mqtt as aiomqtt
import paho.mqtt.client as mqtt

from telemetrix_aio.telemetrix_aio import TelemetrixAIO


class SensorWatcher:
    POT_PIN = 0
    LDR_PIN = 1
    EPSILON = 0.05

    POT_TOPIC = "threshold"
    LDR_TOPIC = "lightSensor"

    def __init__(self, client, board):
        self.client = client
        self.board = board
        self.pot_value = -1
        self.ldr_value = -1

        self.pot_value_max = 0
        self.pot_value_min = 1023

        self.ldr_value_max = 0
        self.ldr_value_min = 1023

    async def run(self):
        wait_time = 1

        for i in range(5):
            try:
                await self.board.start_aio()
                break
            except RuntimeError as e:
                if not str(e).startswith("No Arduino Found"):
                    raise
                print(f"Couldn't connect Arduino, running attempt {i+2}...")
        else:
            raise RuntimeError("Arduino connection failed")

        # NB: With the loop above, there exists and edge case in which we will
        # send the "offline" status before becoming online in the first place.
        # It was decided that this behaviour is preferable to sending some data
        # before setting the "online" status, which could happen if we send the
        # "online" message after we finish Arduino setup
        await self.client.publish(STATUS_TOPIC, "online", qos=2, retain=True)

        try:
            async with asyncio.timeout(wait_time):
                await self._init_values()
        except TimeoutError:
            print("Unable to recover sensor values, starting from scratch")


        await self.board.set_analog_scan_interval(100)
        await self.board.set_pin_mode_analog_input(
                self.POT_PIN,
                # differential=int(self.EPSILON * 1023),
                callback=self._process_pot_value)
        await self.board.set_pin_mode_analog_input(
                self.LDR_PIN,
                # differential=int(self.EPSILON * 1023),
                callback=self._process_ldr_value)

    def print_stats(self):
        print(f"Observed POT range: {self.pot_value_min}-{self.pot_value_max}", flush=True)
        print(f"Observed LDR range: {self.ldr_value_min}-{self.ldr_value_max}", flush=True)

    async def _init_values(self):
        async with self.client.messages() as messages:
            await self.client.subscribe(self.POT_TOPIC)
            await self.client.subscribe(self.LDR_TOPIC)

            async for message in messages:
                if message.topic.matches(self.POT_TOPIC):
                    self.pot_value = float(message.payload)
                    print(f"Recovered POT value: {self.pot_value}")
                elif message.topic.matches(self.LDR_TOPIC):
                    self.ldr_value = float(message.payload)
                    print(f"Recovered LDR value: {self.ldr_value}")
                if self.pot_value != -1 and self.ldr_value != -1:
                    break

    async def _process_pot_value(self, data):
        _, _, pot_value, _ = data
        self.pot_value_min = min(self.pot_value_min, pot_value)
        self.pot_value_max = max(self.pot_value_max, pot_value)
        if abs(pot_value - self.pot_value) > self.EPSILON * 1023:
            self.pot_value = pot_value
            await self.client.publish(self.POT_TOPIC, f"{self.pot_value:.4f}", qos=2, retain=True)

    async def _process_ldr_value(self, data):
        _, _, ldr_value, _ = data
        self.ldr_value_min = min(self.ldr_value_min, ldr_value)
        self.ldr_value_max = max(self.ldr_value_max, ldr_value)
        if abs(ldr_value - self.ldr_value) > self.EPSILON * 1023:
            self.ldr_value = ldr_value
            await self.client.publish(self.LDR_TOPIC, f"{self.ldr_value:.4f}", qos=2, retain=True)


STATUS_TOPIC = "Status/RaspberryPiA"


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker-address", "-b", required=True)

    args = parser.parse_args()

    will = aiomqtt.Will(STATUS_TOPIC, "offline", qos=2, retain=True)
    board = TelemetrixAIO(autostart=False, close_loop_on_shutdown=False)

    async with aiomqtt.Client(args.broker_address, client_id="RPiA", will=will, keepalive=1) as client:
        try:
            watcher = SensorWatcher(client, board)

            await watcher.run()

            all_tasks = asyncio.all_tasks()
            current_task = asyncio.current_task()
            all_tasks.remove(current_task)
            await asyncio.gather(*all_tasks)
        except BaseException as e:
            print()
            print("Caught exception:")
            print_exception(e)
        finally:
            print()
            print("Shutting down gracefully")
            watcher.print_stats()
            await client.publish(STATUS_TOPIC, "offline", qos=2, retain=True)

if __name__ == "__main__":
    asyncio.run(main())
