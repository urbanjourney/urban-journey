from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml import attribute_types


class TestElement(BaseUJMLElement):
    """This is a test element used in unit test and experiments."""
    # Standard types
    a_str = attribute_types.string_t('a_str')  # Explisitly giving a name to an attribute is optional.
    a_int = attribute_types.int_t()
    a_bool = attribute_types.bool_t()
    a_float = attribute_types.float_t()
    a_list = attribute_types.list_t()

    a_exec = attribute_types.Exec()
    a_eval = attribute_types.Eval()

    a_str2 = attribute_types.string_t()

    a_optional_1 = attribute_types.string_t(optional_value="foo")
    a_optional_2 = attribute_types.string_t(optional_value="bar")
    a_required = attribute_types.string_t()

