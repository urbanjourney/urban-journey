from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.element_types.channel import ChannelElement

# import dtst.modules as sim_modules


class PhaseElement(BaseUJMLElement):
    """This element represents a simulation phase."""
    def _init(self):
        '''Initializes the phase element.'''
        super()._init()

    @staticmethod
    def lookup_child(document, element):
        if element.tag == "channel":
            return ChannelElement
        # if hasattr(sim_modules, element.tag):
        #     return getattr(sim_modules, element.tag)
        return None

    @property
    def channels(self):
        """List of channels defined in this phase."""
        raise NotImplemented()

    @property
    def modules(self):
        """List of modules declared in this phase."""
        raise NotImplemented()

    @property
    def unsubscribes(self):
        """List of unsubscribe elemnts."""
        raise NotImplemented()
