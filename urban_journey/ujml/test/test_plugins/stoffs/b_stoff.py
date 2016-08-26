"""
Multiple same type attribute test node.
"""

from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import String


class b_stoff(NodeBase):
    # Standard types
    a_str1 = String()
    a_str2 = String()
