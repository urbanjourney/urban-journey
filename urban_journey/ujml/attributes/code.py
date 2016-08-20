import builtins
from urban_journey.ujml.interpreter import UJMLPythonSource
from urban_journey.ujml.attributes.base import AttributeBaseClass


class Exec(AttributeBaseClass):
    """
    Compiles the attribute's content as python code and stores it so it can be called later.
    """

    def __init__(self, name=None):
        super().__init__(name, True)
        self.code = None

    def get(self, instance, _):
        if self.code is None:
            try:
                self.code = UJMLPythonSource(instance.root.interpreter,
                                             instance.element.get(self.attrib_name),
                                             instance.file_name,
                                             'exec',
                                             instance.source_line)
            except Exception as e:
                import sys
                raise type(e)(builtins.str(e) +
                              '    File {}, line {}'.format(instance.file_name,
                                                            instance.source_line)).with_traceback(sys.exc_info()[2])
        return self.code


class Eval(AttributeBaseClass):
    """Evaluates the attribute's content as python code and return the result."""
    def __init__(self, name=None):
        super().__init__(name, True)

    def get(self, instance, owner):
        return instance.eval(instance.element.get(self.attrib_name))
