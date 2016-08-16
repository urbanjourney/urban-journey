from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.exceptions import InvalidDataElement, UJMLError
from urban_journey.common.code_formatting import python_pre_process


class InputElement(BaseUJMLElement):
    """This element represent the module inputs. It may either contain python code which is evaluated to get a value or
       a it can contain a data element."""
    @property
    def data(self):
        # Check if there are child elements.
        if len(self):
            # There are child elements. Check if they have a data attribute.
            child = self[0]
            if hasattr(child, "data"):
                # This is a valid data element. So just return the data is contains.
                return child.data
            else:
                # Not a valid data element. raise error.
                raise InvalidDataElement(self.ujml.filename, self.sourceline, child.tag)
        else:
            # There are no elements in here. So there is probably some text to evaluate as python code.
            code = self.text
            if code is not None:
                # There is text in this element, lets evaluate it as python code.
                return self.ujml.interpreter.eval(python_pre_process(code),
                                                   self.ujml.filename,
                                                   self.sourceline)
            else:
                # There is neither code nor a data element in this input. Raise an error.
                raise UJMLError(self.ujml.filename, self.sourceline,
                                 "Input element '{}' is missing data".format(self.tag))
