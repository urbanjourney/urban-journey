from urban_journey.ujml.exceptions import ReadOnlyAttributeError
from urban_journey.ujml.unique import Required

from urban_journey.ujml.exceptions import RequiredAttributeError
from urban_journey.ujml.node_base import NodeBase

import inspect

from abc import ABCMeta, abstractmethod


class AttributeBaseClass(metaclass=ABCMeta):
    def __init__(self, name=None, read_only=False, optional_value=Required):
        self.read_only = read_only
        self.attrib_name = name
        self.optional_value = optional_value

    @abstractmethod
    def get(self, instance: NodeBase, owner):
        """This function should be overridden by child classes and returns the attribute value"""
        pass

    def set(self, instance: NodeBase, value):
        """This class can optionally be overridden by child classes and should set the attribute value. If not
        overridden the attribute will be readonly."""
        instance.raise_exception(ReadOnlyAttributeError, self.attrib_name)

    def get_optional(self, instance: NodeBase):
        if self.optional_value is not Required:
            return self.optional_value
        else:
            instance.raise_exception(RequiredAttributeError, instance.tag, self.attrib_name)

    # I think this one is useless, I'll remove it after I'm sure.
    # def check_for_optional(self, instance: NodeBase, owner, val):
    #     if val is None:
    #         if self.optional_value is not Required:
    #             return self.optional_value
    #         else:
    #             instance.raise_exception(RequiredAttributeError, instance.tag, self.attrib_name)
    #     return val

    def get_attribute_name(self, instance: NodeBase):
        for attr in dir(instance):
            if inspect.getattr_static(instance, attr) is self:
                self.attrib_name = attr

    def __get__(self, instance: NodeBase, owner):
        if self.attrib_name is None:
            self.get_attribute_name(instance)
        return self.get(instance, owner)

    def __set__(self, instance: NodeBase, value):
        if self.attrib_name is None:
            self.get_attribute_name(instance)
        if self.read_only:
            instance.raise_exception(ReadOnlyAttributeError, self.attrib_name)
        else:
            self.set(instance, value)
