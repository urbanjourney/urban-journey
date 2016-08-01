"""This module contains f"""

import asyncio
from threading import Thread, Semaphore


loop = None
thread = None


def get():
    """Returns the event secondary event loop."""
    global loop
    if loop is None:
        enable_event_loop()
    return loop


def get_thread():
    """Returns the thread object running the secondary event loop."""
    global thread
    return thread


def enable_event_loop():
    """Creates a secondary thread running an asyncio event loop."""
    global thread
    if thread is None:
        s = Semaphore(0)
        thread = Thread(target=event_loop_target, args=(s,))
        thread.start()
        s.acquire()


def event_loop_target(s):
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    s.release()
    loop.run_forever()


if __name__ == "__main__":
    enable_event_loop()
