from urban_journey.ujml.unique import Required
from urban_journey.ujml.exceptions import UJMLTypeError, InvalidShapeError, MissingRequiredInput


import numpy as np


class Data(object):
    """Used to declare a data input child nodes. The child nodes will be of type
       :class:`urban_journey.ujml.nodes.data.data.data` and will thus behave the same as a :ref:`data_node_section` node.

       :param type: Required data type.
       :param optional_value: Optional value to return in case the node was not given in the ujml file.
       :param shape: Check the shape of an array. The data must be a numpy.ndarray. Pass 'nan' to skip checking a dimension.
    """

    # TODO: Add name as a parameter.
    def __init__(self, type=None, optional_value=Required, shape=None):
        self.type = type
        self.optional_value = optional_value
        self.shape = shape
        self.name = None
        self.child = None

    def __get__(self, instance, owner):
        if self.name is None:
            self.get_name(owner)

        if self.child is None:
            for child in instance:
                if child.tag == self.name:
                    self.child = child

        if self.child is not None:
            return self.validate(self.child, self.child.data)
        else:
            if self.optional_value is Required:
                instance.raise_exception(MissingRequiredInput, instance.tag, self.name)
            else:
                return self.validate(instance, self.optional_value)

    def get_name(self, owner):
        for key, value in owner.__dict__.items():
            if value is self:
                self.name = key
        assert self.name

    def validate(self, instance, data):
        if self.type is not None:
            if not isinstance(data, self.type):
                instance.raise_exception(UJMLTypeError, self.name)
        if self.shape is not None:
            # Data type must be numpy array if checking for type.
            if not isinstance(data, np.ndarray):
                instance.raise_exception(UJMLTypeError, self.name)
            shape = data.shape
            if len(shape) != len(self.shape):
                instance.raise_exception(InvalidShapeError, self.name)
            else:
                for s1, s2 in zip(shape, self.shape):
                    if not np.isnan(s2):
                        if s1 != s2:
                            instance.raise_exception(InvalidShapeError, self.name)
        return data
