"""
Channel Class
Handles and retransmits data in between ports.
"""

from asyncio import shield, wait, wait_for, ensure_future

from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.output import OutputPortDescriptorInstance, OutputPort
from urban_journey.pubsub.ports.input import InputPortDescriptorInstance, InputPort
from urban_journey import event_loop


class Channel:
    def __init__(self, name, timeout=5):
        self.name = name
        self.output_list = []
        self.input_list = []
        self.timeout = timeout
        self.loop = event_loop.get()

    def add_port(self, port):
        if isinstance(port, (OutputPortDescriptorInstance, OutputPort)):
            self.output_list.append(port)
            port.set_channel(self)
        elif isinstance(port, (InputPortDescriptorInstance, InputPort)):
            self.input_list.append(port)
            port.set_channel(self)
        else:
            raise TypeError()

    async def flush(self, data):
        print_channel_transmit("Channel.flush({})".format(data))
        for i, port in enumerate(self.input_list):
            ensure_future(wait_for(port.flush(data), self.timeout), loop=self.loop)
