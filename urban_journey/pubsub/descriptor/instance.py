from urban_journey.common.cached import cached


class DescriptorInstance:
    """Not a descriptor itself. But the base class for types returned by DescriptorStatic."""
    def __init__(self, parent_object, attribute_name):
        super().__init__()
        self.__parent_object = parent_object
        self.__attribute_name = attribute_name

    @cached
    def parent_object(self):
        return self.__parent_object

    @cached
    def attribute_name(self):
        return self.__attribute_name
