from urban_journey.common.cached import cached
from urban_journey.pubsub.descriptor.static import DescriptorStatic


class PortBase:
    """
    Base class for all ports.

    :param urban_journey.ChannelRegister: Channel register in which to register the port.
    :param string attribute_name: The name of the port.
    :param string channel_name: The name of the default channel to witch to subscribe the port
       to. If None, the attribute_name is used as the default channel name.
    """
    def __init__(self, channel_register, attribute_name, channel_name):
        self.channel = None  #: Channel to which this port is subscribed to.
        self.channel_register = channel_register  #: Channel register in which to register the port.
        self.default_channel_name = channel_name  #: Default channel name.

        self.attribute_name = attribute_name  #: The name of the port.

    def subscribe(self, channel_name=None):
        """
        Subscribe the port to a channel. If channel_name is ``None`` it will be subsribed to the default channel. If
        no default channel was given that the attribute_name will be used as the default channel name.
        :param channel_name:
        :return:
        """
        self.unsubscribe()
        channel = self.channel_register.get_channel(channel_name or self.default_channel_name or self.attribute_name)
        channel.add_port(self)

    def unsubscribe(self):
        """
        .. warning:: Not implemented

        Unsubscribes the port from whatever channel it's connected to.
        :return:
        """
        # TODO: Implement port unsubscribe. Return without exceptions when not subscribed.
        pass

    @property
    def channel_name(self):
        """
        The name of the channel this port is subscribed to. None if it's subscribed.
        """

        return self.channel.name if self.channel is not None else None

    def set_channel(self, channel):
        """
        .. warning:: Not implemented

        Swap the channel this port is subscribed to. Or subscribe to the channel.

        :param channel: Channel object.
        :return:
        """
        if self.channel is not None:
            self.channel.remove_port(self)
        self.channel = channel
        # self.channel = channel
        pass


class PortDescriptorBase(DescriptorStatic):
    pass
