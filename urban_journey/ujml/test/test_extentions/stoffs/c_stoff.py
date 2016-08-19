import numpy as np

from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import input


class c_stoff(NodeBase):
    # Module inputs
    eval_input = input()
    csv_input = input()
    ref_input = input()

    optional_input = input(optional_value=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    required_input = input()  # Will fail in unit tests

    type_check_input = input(type=str)  # You can pass either a type or a tuple with types.

    # The type is always checked to be np.ndarray before checking the shape.
    shape_check_1 = input(shape=(3, 3))  # Checking if it's a 3x3 matrix
    shape_check_2 = input(shape=(3, np.nan))  # Only checking the first dimension.
    shape_check_3 = input(shape=(4, 3))  # This one will fail the shape check in the unit tests.
    shape_check_4 = input(shape=(np.nan, 4))  # This one will fail the shape check in the unit tests.
    shape_check_5 = input(shape=(4, 3))  # This one will fail the type check in the unit tests.
