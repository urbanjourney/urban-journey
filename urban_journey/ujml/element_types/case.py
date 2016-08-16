from dtst.dtsml.element_types.base import BaseDTSMLElement
from dtst.dtsml import attribute_types

from dtst.dtsml.element_types.phase import PhaseElement
from dtst.dtsml.element_types.channel import ChannelElement


class CaseElement(BaseDTSMLElement):
    """This elements encloses one simulation case. There is not much here yet. But in the end I hope to let this element
       inherit from the core class."""
    # Events
    on_start = attribute_types.Exec('on_start')
    on_step = attribute_types.Exec('on_step')
    on_end = attribute_types.Exec('on_end')

    def _init(self):
        self.channels = []

    def run_step(self):
        raise NotImplemented()

    def rhs_function(self):
        raise NotImplemented()

    def configure_integrator(self):
        raise NotImplemented()

    @staticmethod
    def lookup_child(document, element):
        if element.tag == "phase":
            return PhaseElement
        elif element.tag == "channel":
            return ChannelElement
        else:
            return None


