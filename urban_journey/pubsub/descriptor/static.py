"""
WARNING: Before continuing make sure you know what a python descriptor is.
"""
import inspect


class DescriptorStatic:
    """
    Descriptor that returns instances of DescriptorInstance for each individual object using this descriptor.

    :param type instances_base_class: Class that is used to create individual descriptor instances for each parent class
       instances.
    :param *args: Extra args to be passed to the `instances_base_class` when initializing it.
    :param **kwargs Extra kwargs to be passed to the `instances_base_class` when initializing it.
    """

    def __init__(self, instances_base_class, *args, **kwargs):
        # super().__init__()  # Do not remove this line. It does something. No one knows what.
        self.instances = {}  #: Dictionary mapping parent class instances with `instances_base_class` instances.
        self.instances_base_class = instances_base_class
        """
        Class that is used to create individual descriptor instances for each parent class instances.
        """

        self.attribute_name = None  #: Name of the descriptor.

        self._instance_args = args  #: Extra args to be passed to the `instances_base_class` when initializing it.
        self._instance_kwargs = kwargs  #: Extra kwargs to be passed to the `instances_base_class` when initializing it.

    def __get__(self, obj, klass=None):
        # If being called from Class, return instance
        if obj is None:
            return self

        # If the attribute name is still unknown find it.
        if self.attribute_name is None:
            self.find_attribute_name(klass)

        # If this is the first call from this object register it.
        if id(obj) not in self.instances:
            self.add_obj(obj)

        # Return the instance of DescriptorInstance corresponding to obj.
        return self.instances[id(obj)]

    def find_attribute_name(self, klass):
        """
        It finds the name of the descriptor as it is defined in the paret class.

        :param type klass: Parent class
        """
        # Loop through each member of the class and get it's static attribute.
        # This is necessary since descriptor are meant to override the default
        # behaviour of getattr(..)
        # If this instance is found get it's name.

        for member_name in dir(klass):
            member = inspect.getattr_static(klass, member_name)
            if member is self:
                self.attribute_name = member_name

    def add_obj(self, obj):
        """
        Creates a new instance of `instances_base_class` that corresponds to
        obj and add it to the instance dictionary.

        :param obj: Parent instance.
        """
        self.instances[id(obj)] = self.instances_base_class(obj,
                                                            self.attribute_name,
                                                            self,
                                                            *self._instance_args,
                                                            **self._instance_kwargs)


if __name__ == "__main__":
    pass
