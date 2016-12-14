import umsgpack
from io import BytesIO
import struct
import asyncio
from urban_journey import event_loop


restricted_allowed_data_length = 1024


class Decoder:
    """
    This class is used to decode the incoming data into usable packages.

    :param error_callback: A Callable that is called whenever an error occurs while decoding the data.
    :param loop: Event loop on which to run the internal queue holding the decoded packages.
    """

    def __init__(self, error_callback=None, loop=None):
        self.state = 0
        """The current state of the decoder. If 0, it's reading the data length. If 1, it's reading the data."""

        self.error_callback = error_callback  #: Function that is called whenever an error occurs decoding the data.
        self.buffer = BytesIO()  #: Buffer used to hold the data being read.
        self.block_read = 0  #: Number of bytes read in the current block.
        self.data_length = 0  #: The length of the current package being read.
        self.queue = asyncio.Queue(10, loop=loop or event_loop.get())  #: Queue holding the packages received.
        self.get = self.queue.get
        self.get_nowait = self.queue.get_nowait

        self.restricted = True
        """
        If ``True`` this means that the decoder is running in restricted mode.
        In the restricted mode the decoder only allows packages big enough for
        the handshake packages.
        """

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
                    if self.restricted and self.data_length > restricted_allowed_data_length:
                        if self.error_callback is not None:
                            self.error_callback()
                            break

            elif self.state == 1:  # Reading data block
                dl = self.buffer.write(bts[read:(self.data_length - self.block_read + read)])
                self.block_read += dl
                read += dl
                if self.block_read == self.data_length:
                    try:
                        data = umsgpack.unpackb(self.buffer.getvalue())

                        if (len(data) != 2) or \
                           (not isinstance(data[0], int)) or \
                           (not isinstance(data[1], list)):

                            if self.error_callback is not None:
                                self.error_callback()
                            break
                    except:
                        if self.error_callback is not None:
                            self.error_callback()
                        break

                    await self.queue.put(data)
                    self.state = 0
                    self.block_read = 0
                    self.buffer.seek(0)
                    self.buffer.truncate()
