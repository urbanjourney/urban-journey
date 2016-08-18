from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import string_t, int_t, bool_t, float_t, list_t, Exec, Eval


class a_stoff(NodeBase):
    # Standard types
    a_str = string_t('a_str')  # Explicitly giving a name to an attribute is optional.
    a_int = int_t()
    a_bool = bool_t()
    a_float = float_t()
    a_list = list_t()

    #  Code types
    a_exec = Exec()
    a_eval = Eval()

    a_str2 = string_t()

    a_optional_1 = string_t(optional_value="foo")
    a_optional_2 = string_t(optional_value="bar")
    a_required = string_t()
