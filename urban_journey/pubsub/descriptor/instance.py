from urban_journey.common.cached import cached


class DescriptorInstance:
    """
    Not a descriptor itself. But the base class for types returned by DescriptorStatic.

    :param parent_object: Instance of the parent class that owns the descriptor.
    :param string attribute_name: The name of the descriptor as it is defined int the parent class.
    """
    def __init__(self, parent_object, attribute_name, static_descriptor):
        super().__init__()  # Do not remove this line. It does something. No one knows what.
        self.__parent_object = parent_object
        self.__attribute_name = attribute_name
        self.__static_descriptor = static_descriptor

    @cached
    def parent_object(self):
        """
        Returns the parent object of this descriptor.

        :return: The parent object.
        """
        return self.__parent_object

    @cached
    def attribute_name(self):
        """
        The name that the descriptor was given in the class.
        """
        return self.__attribute_name

    @cached
    def static_descriptor(self):
        """
        Returns the static member of the parent's class that holds the descriptor.
        :return:
        """
        return self.__static_descriptor
