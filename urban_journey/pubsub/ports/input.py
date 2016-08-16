"""

"""

from urban_journey.base.ports.base import PortBase
from urban_journey.base.trigger import DescriptorClassTriggerBase, Trigger
from urban_journey.base.descriptor.instance import DescriptorInstance
from urban_journey.base.descriptor.static import DescriptorStatic


from asyncio import wait_for, wait, shield


class InputPort(PortBase, DescriptorInstance, Trigger):
    def __init__(self, parent_object, attribute_name, channel_name=None, auto_connect=True, time_out=5):
        print(parent_object, attribute_name, channel_name, auto_connect)
        PortBase.__init__(self, parent_object, attribute_name, channel_name, auto_connect)
        DescriptorInstance.__init__(self, parent_object, attribute_name)
        Trigger.__init__(self)
        self.time_out = time_out

    async def flush(self, data):
        await self.trigger(data)

    async def trigger(self, data, *args, **kwargs):
        print("InputPort.trigger({})".format(data))
        futures = [None] * len(self._activities)
        print(self._activities)
        for i, activity in enumerate(self._activities):
            futures[i] = activity.trigger((self, {self.attribute_name: data}), self.parent_object, *args, **kwargs)
        await wait_for(shield(wait(futures)), self.time_out)


class InputPortStatic(DescriptorStatic, Trigger):
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