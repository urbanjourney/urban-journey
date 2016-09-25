import builtins
from urban_journey.ujml.attributes.base import AttributeBaseClass
from urban_journey.ujml.exceptions import InvalidAttributeValueError
from urban_journey.ujml.unique import Required
from urban_journey.common.cached import cached


class String(AttributeBaseClass):
    """
    String ujml attribute.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """
    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            return val_str

    def set(self, instance, x):
        instance.element.set(self.attrib_name, x)


class Int(AttributeBaseClass):
    """
    Integer ujml attribute.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """
    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            if val_str.isdigit():
                return int(val_str)
            else:
                instance.raise_exception(InvalidAttributeValueError, instance.tag, self.attrib_name)

    def set(self, instance, x):
        instance.element.set(self.attrib_name, "%d" % (x, ))


class Bool(AttributeBaseClass):
    """
    Boolean ujml attribute.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """
    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            val_str = val_str.lower()
            if val_str in ['true', 'false']:
                return val_str == "true"
            else:
                instance.raise_exception(InvalidAttributeValueError, instance.tag, self.attrib_name)

    def set(self, instance, x):
        instance.element.set(self.attrib_name, str(x))


class Float(AttributeBaseClass):
    """
    Float ujml attribute.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """
    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            try:
                return float(val_str)
            except ValueError:
                instance.raise_exception(InvalidAttributeValueError, instance.tag, self.attrib_name)

    def set(self, instance, x):
        instance.element.set(self.attrib_name,  str(x))


class List(AttributeBaseClass):
    """
    Comma separated list ujml attribute. The contents of the list are evaluated as python code.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.

    """
    def get(self, instance, owner):
            val_str = instance.element.get(self.attrib_name)
            if val_str is None:
                return self.get_optional(instance)
            else:
                return instance.eval("[{}]".format(val_str))


class FilePath(AttributeBaseClass):
    """
    File path ujml attribute. If a relative path was given by the user, this attribute will return an
    absolute path for a file relative to the ujml file.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param read_only: Mark attribute as read only.
    :param optional_value: Optional value in case the attribute wasn't given.
    """

    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            val_str = self.get_optional(instance)

        if val_str is None:
            return None

        return instance.abs_path(val_str)

    def set(self, instance, x):
        instance.element.set(self.attrib_name, x)
