import asyncio
from collections import OrderedDict

from urban_journey.event_loop import get as get_event_loop
from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.base import PortBase, PortDescriptorBase
from urban_journey.pubsub.descriptor.instance import DescriptorInstance


def Output(channel_name=None):
    return PortDescriptorBase(OutputPortDescriptorInstance,
                              channel_name=channel_name)


class OutputPort(PortBase):
    def __init__(self, channel_register, attribute_name, channel_name=None):
        super().__init__(channel_register, attribute_name, channel_name)

    async def flush(self, data):
        print_channel_transmit("OutputPort.flush({})".format(data))
        if self.channel is not None:
            await self.channel.flush(data)

    def flush_threadsafe(self, data):
        print_channel_transmit("OutputPort.flush_threadsafe({})".format(data))
        if self.channel is not None:
            loop = get_event_loop()
            asyncio.run_coroutine_threadsafe(self.channel.flush(data), loop)

    __call__ = flush


class OutputPortDescriptorInstance(OutputPort, DescriptorInstance):
    def __init__(self,
                 parent_object,
                 attribute_name,
                 static_descriptor,
                 channel_name=None):
        """
        :param parent_object: ModelBase instance that owns this port
        :param attribute_name: Name of this port inside the model as instance
        :param static_descriptor: Instance of the static descriptor that created this instance
        :param channel_name: Optional. Channel name to connect to. If None, attribute name will be used as channel_name.
        """

        OutputPort.__init__(self, parent_object.channel_register, attribute_name, channel_name)
        DescriptorInstance.__init__(self, parent_object, attribute_name, static_descriptor)

