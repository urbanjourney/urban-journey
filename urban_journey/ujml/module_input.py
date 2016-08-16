from urban_journey.ujml.unique import Required
from urban_journey.ujml.exceptions import InvalidTypeError, InvalidShapeError, MissingRequiredInput
from urban_journey.ujml import namespace as ujml_namespace

import numpy as np


class Input(object):
    def __init__(self, type=None, optional_value=Required, shape=None):
        self.__type = type
        self.__optional_value = optional_value
        self.__shape = shape
        self.__name = None

    def __get__(self, instance, owner):
        if self.__name is None:
            self.get_name(owner)
        elems = instance.xpath('//'+self.__name)
        if len(elems):
            return self.validate(elems[0], elems[0].data)
        else:
            if self.__optional_value is Required:
                raise MissingRequiredInput(instance.ujml.filename, instance.sourceline, instance.tag, self.__name)
            else:
                return self.validate(instance, self.__optional_value)

    def get_name(self, owner):
        for key, value in owner.__dict__.items():
            if id(value) == id(self):
                self.__name = key
        assert self.__name

    def validate(self, instance, data):
        if self.__type is not None:
            if not isinstance(data, self.__type):
                raise InvalidTypeError(instance.ujml.filename, instance.sourceline, self.__name)
        if self.__shape is not None:
            # Data type must be numpy array if checking for type.
            if not isinstance(data, np.ndarray):
                raise InvalidTypeError(instance.ujml.filename, instance.sourceline, self.__name)
            shape = data.shape
            if len(shape) != len(self.__shape):
                raise InvalidShapeError(instance.ujml.filename, instance.sourceline, self.__name)
            else:
                for s1, s2 in zip(shape, self.__shape):
                    if not np.isnan(s2):
                        if s1 != s2:
                            raise InvalidShapeError(instance.ujml.filename, instance.sourceline, self.__name)
        return data

