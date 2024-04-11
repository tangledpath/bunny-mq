from .bunny_mq import BunnyMQ


def test_simple_message():
    """ Test that we can subscribe to a message command type and then receive it when message is sent. """
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
        bunny.send_message(command='foo', message={'body': "foobar"})
    finally:
        bunny.stop()

    assert handled
    assert len(bunny) == 0
    assert bunny.sequence_number == 1
    assert bunny.processed_count == 1
    assert len(bunny.processed_events) == 1


def test_wildcard_handler():
    """ Test that we can subscribe to a wildcard (*) and then receive any command type of message """
    handled = 0

    def wildcard_handler(message):
        """ Test handler for message queue """
        print(f"Message: {message}")
        nonlocal handled
        handled += 1

    bunny = BunnyMQ(interval=0.1)
    assert len(bunny) == 0
    try:
        bunny.register_handler(BunnyMQ.WILDCARD_HANDLER, wildcard_handler)
        bunny.start()
        bunny.send_message(command='foo', message={'body': "barfood"})
        bunny.send_message(command='bar', message={'body': "foobard"})
    finally:
        bunny.stop()

    assert handled == 2
    assert len(bunny) == 0
    assert bunny.sequence_number == 2
    assert bunny.processed_count == 2
    assert len(bunny.processed_events) == 2
