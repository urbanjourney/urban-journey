from urban_journey.ujml.attributes.base import AttributeBaseClass
from urban_journey.ujml.unique import Required

from datetime import datetime


class DateTime(AttributeBaseClass):
    """
    String ujml attribute.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """

    def __init__(self, name=None, optional_value=Required):
        super().__init__(name, True, optional_value)

    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            return datetime.strptime(val_str, "%d/%m/%Y %H:%M")
