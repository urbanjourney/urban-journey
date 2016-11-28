from urban_journey import event_loop
import asyncio
from urban_journey.pubsub.networking.decoder import Decoder
import umsgpack
import struct


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamReader, loop=None):
        self.loop = loop or event_loop.get()  #: Event loop onto which the host is running.
        self.reader = reader  #: :class:`asyncio.StreamReader` object of the connection
        self.writer = writer  #: :class:`asyncio.StreamReader` object of the connection
        self.decoder = Decoder()  #: Decoder object.

        self.running = True  #: True if the connection is listening for packages.

        # Start co-routines
        asyncio.run_coroutine_threadsafe(self.package_handler(), self.loop)
        asyncio.run_coroutine_threadsafe(self.data_reader(), self.loop)

    @classmethod
    async def from_host(cls, host, port):
        """
        Creates a connection instance from a host address and port.

        :param string host: Host address
        :param int port: Port
        :return: Instance of Connection
        """

        reader, writer = await asyncio.open_connection(host, port)
        return cls(reader, writer)

    async def data_reader(self):
        """
        Co-routine that is constantly listening for data coming in through the connection. The data is then passed to
        the decoder.
        """

        while self.running:
            data = await self.reader.read(1024)
            if self.reader.at_eof():
                self.running = False
                break
            await self.decoder.digest(data)

    async def package_handler(self):
        """
        Co-routine that handles the packages coming out of the decoder.
        """

        while self.running:
            print(await self.decoder.get())
            await asyncio.sleep(1)

    async def send(self, obj):
        """
        Send data through the connection. This can be a dictionary or array containing data.

        :param obj: Object to send
        """

        data = umsgpack.packb(obj)
        self.writer.write(struct.pack(">I", len(data)))
        self.writer.write(data)
        await self.writer.drain()

    def send_threadsafe(self, obj):
        """
        A thread safe version of send.

        :param obj: Object to send
        """
        asyncio.run_coroutine_threadsafe(self.send(obj), self.loop)
