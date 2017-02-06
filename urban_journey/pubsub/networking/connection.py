import sys
from urban_journey import event_loop
import asyncio
from urban_journey.pubsub.networking.decoder import Decoder
from urban_journey.pubsub.networking.network_command import network_command, NetworkCommandBase
import umsgpack
import struct
import logging
import time
import inspect
import functools
import socket
import os
import hashlib


from sim_common.cached import cached
from sim_common import log_exc, print_exc

nlog = logging.getLogger("networking")
dlog = logging.getLogger("networking.data_layer")
hlog = logging.getLogger("networking.handshake")
plog = logging.getLogger("networking.ping_pong")

# This is a salt added when hashing the handshake data. This salt is known by both sides and is never
# transmitted.
salt = b"urban_journey"

# Use this regex to comment out all debug logging. Replace logger_name by logger name
# (?:(\s+)|(?:#\s*))(logger_name\.debug.+)
# $1# $2

# Use this regex to uncomment them
# (\s*)(?:#\s*)(logger_name\.debug.+)
# $1$2


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, loop=None):
        self.loop = loop or event_loop.get()  #: Event loop onto which the host is running.
        self.close_event
        self.reader = reader  #: :class:`asyncio.StreamReader` object of the connection.
        self.writer = writer  #: :class:`asyncio.StreamReader` object of the connection.
        self.decoder = Decoder(self.close)  #: Decoder object.

        self.running = True  #: True if the connection is listening for packages.

        self.closing_semaphore = asyncio.Semaphore(0)
        self.ping_semaphore = asyncio.Semaphore(0)

        # Create and load in commands dictionary.
        self.__command_dictionary = {}
        for member_name in dir(self):
            member = inspect.getattr_static(self, member_name)
            if isinstance(member, NetworkCommandBase):
                if member.command_id in self.__command_dictionary:
                    raise ValueError("Network command ids must be unique. '{}' and '{}' have the same id '{}'.".format(
                        member.name,
                        self.__command_dictionary[member.command_id].func.__name__,
                        member.command_id
                    ))
                else:
                    self.__command_dictionary[member.command_id] = functools.partial(member.handler_func, self)
                    self.__dict__["transmit_" + member.name] = functools.partial(self.transmit, member.command_id)

        self.handshake_data = None

        self.__ready_condition = asyncio.Condition()
        self.ready = False

        self.__closed_condition = asyncio.Condition()

        self.__identify_semaphore = asyncio.Semaphore(0)

        self.hostname = socket.gethostname()
        self.remote_hostname = None

        # Start co-routines
        asyncio.run_coroutine_threadsafe(self.package_handler(), self.loop)
        asyncio.run_coroutine_threadsafe(self.data_reader(), self.loop)
        asyncio.run_coroutine_threadsafe(self.handshake(), self.loop)

    @classmethod
    async def from_host(cls, host, port):
        """
        Creates a connection instance from a host address and port.

        :param string host: Host address
        :param int port: Port
        :return: Instance of Connection
        """
        dlog.debug("Creating connection from host at '{}:{}'.".format(host, port))
        reader, writer = await asyncio.open_connection(host, port)
        return cls(reader, writer)

    async def data_reader(self):
        """
        Co-routine that is constantly listening for data coming in through the connection. The data is then passed to
        the decoder.
        """

        dlog.debug(self.log_prefix + "Waiting for incoming data.")
        while self.running:
            data = await self.reader.read(1024)
            # dlog.debug(self.log_prefix + "in_data {}".format(data))
            if self.reader.at_eof():
                self.running = False
                break
            await self.decoder.digest(data)
        dlog.debug(self.log_prefix + "Closed")
        self.__closed_condition.notify_all()

    async def package_handler(self):
        """
        Co-routine that handles the packages coming out of the decoder.
        """
        dlog.debug(self.log_prefix + "Package handler started")
        while self.running:
            decoder_future = asyncio.ensure_future(self.decoder.get())
            await asyncio.wait((decoder_future, self.closing_semaphore.acquire()), return_when=asyncio.FIRST_COMPLETED)
            if decoder_future.done():
                package = decoder_future.result()
                dlog.debug(self.log_prefix + "Received '{}({})'".format(
                    self.__command_dictionary[package[0]].func.__name__,
                    package[1]
                ))
                await self.__command_dictionary[package[0]](*package[1])
            else:
                break
        dlog.debug(self.log_prefix + "Package handler stopped")

    async def transmit(self, command_id, *args):
        """
        Send data through the connection. This can be a dictionary or array containing data.

        :param command_id: Command id
        :param *args: Command arguments
        """

        # Always allow if it's ready to transmit.
        # Only allow handshake and identify packages if it's not ready to transmit.
        if not self.ready and (command_id > 3):
            await self.wait_for_ready()

        dlog.debug(self.log_prefix + "Transmitting '{}({})'".format(
            self.__command_dictionary[command_id].func.__name__,
            args
        ))
        data = umsgpack.packb((command_id, args))
        self.writer.write(struct.pack(">I", len(data)))
        self.writer.write(data)
        await self.writer.drain()

    def transmit_threadsafe(self, command_id, *args):
        """
        A thread safe version of send.

        :param command_id: Command id
        :param *args: Command arguments
        """
        asyncio.run_coroutine_threadsafe(self.transmit(command_id, *args), self.loop)

    @cached
    def name(self):
        return "{}:{}".format(*self.writer.transport.get_extra_info('peername'))

    @cached
    def log_prefix(self):
        return "Connection '{:<21}': ".format(self.name)

    @property
    def closed(self):
        return not self.running

    def close(self):
        self.writer.close()

    async def wait_for_closed(self):
        with self.__closed_condition:
            self.__closed_condition.wait_for(lambda: not self.running)

    async def wait_for_ready(self):
        with await self.__ready_condition:
            await self.__ready_condition.wait_for(lambda: self.ready)

    # Handshake ========================================================================================================
    @network_command(0)
    async def handshake(self, timeout=5):
        """
        Coroutine that performs a handshake with the remote. This is to make sure that the remote is another urban
        journey instance.

        :param timeout: Timeout value for the remote
        :return: True if the handshake was successful, otherwise false.
        :rtype: bool
        """

        # Generate a random bytestring to be used for the handshake
        self.handshake_data = os.urandom(32)

        # hlog.debug(self.log_prefix + "Handshake transmit       " + self.handshake_data.hex())
        # Transmit the handshake commad to the remote
        await self.transmit_handshake(self.handshake_data)

    @handshake.handler
    async def handshake(self, data):
        """
        Handler for the handshake command.

        :param data: Random data that has to be hashed and transmitted in a handshake_reply command.
        """

        # hlog.debug(self.log_prefix + "Handshake received       " + data.hex())
        reply_data = hashlib.sha256(data + salt).digest()
        await self.handshake_reply(reply_data)

    @network_command(1)
    async def handshake_reply(self, data):
        """
        Transmits the hashed handshake data back to the remote
        :param data: Hashed data.
        """
        # hlog.debug(self.log_prefix + "Handshake reply send     " + data.hex())
        await self.transmit_handshake_reply(data)

    @handshake_reply.handler
    async def handshake_reply(self, data):
        """
        Handles the handshake reply command with the hashed data.

        :param data: Hashed data.
        """

        # Create a future on the queue.get() co-routine and await it with a timeout.
        # hlog.debug(self.log_prefix + "Handshake reply received " + data.hex())

        correct = hashlib.sha256(self.handshake_data + salt).digest()

        if data == correct:
            # hlog.debug(self.log_prefix + "Handshake success        ")

            # Ask the remote for identification information
            asyncio.ensure_future(self.identify())
        else:
            self.close()
            # hlog.debug(self.log_prefix + "Handshake failed         ")

    # Identify =========================================================================================================
    @network_command(2)
    async def identify(self):
        """
        Asks the remote to identify itself.

        :param float timeout: If non-zero, the coroutine will block until time the reply has been received or timeout.
        """
        await self.transmit_identify()

    @identify.handler
    async def identify(self):
        await self.identify_reply()

    @network_command(3)
    async def identify_reply(self):
        """
        Sends the identification information to the remote.
        """
        await self.transmit_identify_reply(self.hostname)

    @identify_reply.handler
    async def identify_reply(self, hostname):
        nlog.debug(self.log_prefix + "")
        self.remote_hostname = hostname
        self.ready = True
        self.decoder.restricted = False
        with await self.__ready_condition:
            self.__ready_condition.notify_all()

    # Ping Pong ========================================================================================================
    @network_command(4)
    async def ping(self, timeout=None):
        """
        Coroutine that transmits a ping command and waits until pong is received.

        :param timeout: Timeout
        :return: Ping time
        """
        await self.transmit_ping()

        t0 = time.perf_counter()
        plog.debug(self.log_prefix + "Ping")
        await asyncio.wait_for(self.ping_semaphore.acquire(), timeout=timeout)
        plog.debug(self.log_prefix + "Ping response {} [s]".format(time.perf_counter() - t0))
        return time.perf_counter() - t0

    @ping.handler
    async def ping(self):
        # plog.debug(self.log_prefix + "Ping received")
        await self.pong()

    @network_command(5)
    async def pong(self):
        """
        Sends a pong back to the remote that requested the ping.

        """
        plog.debug(self.log_prefix + "Pong")
        await self.transmit_pong()

    @pong.handler
    async def pong(self):
        self.ping_semaphore.release()


