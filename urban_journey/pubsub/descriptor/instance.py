from urban_journey.common.cached import cached


class DescriptorInstance:
    """Not a descriptor itself. But the base class for types returned by DescriptorStatic."""
    def __init__(self, parent_object, attribute_name, static_descriptor):
        super().__init__()
        self.__parent_object = parent_object
        self.__attribute_name = attribute_name
        self.__static_descriptor = static_descriptor

    @cached
    def parent_object(self):
        return self.__parent_object

    @cached
    def attribute_name(self):
        return self.__attribute_name

    @cached
    def static_descriptor(self):
        return self.__static_descriptor
