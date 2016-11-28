import asyncio
from urban_journey import event_loop
from urban_journey.pubsub.networking.connection import Connection


class Listener:
    def __init__(self, host, port, connection_list=None, loop=None):
        self.host = host  #: Listening host
        self.port = port  #: Listening port
        self.loop = loop or event_loop.get()  #: Event loop onto which the listener is running.
        self.server = None  #: class:`asyncio.Server` instance used by the listener.
        self.connection_list = connection_list or []  #: List of hosts

        asyncio.run_coroutine_threadsafe(self.start_server(), self.loop)

    async def start_server(self):
        """
        Starts the listening server.

        :return: Server object
        :rtype: asyncio.Server
        """
        print("Creating server listing on '{}:{}'".format(self.host, self.port))
        self.server = await asyncio.start_server(self.create_connection,
                                                 self.host,
                                                 self.port)
        return self.server

    def create_connection(self, reader, writer):
        """
        Create a new connection.

        :param asyncio.StreamReader reader: Reader object
        :param asyncio.StreamReader writer: Writer object
        :return: Connection object.
        """
        print("Creating new host")
        self.connection_list.append(Connection(reader, writer))
