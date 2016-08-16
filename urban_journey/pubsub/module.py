import inspect

from urban_journey.pubsub.trigger import DescriptorClassTrigger
from urban_journey.common.cached import cached_class
from urban_journey.pubsub.activity import ActivityBase
from urban_journey.pubsub.descriptor.static import DescriptorStatic


class ModuleBase:
    def __init__(self, channel_register=None):
        self.channel_register = channel_register
        self.initialize_descriptors()

    def initialize_descriptors(self):
        """Initializes the DescriptorInstance instances for this object."""
        for member_name in dir(self):
            member = inspect.getattr_static(self, member_name)
            if isinstance(member, DescriptorStatic):
                getattr(self, member_name)

    @cached_class
    def activities(cls):
        """Property returning all statically declared activities."""
        al = {}
        for member_name in dir(cls):
            member = inspect.getattr_static(cls, member_name)
            if isinstance(member, ActivityBase):
                al[member_name] = member
        return al

    @cached_class
    def triggers(cls):
        """Property returning all statically declared triggers."""
        tl = {}
        for member_name in dir(cls):
            member = inspect.getattr_static(cls, member_name)
            if isinstance(member, DescriptorClassTrigger):
                tl[member_name] = member
        return tl
