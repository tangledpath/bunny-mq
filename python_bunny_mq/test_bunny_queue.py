import time

from .bunny_mq import BunnyMQ


def test_bunny_queue():
    def foo_handler(message):
        print(f"Message: {message}")

    bunny = BunnyMQ(interval=0.1)
    try:
        bunny.register_handler("foo", foo_handler)
        bunny.start()
        bunny.send_message(type='foo', body="foobar")
        # time.sleep(1)
    finally:
        bunny.stop()
