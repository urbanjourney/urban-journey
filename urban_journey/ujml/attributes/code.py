from collections import defaultdict

from urban_journey.ujml.unique import Required
from urban_journey.ujml.interpreter import UJMLPythonSource
from urban_journey.ujml.attributes.base import AttributeBaseClass


class Exec(AttributeBaseClass):
    """
    Compiles the attribute's content as python code and stores it so it can be called later.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param optional_value: Optional code to execute in case the attribute wasn't given.
    """

    def __init__(self, name=None, optional_value=Required):
        super().__init__(name, True, optional_value)

    def get(self, instance, _):
        return UJMLPythonSource(instance.root.interpreter,
                                instance.element.get(self.attrib_name) or self.get_optional(instance),
                                instance.file_name,
                                'exec',
                                instance.source_line)


class Eval(AttributeBaseClass):
    """
    Evaluates the attribute's content as python code and returns the result.

    :param name: Name of the attribute in ujml. Default is same as the class attribute.
    :param optional_value: Optional code to evaluate in case the attribute wasn't given.
    """
    def __init__(self, name=None, optional_value=Required):
        super().__init__(name, True, optional_value)
        self.code = defaultdict(type(None))
        self.uncached = True

    def get(self, instance, owner):
        if self.code[instance] is None:
            self.code[instance] = UJMLPythonSource(instance.root.interpreter,
                                                   instance.element.get(self.attrib_name) or self.get_optional(instance),
                                                   instance.file_name,
                                                   'eval',
                                                   instance.source_line)
        value = self.code[instance]()
        return value
