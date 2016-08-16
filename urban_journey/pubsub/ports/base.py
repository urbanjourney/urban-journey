from urban_journey.common.cached import cached


class PortBase:
    def __init__(self, parent_object, attribute_name, channel_name, auto_connect):
        self.channel = None
        self.__attribute_name = attribute_name

        if auto_connect:
            if parent_object.channel_register is not None:
                if channel_name is None:
                    channel = parent_object.channel_register.get_channel(attribute_name)
                else:
                    channel = parent_object.channel_register.get_channel(channel_name)
                channel.add_port(self)
            else:
                raise ValueError("ModelBase object has no channel_register assigned to it.")

    @cached
    def attribute_name(self):
        return self.__attribute_name

    @property
    def channel_name(self):
        return self.channel.name

    def set_channel(self, channel):
        self.channel = channel
