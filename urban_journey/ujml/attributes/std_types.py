import builtins
from urban_journey.ujml.attributes.base import AttributeBaseClass
from urban_journey.ujml.exceptions import InvalidAttributeValueError


class string_t(AttributeBaseClass):
    """
    String ujml attribute descriptor.
    """
    def get(self, instance, owner):
        val_str = instance.element.get(self.attrib_name)
        if val_str is None:
            return self.get_optional(instance)
        else:
            return val_str

    def set(self, instance, x):
        instance.element.set(self.attrib_name, x)


class int_t(AttributeBaseClass):
    """
    Integer ujml attribute descriptor.
    """
    def get(self, instance, owner):
        try:
            val_str = instance.element.get(self.attrib_name)
            if val_str is None:
                return self.get_optional(instance)
            else:
                return int(val_str)
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])

    def set(self, instance, x):
        try:
            instance.element.set(self.attrib_name, builtins.str(builtins.int(x)))
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])


class bool_t(AttributeBaseClass):
    """
    Boolean ujml attribute descriptor.
    """
    def get(self, instance, owner):
        try:
            val_str = instance.element.get(self.attrib_name)
            if val_str is None:
                return self.get_optional(instance)
            else:
                val_str = val_str.lower()
                if val_str in ['true', 'false']:
                    return val_str == "true" if val_str in ['true', 'false'] else \
                        instance.raise_exception(InvalidAttributeValueError, instance.tag, self.attrib_name)
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])

    def set(self, instance, x):
        try:
            instance.element.set(self.attrib_name, builtins.str(builtins.bool(x)))
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])


class float_t(AttributeBaseClass):
    """
    Float ujml attribute descriptor.
    """
    def get(self, instance, owner):
        try:
            val_str = instance.element.get(self.attrib_name)
            if val_str is None:
                return self.get_optional(instance)
            else:
                return float(val_str)
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])

    def set(self, instance, x):
        try:
            instance.element.set(self.attrib_name, builtins.str(builtins.float(x)))
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])


class list_t(AttributeBaseClass):
    """
    List ujml attribute descriptor. The contents of the list are evaluated as python code.
    """
    def get(self, instance, owner):
        try:
            val_str = instance.element.get(self.attrib_name)
            if val_str is None:
                return self.get_optional(instance)
            else:
                return eval("[{}]".format(val_str))
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])

    def set(self, instance, x):
        try:
            instance.element.set(self.attrib_name, builtins.str(builtins.float(x)))
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '\n    File {}, line {}'.format(instance.file_name,
                                                          instance.source_line)).with_traceback(sys.exc_info()[2])
