"""
Base classes for triggers.
WARNING: I don't know exactly how to explain how these work. It's kinda simple when understood. Before continuing make
sure you know what a descriptor is in python. Then continue on reading the rest of the documentation here.
"""
from urban_journey.common.cached import cached


class Trigger:
    """Base class for all triggers"""
    def __init__(self):
        self._activities = []

    def add_activity(self, activity):
        """Subscribe an activity to this trigger."""
        self._activities.append(activity)

    def trigger(self, *args, **kwargs):
        """Trigger all activities subscribed to this trigger."""
        for activity in self._activities:
            activity.trigger(*args, **kwargs)


class DescriptorClassTrigger(Trigger):
    """
    Descriptor holding a trigger instance for each instance of a model class that uses a descriptor trigger. When called
    it returns the trigger instance corresponding to the model instance that requested it.
    """

    def __init__(self, klass):
        super().__init__()
        self.triggers = {}
        self.trigger_base_class = klass

    @cached
    def obj_id(self):
        return id(self)

    def __get__(self, obj, klass=None):
        if obj is None:
            return self
        # TODO: Add type check here.
        # If there is an attribute error on the following line, then you have probably forgotten to inherit from
        # 'ModelBase' or a child thereof. I tried to place a check here for this but had issues with circular imports,
        # So I had to remove it. I'll fix it later.
        # It will also crash is for some reason someone changes the name of the 'ModuleBase' class.
        if id(obj) not in self.triggers:
            self.add_obj(obj)
        return self.triggers[id(obj)]

    def add_obj(self, obj):
        t = self.trigger_class(obj)
        for activity in self._activities:
            t.add_activity(activity)
        self.triggers[id(obj)] = t

    def add_activity(self, activity):
        super().add_activity(activity)
        for _, t in self.triggers.items():
            t.add_activity(activity)

    def trigger(self):
        for _, t in self.triggers.items():
            t.trigger()

    @cached
    def trigger_class(self):
        """
        Factory function for DescriptorInstanceTrigger classes. It returns a DescriptorInstanceTrigger class that
        inherits from the trigger class it's parent DescriptorClassTrigger represents.
        :return:
        """

        # Check if the trigger class has defined __repr__. If not pass the fully qualified name of the class.
        if "__repr__" not in self.trigger_base_class.__dict__:
            base_name = "%s.%s" % (self.trigger_base_class.__module__, self.trigger_base_class.__name__)
        else:
            base_name = None

        class DescriptorInstanceTrigger(self.trigger_base_class):
            """Type used for all module instance specific trigger instance. It inherits the target trigger class."""
            def __init__(self, obj):
                super().__init__()
                self.__obj = obj

            def __repr__(self):
                # Return the __repr__ of the base class if it has defined it. Otherwise a default like one.
                if base_name is None:
                    return super().__repr__()
                return '<%s.%s object at %s>' % (
                    self.__class__.__module__,
                    '%s<%s>' % (self.__class__.__name__, base_name),
                    hex(id(self))
                )

            def trigger(self, *args, **kwargs):
                for activity in self._activities:
                    activity.trigger(self.__obj, *args, **kwargs)
        return DescriptorInstanceTrigger

if __name__ == "__main__":
    pass
