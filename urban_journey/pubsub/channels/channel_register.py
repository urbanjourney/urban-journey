"""
Creates and destroys channels as needed and keeps a record of all currently living channels.
"""
from urban_journey.pubsub.channels.channel import Channel
from urban_journey.pubsub.networking.listener import Listener


class ChannelRegister:
    """
    The channel register keeps a list of all existing channels and creates
    a channel when necessary.

    It also keeps a list of all remote connections and listeners if existing.
    """
    def __init__(self):
        self.channels = {}  #: Dictionary holding the channels.
        self.connections = {}
        self.listeners = {}

    def new_listener(self, host, port):
        listener_name = "{}:{}".format(host, port)
        if listener_name not in self.listeners:
            listener = Listener(host, port, self.connections)
            self.listeners[listener_name] = listener

    def get_channel(self, channel_name):
        """
        Return the requested channel. If the channel does not exist yet it creates it.
        :param string channel_name: Name of the requested channel.
        :return: Requested channel object.
        """
        if channel_name not in self.channels:
            self.create_channel(channel_name)
        return self.channels[channel_name]

    def create_channel(self, channel_name):
        """
        Creates a new channel
        :param channel_name: The name of the new channel.
        """
        self.channels[channel_name] = Channel(channel_name)
