"""
Channel Class
Handles and retransmits data in between ports.
"""

from asyncio import shield, wait, wait_for

from urban_journey.base.ports.output import OutputPort
from urban_journey.base.ports.input import InputPort


class Channel:
    def __init__(self, name, timeout=5):
        self.name = name
        self.output_list = []
        self.input_list = []
        self.timeout = timeout

    def add_port(self, port):
        if isinstance(port, OutputPort):
            self.output_list.append(port)
            port.set_channel(self)
        elif isinstance(port, InputPort):
            self.input_list.append(port)
            port.set_channel(self)
        else:
            raise TypeError()

    async def flush(self, data):
        futures = [None]*len(self.input_list)
        for i, port in enumerate(self.input_list):
            futures[i] = port.flush(data)
        await wait_for(shield(wait(futures)), self.timeout)
