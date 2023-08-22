import asyncio
import threading
from lib.config import Config
from datetime import datetime
from lib.constants import Dates
class Pipeline:

    def __init__(self, async_generator, func_tuples, cron: bool = False):
        self.cron = cron
        self.async_generator = async_generator
        self.data_queue = asyncio.Queue(maxsize=6)  # Set queue size to max 6
        self.stop_signal = asyncio.Event()
        self.func_tuples = func_tuples
        self.counter = 0
        self.flag = 0

    async def producer(self):
        async for data in self.async_generator:
            print("Producer: Got data from async generator", self.data_queue.qsize())
            print("data", len(data))
            if datetime.strftime(data[0]["Date"], '%d-%m-%y') == Dates.today and self.flag != len(data):
                print(f"Data has been updated: from {self.flag} to {len(data)}")
                self.flag = len(data)

            print("date", data[0]["Date"])
            self.counter += len(data)
            print("counter", self.counter)
            await self.data_queue.put(data)  # This will block if the queue is full
        self.stop_signal.set()

    async def start(self):
        if self.cron != False:
            self.async_generator = self.run_cron(self.async_generator, Config.refresh_interval)
            await self.run()
        else:
            await self.run()
    async def run_cron(self, generator, interval_seconds: int):
        while True:
            print(f"Starting the cron job... {datetime.now()}")
            async for data in generator:
                yield data
            print(f"Job done! Waiting for {interval_seconds} seconds...")
            await asyncio.sleep(interval_seconds)

    async def run(self):
        # Start fetching data asynchronously on the main thread
        producer_task = asyncio.create_task(self.producer())
        consumer_task = asyncio.create_task(self.consumer())

        await producer_task
        await consumer_task

    async def consumer(self):

        while not self.stop_signal.is_set() or not self.data_queue.empty():
            try:
                # Get data from the queue with a timeout to avoid infinite blocking
                data = await asyncio.wait_for(self.data_queue.get(), timeout=1)

                # Start the threads for the current data
                threads = [threading.Thread(target=func, args=(data, *args)) for func, *args in self.func_tuples]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                raise e

        print("All data processed!")
