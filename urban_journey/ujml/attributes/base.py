from urban_journey.ujml.exceptions import ReadOnlyAttributeError
from urban_journey.ujml.unique import Required

from urban_journey.ujml.exceptions import RequiredAttributeError

import inspect

from abc import ABCMeta, abstractmethod


class AttributeBaseClass(metaclass=ABCMeta):
    def __init__(self, name=None, read_only=False, optional_value=Required):
        self.read_only = read_only
        self.attrib_name = name
        self.optional_value = optional_value

    @abstractmethod
    def get(self, instance, owner):
        """This function should be overridden by child classes and returns the attribute value"""
        pass

    def set(self, instance, value):
        """This class can optionally be overridden by child classes and should set the attribute value. If not
        overridden the attribute will be readonly."""
        instance.raise_exception(ReadOnlyAttributeError, self.attrib_name)

    def get_optional(self, instance):
        if self.optional_value is not Required:
            return self.optional_value
        else:
            instance.raise_exception(RequiredAttributeError, instance.tag, self.attrib_name)

    def get_attribute_name(self, instance):
        for attr in dir(instance):
            if inspect.getattr_static(instance, attr) is self:
                self.attrib_name = attr

    def __get__(self, instance, owner):
        if self.attrib_name is None:
            self.get_attribute_name(instance)
        return self.get(instance, owner)

    def __set__(self, instance, value):
        if self.attrib_name is None:
            self.get_attribute_name(instance)
        if self.read_only:
            instance.raise_exception(ReadOnlyAttributeError, self.attrib_name)
        else:
            self.set(instance, value)
