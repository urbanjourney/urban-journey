"""
This is the base class that represent data in dtsml files.
"""

from dtst.dtsml.element_types.base import BaseDTSMLElement


class DataBaseElement(BaseDTSMLElement):
    """Base element for elements holding or processing data."""
    def _init(self):
        super()._init()

    @property
    def data(self):
        """This property must return the data. It may optionally set data where applicable."""
        return None

