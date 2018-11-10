import sys
import pickle as pck

from sim_common.cached import cached
from urban_journey.ujml.attributes import String
from urban_journey.ujml.data_node_base import DataNodeBase
from urban_journey.ujml.exceptions import DataLoadError, RequiredAttributeError


class pickle(DataNodeBase):
    """
    Load in data from a pickle file.
    """

    file = String()

    @cached
    def data(self):
        try:
            with open(self.abs_path(self.file), "rb") as f:
                return pck.load(f)
        except RequiredAttributeError as e:
            raise e
        except Exception as e:
            self.raise_exception(DataLoadError, "pickle", extra_traceback=sys.exc_info()[2])

    def reset(self):
        del self.data
