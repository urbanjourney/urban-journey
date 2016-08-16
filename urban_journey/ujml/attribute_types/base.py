from dtst.dtsml.exceptions import ModifyingReadOnlyDTSMLAttributeError
from dtst.dtsml.required_placeholder import Required

from dtst.dtsml.exceptions import MissingRequiredAttributeError

import inspect


class AttributeBaseClass(object):
    def __init__(self, attrib_name=None, read_only=False, optional_value=Required):
        self.read_only = read_only
        self.attrib_name = attrib_name
        self.optional_value = optional_value

    def get(self, instance, owner):
        pass

    def set(self, instance, value):
        raise ModifyingReadOnlyDTSMLAttributeError(instance.sourceline, instance.dtsml.filename)

    def get_optional(self, instance):
        if self.optional_value is not Required:
            return self.optional_value
        else:
            raise MissingRequiredAttributeError(instance.dtsml.filename,
                                                instance.sourceline,
                                                instance.tag,
                                                self.attrib_name)

    def check_for_optional(self, instance, owner, val):
        if val is None:
            if self.optional_value is not Required:
                return self.optional_value
            else:
                raise MissingRequiredAttributeError(instance.dtsml.filename,
                                                    instance.sourceline,
                                                    instance.tag,
                                                    self.attrib_name)
        return val

    def get_attribute_name(self, instance, _):
        for attr in dir(instance):
            if id(inspect.getattr_static(instance, attr)) == id(self):
                self.attrib_name = attr
        assert self.attrib_name

    def __get__(self, instance, owner):
        if self.attrib_name is None:
            self.get_attribute_name(instance, owner)
        return self.get(instance, owner)

    def __set__(self, instance, value):
        if self.attrib_name is None:
            self.get_attribute_name(instance)
        if self.read_only:
            raise ModifyingReadOnlyDTSMLAttributeError(instance.sourceline, instance.dtsml.filename)
        else:
            self.set(instance, value)
