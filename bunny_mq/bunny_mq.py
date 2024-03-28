import queue
import signal
from threading import Thread, Event
from typing import Dict, Any, Callable

from loguru import logger

class BunnyMQ(Thread):
    """
    Lightweight message queue for intra-process pub-sub communication.

    Usage:
    ```
    def foo_handler(message):
        print(f"Message: {message}")

    bunny = BunnyMQ(interval=0.1)
    try:
        bunny.register_handler("foo", foo_handler)
        bunny.start()
        bunny.send_message(type='foo', body="foobar")
        time.sleep(1)
    finally:
        bunny.stop()
    ```
    """
    def __init__(self, interval=0.5):
        Thread.__init__(self)
        self.queue = queue.Queue()
        self.handlers: Dict[str, Callable] = {}
        self.interval = interval
        self.stopped = Event()

    def register_handler(self, message_type: str, handler: Callable):
        logger.info(f"Registering handler for {message_type}")
        self.handlers[message_type] = handler

    def execute(self):
        signal.signal(signal.SIGTERM, self.service_shutdown)
        signal.signal(signal.SIGINT, self.service_shutdown)
        self.start()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.handle_message()

    def stop(self):
        logger.info(f"Stopping queue with: {self.queue.qsize()} items left.")
        self.stopped.set()
        self.join()

    def send_message(self, **message: Dict[str, Any]):
        logger.info(f"Sending message: {message}")
        self.queue.put(message)

    def handle_message(self):
        try:
            message: Dict[str] = self.queue.get(block=False)
            logger.info(f"Received message: {message}")
            message_type = message["type"]
            handler = self.handlers.get(message_type, None)
            handler(message)
        except queue.Empty:
            pass

    def service_shutdown(self, _signum, _frame):
        self.stop()
