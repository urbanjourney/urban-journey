from urban_journey.base.ports.base import PortBase


class OutputPort(PortBase):
    def __init__(self):
        super().__init__()
        self.data = None

    async def flush(self):
        await self.channel.flush(self.data)
