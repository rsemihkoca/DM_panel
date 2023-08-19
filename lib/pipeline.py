import asyncio
import threading
import queue
class Pipeline:

    # Change generator daily to 5 minutes for today
    def __init__(self, async_generator):
        self.async_generator = async_generator
        self.data_queue = queue.Queue()
        self.processed_event = threading.Event()
        self.stop_signal = False

    async def producer(self):
        async for data in self.async_generator:
            self.data_queue.put(data)
        self.stop_signal = True
    async def start(self):

        asyncio.run(self.run())

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
                data = await self.data_queue.get(timeout=1)
                self.processed_event.clear()  # Reset the event for the new data

                # Start the threads for the current data
                thread1 = threading.Thread(target=self.func1, args=(data,))
                thread2 = threading.Thread(target=self.func2, args=(data,))
                thread1.start()
                thread2.start()

                # Wait for both threads to finish processing the current data
                thread1.join()
                thread2.join()

            except Exception as e:
                raise e

        print("All data processed!")

    # Usage


processor = Pipeline()
asyncio.run(processor.run())
