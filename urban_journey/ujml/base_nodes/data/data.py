from urban_journey.ujml.data_base import DataNodeBase
from urban_journey.ujml.exceptions import InvalidInputError


class data(DataNodeBase):
    @property
    def data(self):
        # Check if there are child elements.
        if len(self.children):
            # There are child elements. Check if they have a data attribute.
            for child in self.children:
                # This is a valid data element. So just return the data it contains.
                try:
                    return child.data
                except AttributeError:
                    pass
            # No valid data element was found. raise error.
            self.raise_exception(InvalidInputError, self.tag)
        else:
            # There are no elements in here. So there is probably some text to evaluate as python code.
            source = self.element.text
            if source is not None:
                # There is text in this element, lets evaluate it as python code.
                return self.root.interpreter.eval(source,
                                                  self.file_name,
                                                  self.source_line)
            else:
                # There is neither code nor a data element in this input. Raise an error.
                self.raise_exception(InvalidInputError, self.tag)
