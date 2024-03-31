from .bunny_mq import BunnyMQ


def test_bunny_queue():
    """ Test that we can subscribe to a message type and then receive it when message is sent. """
    handled = False

    def foo_handler(message):
        """ Test handler for message queue """
        print(f"Message: {message}")
        nonlocal handled
        handled = True

    bunny = BunnyMQ(interval=0.1)
    assert len(bunny) == 0
    try:
        bunny.register_handler("foo", foo_handler)
        bunny.start()
        bunny.send_message({'type': 'foo', 'body': "foobar"})
    finally:
        bunny.stop()

    assert handled
    assert len(bunny) == 0
