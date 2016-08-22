from collections import defaultdict

from urban_journey.ujml.interpreter import UJMLPythonSource
from urban_journey.ujml.attributes.base import AttributeBaseClass


class Exec(AttributeBaseClass):
    """
    Compiles the attribute's content as python code and stores it so it can be called later.
    """

    def __init__(self, name=None):
        super().__init__(name, True)

    def get(self, instance, _):
        return UJMLPythonSource(instance.root.interpreter,
                                instance.element.get(self.attrib_name),
                                instance.file_name,
                                'exec',
                                instance.source_line)


class Eval(AttributeBaseClass):
    """Evaluates the attribute's content as python code and return the result."""
    def __init__(self, name=None):
        super().__init__(name, True)
        self.code = defaultdict(type(None))
        self.uncached = True

    def get(self, instance, owner):
        if self.code[instance] is None:
            self.code[instance] = UJMLPythonSource(instance.root.interpreter,
                                                   instance.element.get(self.attrib_name),
                                                   instance.file_name,
                                                   'eval',
                                                   instance.source_line)
        value = self.code[instance]()
        return value
