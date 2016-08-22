import sys
import pickle as pck

from urban_journey.common.cached import cached
from urban_journey.ujml.attributes import String
from urban_journey.ujml.data_node_base import DataNodeBase
from urban_journey.ujml.exceptions import DataLoadError, RequiredAttributeError


class pickle(DataNodeBase):
    file = String()

    @cached
    def data(self):
        try:
            return pck.load(open(self.abs_path(self.file), "rb"))
        except RequiredAttributeError as e:
            raise e
        except Exception as e:
            self.raise_exception(DataLoadError, "pickle", extra_traceback=sys.exc_info()[2])

    def reset(self):
        del self.data
