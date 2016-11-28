import asyncio

from urban_journey.event_loop import get as get_event_loop
# from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.base import PortBase, PortDescriptorBase
from urban_journey.pubsub.descriptor.instance import DescriptorInstance
import logging


ctlog = logging.getLogger('channels_transmission')


def Output(channel_name=None):
    """
    Returns the class used to statically declare ports using a descriptor.

    :param string channel_name: Default channel to connect to. If None, the descriptor/attribute name is used.
    """
    return PortDescriptorBase(OutputPortDescriptorInstance,
                              channel_name=channel_name)


class OutputPort(PortBase):
    """
    This class can be used to create a new output port dynamically after
    the parent module has initialized. This object object is callable.

    :param urban_journey.ModuleBase parent_object: Paren module that will own this port.
    :param string attribute_name: The name of the port.
    :param string channel_name: The default channel name. If None `attribute_name` is used.
    """
    def __init__(self, channel_register, attribute_name, channel_name=None):
        super().__init__(channel_register, attribute_name, channel_name)

    async def flush(self, data):
        """
        Flushed out the data to the channel.

        :param data: Data to flush.
        """
        ctlog.debug("OutputPort.flush({})".format(data))
        if self.channel is not None:
            await self.channel.flush(data)

    def flush_threadsafe(self, data):
        """
        Thread safe version of flush.

        :param data: Data to flush.
        """
        ctlog.debug("OutputPort.flush_threadsafe({})".format(data))
        if self.channel is not None:
            loop = get_event_loop()
            asyncio.run_coroutine_threadsafe(self.channel.flush(data), loop)

    __call__ = flush


class OutputPortDescriptorInstance(OutputPort, DescriptorInstance):
    """
        Class used to create input port instances for static/descriptor defined port.

        :param urban_journey.ModuleBase parent_object: Parent module that will own this port.
        :param string attribute_name: The name of the port.
        :param static_descriptor: Instance of the static descriptor that created this instance
        :param string channel_name: The default channel name. If None `attribute_name` is used.
        """
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
