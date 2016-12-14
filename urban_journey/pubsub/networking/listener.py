import asyncio
import sys
from urban_journey import event_loop
from urban_journey.pubsub.networking.connection import Connection

from sim_common.cached import cached

import logging

nlog = logging.getLogger("networking")


class Listener:
    def __init__(self, host, port, connections, loop=None):
        self.host = host  #: Listening host
        self.port = port  #: Listening port
        self.loop = loop or event_loop.get()  #: Event loop onto which the listener is running.
        self.server = None  #: class:`asyncio.Server` instance used by the listener.
        self.connections = connections  #: Dictionary containing all connections.

        asyncio.run_coroutine_threadsafe(self.start_server(), self.loop)

        self.started_semaphore = asyncio.Semaphore(0)

        self.startup_exception_info = None

    async def start_server(self):
        """
        Starts the listening server.

        :return: Server object if successful, otherwise None.
        :rtype: asyncio.Server
        """

        nlog.info("Creating server listing on '{}:{}'...".format(self.host, self.port))
        try:
            self.server = await asyncio.start_server(self.create_connection,
                                                     self.host,
                                                     self.port)
            nlog.info(self.log_prefix + "Success created server listing on '{}:{}'...".format(self.host, self.port))

        except:
            self.startup_exception_info = sys.exc_info()
            nlog.exception(self.log_prefix + "Error opening server listening on '{}:{}'...".format(self.host, self.port))

        self.started_semaphore.release()
        return self.server

    def create_connection(self, reader, writer):
        """
        Create a new connection.

        :param asyncio.StreamReader reader: Reader object
        :param asyncio.StreamWriter writer: Writer object
        :return: Connection object.
        """
        connection = Connection(reader, writer)
        nlog.debug(self.log_prefix + "New connection '{}'".format(connection.name))

        self.connections(connection)

    async def wait_until_started(self):
        """
        Co-routine that blocks until the listener startup process has finished, whether it was successful or not.

        :return: `None` if startup was successful. If unsuccessful it returns the ``(type, value, traceback)`` or the
           exception that occurred while starting. This is the same tuple as returned by :func:`sys.exc_info()`.
        """

        await self.started_semaphore.acquire()
        return self.startup_exception_info

    @cached
    def name(self):
        return "{}:{}".format(self.host, self.port)

    @cached
    def log_prefix(self):
        return "Listener   '{:<21}': ".format(self.name)
