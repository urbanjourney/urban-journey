from urban_journey.ujml.element_types.data_base import DataBaseElement
from urban_journey.ujml.attribute_types import string_t
from urban_journey.ujml.exceptions import DataLoadError, MissingRequiredAttributeError


import numpy as np
import sys


class CsvLoaderClass(DataBaseElement):
    """This element is used to load in csv files.

        **DTSML attributes**

        .. attribute:: file

           **type:** string

        .. attribute:: delimiter

           **type:** string\n

        **Members**

    """
    # Attributes
    file = string_t()
    delimiter = string_t(optional_value=",")

    def _init(self):
        super()._init()
        try:
            self.__data = np.genfromtxt(self.file, delimiter=self.delimiter)
        except MissingRequiredAttributeError as e:
            raise e
        except:
            raise DataLoadError(self.dtsml.filename, self.sourceline, "csv").with_traceback(sys.exc_info()[2])

    @property
    def data(self):
        """Numpy array holding the data loaded in."""
        return self.__data
