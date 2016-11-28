"""

"""
from traceback import print_exception
import sys

# from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.base import PortBase, PortDescriptorBase
from urban_journey.pubsub.trigger import TriggerBase
from urban_journey.pubsub.descriptor.instance import DescriptorInstance
from urban_journey.pubsub.descriptor.static import DescriptorStatic
import logging

from asyncio import wait_for, wait, shield


ctlog = logging.getLogger('channels_transmission')


class InputPort(PortBase, TriggerBase):
    """
    This class can be used to create a new input port dynamically after
    the parent module has initialized.

    :param urban_journey.ModuleBase parent_object: Paren module that will own this port.
    :param string attribute_name: The name of the port.
    :param string channel_name: The default channel name. If None `attribute_name` is used.
    :param float time_out: Timeout on the processing time.
    """
    def __init__(self, parent_object, attribute_name, channel_name=None, time_out=5):
        PortBase.__init__(self, parent_object.channel_register, attribute_name, channel_name)
        TriggerBase.__init__(self)
        self.parent_object = parent_object  #: The parent module object.
        self.time_out = time_out  #: Time out

    async def flush(self, data):
        """
        Receives the data coming in from the channel.

        :param data: The data being transmitted.
        """
        await self.trigger(data)

    async def trigger(self, data, *args, **kwargs):
        """
        Triggers all activities connected to his port.

        :param data: The data being transmitted.
        :param args:  Random stuff
        :param kwargs: More random stuff
        """
        ctlog.debug("InputPort.trigger({})".format(data))
        # Only transmit the data if there are activities connected to this port.
        if len(self._activities):
            futures = [None] * len(self._activities)
            for i, activity in enumerate(self._activities):
                futures[i] = activity.trigger([self], {self.attribute_name: data}, self.parent_object, *args, **kwargs)

            try:
                # TODO: This will stop calling modules as soon as one raises an exception. Figure out a way to handle
                #       exceptions individually for each future.
                await wait_for(shield(wait(futures)), self.time_out)
            except Exception as e:
                self.parent_object.root.handle_exception(sys.exc_info())


class InputPortDescriptorInstance(InputPort, DescriptorInstance):
    """
    Class used to create input port instances for static/descriptor defined port.

    :param urban_journey.ModuleBase parent_object: Paren module that will own this port.
    :param string attribute_name: The name of the port.
    :param string channel_name: The default channel name. If None `attribute_name` is used.
    :param float time_out: Timeout on the processing time.
    """

    def __init__(self, parent_object, attribute_name, static_descriptor, channel_name=None, time_out=5):
        InputPort.__init__(self, parent_object, attribute_name, channel_name, time_out)
        DescriptorInstance.__init__(self, parent_object, attribute_name, static_descriptor)


class InputPortStatic(PortDescriptorBase, TriggerBase):
    """
    Class used to statically declare ports using a descriptor.

    :param string channel_name: Default channel to connect to. If None, the descriptor/attribute name is used.
    """
    def __init__(self, channel_name=None):
        DescriptorStatic.__init__(self, InputPortDescriptorInstance)
        TriggerBase.__init__(self)
        self.channel_name = channel_name

    def add_obj(self, obj):
        """
        Creates a new instance of `instances_base_class` that corresponds to
        obj and adds it to the instance dictionary.

        :param obj: Parent instance.
        """
        t = self.instances_base_class(obj,
                                      self.attribute_name,
                                      self,
                                      *self._instance_args,
                                      channel_name=self.channel_name,
                                      **self._instance_kwargs)
        self.instances[id(obj)] = t
        for activity in self._activities:
            t.add_activity(activity)

    def add_activity(self, activity):
        """
        Connects a new activity to this port.

        :param urban_journey.ActivityBase activity: Activity to connect.
        """
        super().add_activity(activity)
        for _, t in self.instances.items():
            t.add_activity(activity)

    def remove_activity(self, activity):
        """
        Disconnects a activity from this port.

        :param urban_journey.ActivityBase activity: Activity to disconnect.
        """
        super().remove_activity(activity)
        for _, t in self.instances.items():
            t.remove_activity(activity)

    def trigger(self, s):
        """
        .. warning:: Not implemented.
        :param s:
        :return:
        """
        for _, t in self.instances.items():
            # TODO: Fix this.
            # This will cause an error. But I'll deal with that later.
            # But this shouldn't happen anyways.
            t.trigger(None)
