from urban_journey.common.cached import cached
from urban_journey.pubsub.descriptor.static import DescriptorStatic


class PortBase:
    def __init__(self, channel_register, attribute_name, channel_name):
        self.channel = None
        self.channel_register = channel_register
        self.input_channel_name = channel_name
        self.__attribute_name = attribute_name

    def subscribe(self, channel_name=None):
        self.unsubscribe()
        channel = self.channel_register.get_channel(channel_name or self.input_channel_name or self.attribute_name)
        channel.add_port(self)

    def unsubscribe(self):
        # TODO: Implement port unsubscribe. Return without exceptions when not subscribed.
        pass

    @cached
    def attribute_name(self):
        return self.__attribute_name

    @property
    def channel_name(self):
        return self.channel.name

    def set_channel(self, channel):
        self.channel = channel


class PortDescriptorBase(DescriptorStatic):
    pass
