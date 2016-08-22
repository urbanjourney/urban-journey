from lxml import etree


class UjmlElement(etree.ElementBase):
    """Class used to create lxml elements."""
    def _init(self):
        super()._init()
        self.node = None
