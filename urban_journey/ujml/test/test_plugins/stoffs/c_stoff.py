"""
Data input test node.
"""

import numpy as np

from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.attributes import Data


class c_stoff(NodeBase):
    # Module inputs
    eval_input = Data()
    csv_input = Data()
    ref_input = Data()

    optional_input = Data(optional_value=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    required_input = Data()  # Will fail in unit tests

    type_check_input = Data(type=str)  # You can pass either a type or a tuple with types.

    # The type is always checked to be np.ndarray before checking the shape.
    shape_check_1 = Data(shape=(3, 3))  # Checking if it's a 3x3 matrix
    shape_check_2 = Data(shape=(3, np.nan))  # Only checking the first dimension.
    shape_check_3 = Data(shape=(4, 3))  # This one will fail the shape check in the unit tests.
    shape_check_4 = Data(shape=(np.nan, 4))  # This one will fail the shape check in the unit tests.
    shape_check_5 = Data(shape=(4, 3))  # This one will fail the type check in the unit tests.
