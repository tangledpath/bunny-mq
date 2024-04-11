import hashlib
import json
import logging
import queue
import signal
import time
import uuid
from threading import Thread, Event
from typing import Dict, Any, Callable

from .bounded_dict import BoundedDict

logger = logging.getLogger("python-bunny-mq")


class BunnyMQ(Thread):
    DEFAULT_NAME = "BunnyMQ"
    WILDCARD_HANDLER = "*"
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
        bunny.send_message(['command':'foo', 'body':{"foo": 'bar}])
        time.sleep(1)
    finally:
        bunny.stop()
    ```
    """

    def __init__(self, name: str = DEFAULT_NAME, timeout: float = 1.0, interval: float = 1.0,
                 grace_period: float = 15.0, sequence_number: int = 0):
        """
        Constructs a new BunnyMQ
        :param name: Name for given queue, in case you are using multiple..
        :param timeout: Timeout period for thread operations
        :param interval: Interval to sleep when queue is empty
        :param grace_period: How long to wait after stopping to wait for messages in the queue to empty out:
        :param sequence_number: Starting sequence number for events, defaults to 0
        """
        Thread.__init__(self)
        self.name = name
        self.queue = queue.Queue()
        self.handlers: Dict[str, Callable] = {}
        self.timeout = timeout
        self.interval = interval
        self.grace_period = grace_period
        self.stopping = False
        self.sequence_number = 0
        self.stopped = Event()
        self.processed_count = 0
        self.processed_events = BoundedDict()

    def send_message(self, command:str, message: Dict[str, Any]) -> Dict[str, Any]:
        """ Stores a message in the queue, to processed by any registered handlers"""
        logger.info(f"Sending message[{command}]: {message}", {"name": self.name})
        result = None
        if self.stopping:
            logger.info(f"Queue is stopped; blocking message: {message}", {
                "name": self.name
            })
        else:
            message_id = str(uuid.uuid4())
            metadata = {
                'command': command,
                'MD5OfMessageBody': hashlib.md5(json.dumps(message).encode()).hexdigest(),
                'MessageId': message_id,
                'SequenceNumber': self.sequence_number
            }
            self.queue.put(dict(metadata=metadata, message=message))
            self.sequence_number += 1
            result = message_id

        return result

    def register_handler(self, message_command: str, handler: Callable) -> None:
        """
        Registers a handler for given message_command
        :param message_command: The message command(type).  Use WILDCARD_HANDLER for all messages.
        :param handler: The callable to register; this will be passed the messag
        """
        logger.info(f"Registering handler for {message_command}")
        handlers = self.handlers.get(message_command, [])
        handlers.append(handler)
        self.handlers[message_command] = handlers

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
            self.processed_count += 1
            if self.queue.empty():
                time.sleep(self.interval)

    def handle_message(self):
        """
        Handles the next message from the queue; calling any registered
        handlers with the message
        """
        try:
            full_event: Dict[str, Any] = self.queue.get(block=False)
            message: Dict[str, Any] = full_event["message"]
            metadata: Dict[str, Any] = full_event["metadata"]

            message_cmd = metadata.get("command", None)
            processed = False
            if message_cmd:
                handlers = self.handlers.get(message_cmd, None)
                if handlers:
                    logger.info(f"Processing message: {message}", {
                        "name": self.name,
                        "message": message,
                        "metadata": metadata,
                    })

                    for handler in handlers:
                        handler(message)
                        processed = True

            # Check for wildcard handlers:
            handlers = self.handlers.get(self.WILDCARD_HANDLER, None)
            if handlers:
                for handler in handlers:
                    handler(message)
                    processed = True

            if processed:
                self.processed_events[metadata["MessageId"]] = full_event

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
        Gracefully stop processing messages and shuts down the queue.   This disallows new
        messages to be sent and waits up to a period of self.grace_period for the queue to empty:
        """
        self.stopping = True
        logger.info(f"Stopping queue with: {self.queue.qsize()} items left.", {
            "name": self.name
        })
        for i in range(int(self.grace_period)):
            if self.queue.empty():
                break
            time.sleep(1)
        self.stopped.set()
        self.join(self.timeout)
        logger.info(f"Stopped queue with: {self.queue.qsize()} items left.", {
            "name": self.name
        })

    def __signal_shutdown(self, _signum, _frame):
        """ Called because of a SIGTERM or SIGINT signal"""
        self.stop()
