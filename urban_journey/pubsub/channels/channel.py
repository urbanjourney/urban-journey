
from asyncio import wait_for, ensure_future

from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.output import OutputPortDescriptorInstance, OutputPort
from urban_journey.pubsub.ports.input import InputPortDescriptorInstance, InputPort
from urban_journey import event_loop


class Channel:
    """
    The channel class transmits data between input and output ports.

    :param string name: Name of the channel.
    :param float timeout: Time out for input channels.
    """
    def __init__(self, name, timeout=5):
        self.name = name  #: Channel name.
        self.output_list = []  #: List of output ports.
        self.input_list = []  #: List of input ports.
        self.timeout = timeout  #: Time-out for input ports.
        self.loop = event_loop.get()  #: The main event loop.

    def add_port(self, port):
        """
        Subscribe either an input or output port the the channel.
        :param port: The port to be subsribed.
        :type port: urban_journey.PortBase
        """
        # Check the type of the port and add it to the appropriate list.
        if isinstance(port, (OutputPortDescriptorInstance, OutputPort)):
            self.output_list.append(port)
            port.set_channel(self)
        elif isinstance(port, (InputPortDescriptorInstance, InputPort)):
            self.input_list.append(port)
            port.set_channel(self)
        else:
            raise TypeError()

    def remove_port(self, port):
        if port in self.output_list:
            self.output_list.remove(port)
        elif port in self.input_list:
            self.input_list.remove(port)
        else:
            raise Exception("Port not subscribed to channel.")

    async def flush(self, data):
        """
        Flushes the data to all registered input ports.
        :param data: The data to be flushed.
        """
        print_channel_transmit("Channel.flush({})".format(data))
        for i, port in enumerate(self.input_list):
            # We don't want this function to block until all ports
            # have processed the data or timed-out. So instead we create the futures and
            # ensure it on the event loop.
            ensure_future(wait_for(port.flush(data), self.timeout), loop=self.loop)
