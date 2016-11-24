"""
WARNING: Before continuing make sure you know what a python descriptor is.
"""
import inspect


class DescriptorStatic:
    """
    Descriptor that returns instances of DescriptorInstance for each individual object using this descriptor.
    """

    def __init__(self, instances_base_class, *args, **kwargs):
        super().__init__()
        self.instances = {}
        self.instances_base_class = instances_base_class
        self._attribute_name = None

        self._instance_args = args
        self._instance_kwargs = kwargs

    def __get__(self, obj, klass=None):
        if obj is None:
            return self

        # If being called from Class, return instance
        if obj is None:
            return self

        # If the attribute name is still unknown find it.
        if self._attribute_name is None:
            self.find_attribute_name(klass)

        # If this is the first call from this object register it.
        if id(obj) not in self.instances:
            self.add_obj(obj)

        # Return the instance of DescriptorInstance corresponding to obj.
        return self.instances[id(obj)]

    def find_attribute_name(self, klass):
        for member_name in dir(klass):
            member = inspect.getattr_static(klass, member_name)
            if member is self:
                self._attribute_name = member_name

    def add_obj(self, obj):
        self.instances[id(obj)] = self.instances_base_class(obj,
                                                            self._attribute_name,
                                                            self,
                                                            *self._instance_args,
                                                            **self._instance_kwargs)


if __name__ == "__main__":
    pass
