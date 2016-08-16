import builtins
from urban_journey.ujml.python_interpreter import DTSMLPythonSourceClass
from urban_journey.ujml.attribute_types.base import AttributeBaseClass
from urban_journey.common.code_formatting import python_pre_process


class Exec(AttributeBaseClass):
    """
    Compiles the attribute's content as python code and stores it so it can be called later.
    """

    def __init__(self, attrib_name=None):
        super().__init__(attrib_name, True)

    def get(self, instance, owner):
        try:
            code = DTSMLPythonSourceClass(python_pre_process(instance.get(self.attrib_name)),
                                          instance.dtsml.filename,
                                          'exec',
                                          instance.sourceline)
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '    File {}, line {}'.format(instance.dtsml.filename,
                                                        instance.sourceline)).with_traceback(sys.exc_info()[2])
        return code


class Eval(AttributeBaseClass):
    """Evaluates the attribute's content as python code and return the result."""
    def __init__(self, attrib_name=None):
        super().__init__(attrib_name, True)

    def get(self, instance, owner):
        try:
            return instance.dtsml.interpreter.eval(python_pre_process(instance.get(self.attrib_name)),
                                                   instance.dtsml.filename,
                                                   instance.sourceline)
        except Exception as e:
            import sys
            raise type(e)(builtins.str(e) +
                          '    File {}, line {}'.format(instance.dtsml.filename,
                                                        instance.sourceline)).with_traceback(sys.exc_info()[2])



