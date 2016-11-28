"""
Optional/required attribute test node
"""

from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import String


class bn_stoff(NodeBase):
    # Standard types
    a_optional_1 = String(optional_value="foo")
    a_optional_2 = String(optional_value="bar")
    a_required = String()
