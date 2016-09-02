"""

"""
from urban_journey.debug import print_channel_transmit
from urban_journey.pubsub.ports.base import PortBase, PortDescriptorBase
from urban_journey.pubsub.trigger import Trigger
from urban_journey.pubsub.descriptor.instance import DescriptorInstance
from urban_journey.pubsub.descriptor.static import DescriptorStatic


from asyncio import wait_for, wait, shield


class InputPort(PortBase, DescriptorInstance, Trigger):
    def __init__(self, parent_object, attribute_name, channel_name=None, time_out=5):
        PortBase.__init__(self, parent_object.channel_register, attribute_name, channel_name)
        DescriptorInstance.__init__(self, parent_object, attribute_name)
        Trigger.__init__(self)
        self.time_out = time_out

    async def flush(self, data):
        await self.trigger(data)

    async def trigger(self, data, *args, **kwargs):
        print_channel_transmit("InputPort.trigger({})".format(data))
        futures = [None] * len(self._activities)
        for i, activity in enumerate(self._activities):
            futures[i] = activity.trigger((self, {self.attribute_name: data}), self.parent_object, *args, **kwargs)
        await wait_for(shield(wait(futures)), self.time_out)


class InputPortStatic(PortDescriptorBase, Trigger):
    def __init__(self, channel_name=None):
        DescriptorStatic.__init__(self, InputPort)
        Trigger.__init__(self)
        self.channel_name = channel_name

    def add_obj(self, obj):
        t = self.instances_base_class(obj,
                                      self._attribute_name,
                                      *self._instance_args,
                                      channel_name=self.channel_name,
                                      **self._instance_kwargs)
        self.instances[id(obj)] = t
        for activity in self._activities:
            t.add_activity(activity)

    def add_activity(self, activity):
        super().add_activity(activity)
        for _, t in self.instances.items():
            t.add_activity(activity)

    def trigger(self, s):
        for _, t in self.instances.items():
            # TODO: Fix this.
            # This will cause an error. But I'll deal with that later.
            t.trigger(None)
