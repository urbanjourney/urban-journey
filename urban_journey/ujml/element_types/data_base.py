"""
This is the base class that represent data in ujml files.
"""

from urban_journey.ujml.element_types.base import BaseUJMLElement


class DataBaseElement(BaseUJMLElement):
    """Base element for elements holding or processing data."""
    def _init(self):
        super()._init()

    @property
    def data(self):
        """This property must return the data. It may optionally set data where applicable."""
        return None

