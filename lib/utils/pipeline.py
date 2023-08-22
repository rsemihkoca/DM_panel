import asyncio
import threading
from datetime import datetime
from lib.constants import Dates
from lib.utils.helper import has_day_changed
class Pipeline:

    def __init__(self, async_generator, func_tuples):
        self.async_generator = async_generator
        self.data_queue = asyncio.Queue(maxsize=6)  # Set queue size to max 6
        self.stop_signal = asyncio.Event()
        self.func_tuples = func_tuples
        self.counter = 0
        self.change_in_data = 0
        self.flag = False

    async def producer(self):
        async for data in self.async_generator:
            date = data[0]["Date"]

            print("==========================")
            print("Producer: Got data from async generator", self.data_queue.qsize())
            print("data", len(data))
            print("date", date)

            if datetime.strftime(date, '%d-%m-%y') == Dates.today and self.change_in_data != len(data):
                print(f"Data has been updated: from {self.change_in_data} to {len(data)}")
                self.change_in_data = len(data)

                if not self.flag:
                    self.flag = True
                    self.counter += len(data)
                    print("counter", self.counter)
                else:
                    if has_day_changed():
                        self.flag = False
                    else:
                        pass
            else:
                self.counter += len(data)
                print("counter", self.counter)

            await self.data_queue.put(data)  # This will block if the queue is full
        self.stop_signal.set()

    async def start(self):
        await self.run()

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
