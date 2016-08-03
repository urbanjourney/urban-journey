import inspect

from urban_journey.base.trigger import DescriptorClassTrigger
from urban_journey.common.cached import cached_class
from urban_journey.base.activity import ActivityBase


class ModuleBase:
    def __init__(self):
        pass

    @cached_class
    def activities(cls):
        """Property returning all statically declared activities."""
        al = []
        for member_name in dir(cls):
            member = inspect.getattr_static(cls, member_name)
            if isinstance(member, ActivityBase):
                al.append((member_name, member))
        return al

    @cached_class
    def triggers(cls):
        """Property returning all statically declared triggers."""
        tl = []
        for member_name in dir(cls):
            member = inspect.getattr_static(cls, member_name)
            if isinstance(member, DescriptorClassTrigger):
                tl.append((member_name, member))
        return tl
