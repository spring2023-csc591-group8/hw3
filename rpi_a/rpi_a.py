#!/usr/bin/env python3
import argparse
import asyncio

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

    async def run(self):
        wait_time = 1

        init_values = asyncio.create_task(self._init_values())

        done, pending = await asyncio.wait([init_values], timeout=wait_time)
        if pending:
            print("Unable to recover sensor values, starting from scratch")
            for t in pending:
                t.cancel()
        else:
            print(f"Recovered POT {self.pot_value}, LDR {self.ldr_value}")

        await self.board.start_aio()
        await self.board.set_analog_scan_interval(100)
        await self.board.set_pin_mode_analog_input(
                self.POT_PIN,
                differential=int(self.EPSILON * 1023),
                callback=self._process_pot_value)
        await self.board.set_pin_mode_analog_input(
                self.LDR_PIN,
                differential=int(self.EPSILON * 1023),
                callback=self._process_ldr_value)

    async def _init_values(self):
        async with self.client.messages() as messages:
            await self.client.subscribe(self.POT_TOPIC)
            await self.client.subscribe(self.LDR_TOPIC)

            async for message in messages:
                print(f"[{message.topic}] {message.payload}", flush=True)
                if message.topic.matches(self.POT_TOPIC):
                    self.pot_value = float(message.payload)
                elif message.topic.matches(self.LDR_TOPIC):
                    self.ldr_value = float(message.payload)
                if self.pot_value != -1 and self.ldr_value != -1:
                    break

    async def _process_pot_value(self, data):
        _, _, pot_value, _ = data
        if abs(pot_value - self.pot_value) > self.EPSILON * 1023:
            self.pot_value = pot_value
            print(f"POT: {pot_value:.4f}")
            await self.client.publish(self.POT_TOPIC, f"{self.pot_value:.4f}", qos=2, retain=True)

    async def _process_ldr_value(self, data):
        _, _, ldr_value, _ = data
        if abs(ldr_value - self.ldr_value) > self.EPSILON * 1023:
            self.ldr_value = ldr_value
            print(f"LDR: {ldr_value:.4f}")
            await self.client.publish(self.LDR_TOPIC, f"{self.ldr_value:.4f}", qos=2, retain=True)


STATUS_TOPIC = "Status/RaspberryPiA"

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker-address", "-b", required=True)

    args = parser.parse_args()

    will = aiomqtt.Will(STATUS_TOPIC, "offline", qos=2, retain=True)
    board = TelemetrixAIO(loop=asyncio.get_running_loop(), autostart=False)

    async with aiomqtt.Client(args.broker_address, client_id="RPiA", will=will) as client:
        try:
            await client.publish(STATUS_TOPIC, "online", qos=2, retain=True)
            watcher = SensorWatcher(client, board)

            await watcher.run()

            all_tasks = asyncio.all_tasks()
            current_task = asyncio.current_task()
            all_tasks.remove(current_task)
            await asyncio.gather(*all_tasks)
        finally:
            await client.publish(STATUS_TOPIC, "offline", qos=2, retain=True)

if __name__ == "__main__":
    asyncio.run(main())
