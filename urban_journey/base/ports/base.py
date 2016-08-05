
class PortBase:
    def __init__(self):
        super().__init__()
        self.channel = None

    def set_channel(self, channel):
        self.channel = channel

