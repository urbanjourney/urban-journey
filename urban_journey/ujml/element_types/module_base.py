from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.element_types.input import InputElement


class ModuleBaseElement(BaseUJMLElement):
    '''Base class for dtst modules. This base class implements the lxml specific API.'''

    def _init(self):
        super()._init()

    def _listener(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def f(self):
        pass

    @staticmethod
    def lookup_child(document, element):
        # All child of module elements are module input elements.
        return InputElement
