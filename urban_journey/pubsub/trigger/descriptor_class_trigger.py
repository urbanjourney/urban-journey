"""
Base classes for triggers.
WARNING: I don't know exactly how to explain how these work.Before continuing make sure you know what a descriptor is \
in python. Then continue on reading the rest of the documentation here.
"""
from traceback import print_exception
import sys

from urban_journey.common.cached import cached
from urban_journey.pubsub.trigger import TriggerBase


class DescriptorClassTrigger(TriggerBase):
    """
    Descriptor holding a trigger instance for each instance of a model class that uses a descriptor trigger. When called
    it returns the trigger instance corresponding to the model instance that requested it.
    """

    def __init__(self, klass, is_descriptor_instance=False):
        super().__init__()
        self.triggers = {}
        self.trigger_base_class = klass
        self.is_descriptor_instance = is_descriptor_instance
        self._name = None

    @cached
    def obj_id(self):
        return id(self)

    def __get__(self, obj, klass=None):
        if obj is None:
            return self
        if self._name is None:
            for key in obj.triggers:
                if obj.triggers[key] == self:
                    self._name = key
                    break
        # TODO: Add type check here.
        # If there is an attribute error on the following line, then you have probably forgotten to inherit from
        # 'ModelBase' or a child thereof. I tried to place a check here for this but had issues with circular imports,
        # So I had to remove it. I'll fix it later.
        # It will also crash is for some reason someone changes the name of the 'ModuleBase' class.
        if id(obj) not in self.triggers:
            self.add_obj(obj)
        return self.triggers[id(obj)]

    def add_obj(self, obj):
        t = self.trigger_class(obj, self._name)
        for activity in self._activities:
            t.add_activity(activity)
        self.triggers[id(obj)] = t

    def add_activity(self, activity):
        super().add_activity(activity)
        for _, t in self.triggers.items():
            t.add_activity(activity)

    def trigger(self):
        for _, t in self.triggers.items():
            # This cause an error. But I'll deal with that later.
            t.trigger(None)

    @cached
    def trigger_class(self):
        if self.is_descriptor_instance:
            return self.trigger_base_class
        else:
            return trigger_factory(self.trigger_base_class)


def trigger_factory(klass):
    """
    Factory function for DescriptorInstanceTrigger classes. It returns a DescriptorInstanceTrigger class that
    inherits from the trigger class it's parent DescriptorClassTrigger represents.
    :return:
    """

    # Check if the trigger class has defined __repr__. If not pass the fully qualified name of the class.
    if "__repr__" not in klass.__dict__:
        base_name = "%s.%s" % (klass.__module__, klass.__name__)
    else:
        base_name = None

    class DescriptorInstanceTrigger(klass):
        """Type used for all module instance specific trigger instance. It inherits the target trigger class."""
        def __init__(self, obj, local_name):
            super().__init__()
            self.__obj = obj
            self.__local_name = local_name

        def __repr__(self):
            # Return the __repr__ of the base class if it has defined it. Otherwise a default like one.
            if base_name is None:
                return super().__repr__()
            return '<%s.%s object at %s>' % (
                self.__class__.__module__,
                '%s(%s)' % (self.__class__.__name__, base_name),
                hex(id(self))
            )

        async def trigger(self, *args, **kwargs):
            for activity in self._activities:
                # print(activity)
                try:
                    await activity.trigger([self], {}, self.__obj, *args, **kwargs)
                except:
                    print_exception(*sys.exc_info())
                    assert False

    return DescriptorInstanceTrigger

DescriptorClassTriggerBase = trigger_factory(TriggerBase)


if __name__ == "__main__":
    pass
