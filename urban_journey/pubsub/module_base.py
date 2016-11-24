import inspect

from urban_journey.pubsub.trigger import TriggerBase
from urban_journey.common.cached import cached_class
from urban_journey.pubsub.activity import ActivityBase
from urban_journey.pubsub.ports.base import PortDescriptorBase
from urban_journey.pubsub.descriptor.static import DescriptorStatic


class ModuleBase:
    def __init__(self, channel_register=None):
        self.channel_register = channel_register
        """
        Variable holding an :class:`urban_journey.ChannelRegister` object. The ports will look in this channel register
        for channels when subscribing
        """
        self.__initialize_descriptors()
        self.channel_names = {}
        """
        Dictionary containing alternative channel names for the ports to subscribe to. It can be used to
        programmatically change the channel name before calling :func:`subscribe`
        """

    def subscribe(self):
        """Subscribes all ports to the channels."""
        for port_name in self.ports:
            getattr(self, port_name).subscribe(
                self.channel_names[port_name] if port_name in self.channel_names else None)

    def unsubscribe(self):
        """Unsubscribes all ports."""
        for port_name in self.ports:
            getattr(self, port_name).unsubscribe()

    def __initialize_descriptors(self):
        """Initializes the DescriptorInstance instances in this object."""
        # I'm not sure whether this function has an effect. Descriptors are initialized when they are first requested
        # anyways. I probably had a reason why some descriptors had to be initialized during initialization back when I
        # made this function. - Aaron
        klass = type(self)
        for member_name in dir(klass):
            member = inspect.getattr_static(klass, member_name)
            if isinstance(member, DescriptorStatic):
                getattr(self, member_name)

        # for member_name in dir(self):
        #     getattr(self, member_name)

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
            if isinstance(member, TriggerBase):
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
