"""This module contains f"""

import asyncio
from threading import Thread, Semaphore


loop = None
thread = None


def get(debug_enabled=False) -> asyncio.BaseEventLoop:
    """Returns the event secondary event loop."""
    global loop
    if loop is None:
        enable_event_loop()
    if debug_enabled:
        loop.set_debug(True)
    return loop


def get_thread() -> Thread:
    """Returns the thread object running the secondary event loop."""
    global thread
    return thread


def enable_event_loop():
    """Creates a secondary thread running an asyncio event loop."""
    global thread
    if thread is None:
        s = Semaphore(0)
        thread = Thread(target=event_loop_target, args=(s,), daemon=True)
        # print(1)
        thread.start()
        # print(2)
        s.acquire()
        # print(4)


def event_loop_target(s):
    # print(2)
    global loop, thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # print(3)
    s.release()
    # print(4)
    loop.run_forever()
    # print(999999)
    loop = None
    thread = None

