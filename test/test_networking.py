import os
import unittest
import struct
import asyncio
import sys
from queue import Queue

import umsgpack

from urban_journey.pubsub.networking.listener import Listener
from urban_journey.pubsub.networking.connection import Connection
from urban_journey.pubsub.networking.decoder import Decoder

from urban_journey import get_event_loop


class TestNetworking(unittest.TestCase):
    def test_decoder(self):
        """
        This test, tests whether the decoder is working properly by given it a raw package and checking whether the
        result matches.

        """

        async def run(q):
            try:
                decoder = Decoder()
                inp_data = [0, [1, 2, 3]]

                data = umsgpack.packb(inp_data)

                await decoder.digest(struct.pack(">I", len(data)))
                await decoder.digest(data)

                out_data = await decoder.get()

                assert inp_data == out_data
                q.put(None)
            except:
                q.put(sys.exc_info())

        q = Queue()
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(run(q), loop)

        # If you get an Empty exception over here, it means the co-routine timed out.
        exc_info = q.get(timeout=1)
        if exc_info is not None:
            raise exc_info[1].with_traceback(exc_info[2])

    def test_decoder_failure(self):
        """
        This test checks that the decoder works properly whenever random data in given to it.

        :return:
        """

        async def run(q):
            try:
                s = asyncio.Semaphore(0)

                def error_callback():
                    q.put(None)
                    s.release()

                decoder = Decoder(error_callback)

                data = os.urandom(1000)

                await decoder.digest(struct.pack(">I", len(data)))
                await decoder.digest(data)

                s.acquire()
                q.put(None)
            except:
                q.put(sys.exc_info())

        q = Queue()
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(run(q), loop)

        # If you get an Empty exception over here, it means the co-routine timed out.
        exc_info = q.get(timeout=1)
        if exc_info is not None:
            raise exc_info[1].with_traceback(exc_info[2])

    def test_ping(self):
        async def run(q):
            try:
                connections = {}
                listener = Listener("127.0.0.1", 8888, connections)
                await listener.wait_until_started()

                client_connection = await Connection.from_host("127.0.0.1", 8888)

                # This one is optional. Any commands transmitting will wait for the connection to be ready anyways.
                await client_connection.wait_for_ready()

                await client_connection.ping()
                await client_connection.ping()

                q.put(None)
            except:
                q.put(sys.exc_info())

        q = Queue()
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(run(q), loop)

        # If you get an Empty exception over here, it means the co-routine timed out.
        exc_info = q.get(timeout=1)
        if exc_info is not None:
            raise exc_info[1].with_traceback(exc_info[2])
