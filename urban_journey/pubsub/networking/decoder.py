import umsgpack
from io import BytesIO
import struct
import asyncio
from urban_journey import event_loop


class Decoder:
    """
    This class is used to decode the incoming data into usable packages.
    """

    def __init__(self):
        self.state = 0
        """The current state of the decoder. If 0 it's reading the data length. If 1 it's reading the data."""
        self.buffer = BytesIO()  #: Buffer used to hold the data being read.
        self.block_read = 0  #: Number of bytes read in the current block.
        self.data_length = 0  #: The length of the current package being read.
        self.queue = asyncio.Queue(10, loop=event_loop.get())  #: Queue holding the packages received.
        self.get = self.queue.get
        self.get_nowait = self.queue.get_nowait

    async def digest(self, bts):
        """
        Processes an incoming byte array. If a full package was received, it will be put on the queue.

        :param bts: Bytes to be processed.
        """
        read = 0  # Number of bytes read.
        while read < len(bts):
            if self.state == 0:  # Reading message length
                dl = self.buffer.write(bts[read:(4 - self.block_read + read)])
                self.block_read += dl
                read += dl
                if self.block_read == 4:
                    self.data_length = struct.unpack(">I", self.buffer.getvalue())[0]
                    self.state = 1
                    self.block_read = 0
                    self.buffer.seek(0)
                    self.buffer.truncate()

            elif self.state == 1:  # Reading data block
                dl = self.buffer.write(bts[read:(self.data_length - self.block_read + read)])
                self.block_read += dl
                read += dl
                if self.block_read == self.data_length:
                    data = umsgpack.unpackb(self.buffer.getvalue())
                    await self.queue.put(data)
                    self.state = 0
                    self.block_read = 0
                    self.buffer.seek(0)
                    self.buffer.truncate()
