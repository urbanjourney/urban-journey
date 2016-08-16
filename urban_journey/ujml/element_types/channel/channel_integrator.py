from urban_journey.ujml.element_types.channel import ChannelStateElements
from urban_journey.ujml.element_types.base import BaseDTSMLElement
from dtst.core.channel import Channel


class IntegratorChannelElement(BaseDTSMLElement, Channel):
    def _init(self):
        super()._init()
        Channel.__init__(self.name, self.schema_x0)

    @property
    def schema_x(self):
        """Dictionary containing the schema for the x states."""
        schema = {}
        for state in self.xpath("child::x/*"):
            schema[state.name] = state.schema
        return schema

    @property
    def schema_x0(self):
        """Dictionary containing the schema for the x0 states."""
        schema = {}
        for state in self.xpath("child::x0/*"):
            schema[state.name] = state.schema
        return schema

    @property
    def name(self):
        """The channel name. If it's not defined in the dtsml document, then the element id is used."""
        if self.name_xml_attr is None:
            return self.id
        else:
            return self.name_xml_attr

    @staticmethod
    def lookup_child(document, element):
        return IntegratorChannelStatesGroupElement


class IntegratorChannelStatesGroupElement(BaseDTSMLElement):
    @staticmethod
    def lookup_child(document, element):
        return ChannelStateElements
