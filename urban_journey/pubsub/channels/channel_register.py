"""
Creates and destroys channels as needed and keeps a record of all currently living channels.
"""
from urban_journey.pubsub.channels.channel import Channel


class ChannelRegister:
    def __init__(self):
        self._channels = {}

    def get_channel(self, channel_name):
        if channel_name not in self._channels:
            self.create_channel(channel_name)
        return self._channels[channel_name]

    def create_channel(self, channel_name):
        print("Creating channel:", channel_name)
        self._channels[channel_name] = Channel(channel_name)
