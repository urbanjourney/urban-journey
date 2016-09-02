from collections import OrderedDict

from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.base import PortBase, PortDescriptorBase
from urban_journey.pubsub.descriptor.instance import DescriptorInstance


def Output(channel_name=None):
    return PortDescriptorBase(OutputPort,
                              channel_name=channel_name)


class OutputPort(PortBase, DescriptorInstance):
    def __init__(self,
                 parent_object,
                 attribute_name,
                 channel_name=None):
        """
        :param parent_object: ModelBase instance that owns this port
        :param attribute_name: Name of this port inside the model as instance
        :param channel_name: Optional. Channel name to connect to. If None, attribute name will be used as channel_name.
        """

        PortBase.__init__(self, parent_object.channel_register, attribute_name, channel_name)
        DescriptorInstance.__init__(self, parent_object, attribute_name)

        self.data = OutputDataHolder(self)

    async def flush(self):
        print_channel_transmit("OutputPort.flush({})".format(self.data.data))
        if self.channel is not None:
            await self.channel.flush(self.data.data)


class OutputDataHolder:
    def __init__(self, port):
        self.__flushed = True
        self.data = OrderedDict()
        self.__port = port

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.__flushed = False
        self.data[key] = value

    async def flush(self):
        if not self.__flushed:
            await self.__port.flush()
            self.data = OrderedDict()
            self.__flushed = True
