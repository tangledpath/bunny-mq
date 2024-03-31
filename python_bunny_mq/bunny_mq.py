import logging
import queue
import signal
import time
from threading import Thread, Event
from typing import Dict, Any, Callable

logger = logging.getLogger("python-bunny-mq")


class BunnyMQ(Thread):
    """
    Lightweight message queue for intra-process pub-sub communication.

    Usage:
    ```
    def foo_handler(message):
        print(f"Message: {message}")

    bunny = BunnyMQ(timeout=0.1)
    try:
        bunny.register_handler("foo", foo_handler)
        bunny.start()
        bunny.send_message(type='foo', body="foobar")
        time.sleep(1)
    finally:
        bunny.stop()
    ```
    """

    def __init__(self, timeout: float = 1.0, interval: float = 1.0, grace_period: float = 15.0):
        """
        Constructs a new BunnyMQ
        :param timeout: Timeout period for thread operations
        :param interval: Interval to sleep when queue is empty
        :param grace_period: How long to wait after stopping to wait for messages in the queue to empty out:
        """
        Thread.__init__(self)
        self.queue = queue.Queue()
        self.handlers: Dict[str, Callable] = {}
        self.timeout = timeout
        self.interval = interval
        self.grace_period = grace_period
        self.stopping = False
        self.stopped = Event()

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """
        Registers a handler for given message_typ
        :param message_type: The message type
        :param handler: The callable to register; this will be passed the messag
        """
        logger.info(f"Registering handler for {message_type}")
        self.handlers[message_type] = handler

    def execute(self):
        """
        Begin execution of the queue.  this starts the underlying thread, which
        will call `run`.  It also registers handlers for SIGTERM and SIGINT, so we
        can cleanly shut down:
        """
        signal.signal(signal.SIGTERM, self.__signal_shutdown)
        signal.signal(signal.SIGINT, self.__signal_shutdown)
        self.start()

    def run(self):
        """ This is the underlying Thread's run method; called via `execute->start` """
        while not self.stopped.wait(self.timeout):
            self.handle_message()
            if self.queue.empty():
                time.sleep(self.interval)

    def handle_message(self):
        """
        Handles the next message from the queue; calling any registered
        handlers with the message
        """
        try:
            message: Dict[str] = self.queue.get(block=False)
            logger.info(f"Received message: {message}")
            message_type = message["type"]
            handler = self.handlers.get(message_type, None)
            handler(message)
        except queue.Empty:
            pass

    def __len__(self):
        """
        Returns the number of messages in the queue.

        Usage:
             bunny_mq = BunnyMQ()
             len(bunny_mq)
        """
        return self.queue.qsize()

    def stop(self):
        """
        Stop processing messages and shuts down the queue.   This disallows new messages
        shuttint down, and waits up to a period of self.grace_period for the queue to empty:
        """
        self.stopping = True
        logger.info(f"Stopping queue with: {self.queue.qsize()} items left.")
        for i in range(int(self.grace_period)):
            if self.queue.empty():
                break
            time.sleep(1)
        self.stopped.set()
        self.join(self.timeout)
        logger.info(f"Stopped queue with: {self.queue.qsize()} items left.")

    def send_message(self, message: Dict[str, Any]):
        """ Stores a message in the queue, to processed by any registered handlers"""
        if self.stopping:
            logger.info(f"Queue is stopped; blocking message: {message}")
        else:
            logger.info(f"Sending message: {message}")
            self.queue.put(message)

    def __signal_shutdown(self, _signum, _frame):
        """ Called because of a SIGTERM or SIGINT signal"""
        self.stop()
