from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.element_types.case import CaseElement
from urban_journey.ujml.exceptions import InvalidChildError
from urban_journey.ujml import attribute_types


class VehicleElement(BaseUJMLElement):
    """This element hold some extra information about the vehicle being simulated."""
    name = attribute_types.string_t('name', True)
    version = attribute_types.string_t('version', True)

    def _init(self):
        '''Checks whether the parent of this element is a case element. If not is raises an InvalidChildError.'''
        if not isinstance(self.getparent(), CaseElement):
            raise InvalidChildError(self.ujml.filename, self.sourceline, self.getparent().tag, self.tag)

    @property
    def description(self):
        return self.text.strip()
