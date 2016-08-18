from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import string_t


class bn_stoff(NodeBase):
    # Standard types
    a_optional_1 = string_t(optional_value="foo")
    a_optional_2 = string_t(optional_value="bar")
    a_required = string_t()
