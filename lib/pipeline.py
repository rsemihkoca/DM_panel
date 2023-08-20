import asyncio
import threading


class Pipeline:

    def __init__(self, async_generator, func_tuples):
        self.async_generator = async_generator
        self.data_queue = asyncio.Queue()  # Set queue size to max 6
        self.stop_signal = False
        self.func_tuples = func_tuples
        self.counter = 0

    async def producer(self):
        async for data in self.async_generator:
            print("Producer: Got data from async generator", self.data_queue.qsize())
            print("Data", len(data))
            print("date", data[0]["Date"])
            self.counter += len(data)
            print("counter", self.counter)
            await self.data_queue.put(data)
        self.stop_signal = True

    async def start(self):
        await self.run()

    async def run(self):
        # Start fetching data asynchronously on the main thread
        producer_task = asyncio.create_task(self.producer())
        consumer_task = asyncio.create_task(self.consumer())

        await producer_task
        await consumer_task

    async def consumer(self):
        while not self.stop_signal or not self.data_queue.empty():
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
