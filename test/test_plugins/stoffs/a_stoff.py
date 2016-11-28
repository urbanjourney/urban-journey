"""
Basic Attribute test node.
"""

from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import String, Int, Bool, Float, List, Exec, Eval


class a_stoff(NodeBase):
    # Standard types
    a_str = String('a_str')  # Explicitly giving a name to an attribute is optional.
    a_int = Int()
    a_bool = Bool()
    a_float = Float()
    a_list = List()

    #  Code types
    a_exec = Exec()
    a_eval = Eval()

    a_str2 = String()

    a_optional_1 = String(optional_value="foo")
    a_optional_2 = String(optional_value="bar")
    a_required = String()
