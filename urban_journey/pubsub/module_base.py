import inspect

from urban_journey.pubsub.trigger import Trigger
from urban_journey.common.cached import cached_class
from urban_journey.pubsub.activity import ActivityBase
from urban_journey.pubsub.ports.base import PortDescriptorBase


class ModuleBase:
    def __init__(self, channel_register=None):
        self.channel_register = channel_register
        self.initialize_descriptors()
        self.channel_names = {}

    def subscribe(self):
        for port_name in self.ports:
            getattr(self, port_name).subscribe(
                self.channel_names[port_name] if port_name in self.channel_names else None)

    def unsubscribe(self):
        for port_name in self.ports:
            getattr(self, port_name).unsubscribe()

    def initialize_descriptors(self):
        """Initializes the DescriptorInstance instances for this object."""
        for member_name in dir(self):
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
            if isinstance(member, Trigger):
                tl[member_name] = member
        return tl

    @cached_class
    def ports(cls) -> dict:
        """Property returning all statically declared ports."""
        ps = {}
        for member_name in dir(cls):
            member = inspect.getattr_static(cls, member_name)
            if isinstance(member, PortDescriptorBase):
                ps[member_name] = member
        return ps
