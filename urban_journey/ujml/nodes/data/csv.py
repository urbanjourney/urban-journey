import sys

import numpy as np

from urban_journey.common.cached import cached
from urban_journey.ujml.attributes import String
from urban_journey.ujml.data_node_base import DataNodeBase
from urban_journey.ujml.exceptions import RequiredAttributeError, DataLoadError


class csv(DataNodeBase):
    """
    Bases: :class:`urban_journey.DataNodeBase`
    """
    file = String()
    delimiter = String(optional_value=",")

    @cached
    def data(self):
        try:
            return np.genfromtxt(self.abs_path(self.file), delimiter=self.delimiter)
        except RequiredAttributeError as e:
            raise e
        except:
            self.raise_exception(DataLoadError, "csv", extra_traceback=sys.exc_info()[2])

    def reset(self):
        del self.data
