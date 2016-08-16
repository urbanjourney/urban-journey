from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.required_placeholder import Empty

import urban_journey.ujml.attribute_types as attr


class ChannelElement(BaseUJMLElement):
    """This element is used to create and define a new channel"""
    name_attr = attr.string_t("name", optional_value=None)

    def _init(self):
        super()._init()
        # Channel.__init__(self, self.name, self.schema)
        self.__schema = None

    @property
    def schema(self):
        """A dictionary containing the channel schema used by cerberus to validate the data."""
        if self.__schema is Empty:
            return None

        if self.__schema is None:
            if len(self):
                self.__schema = {}
                for state in self:
                    self.__schema[state.name] = state.schema
            else:
                self.schema = Empty
                return None
        return self.__schema

    @property
    def name(self):
        """The channel name. If it's not defined in the ujml document, then the element id is used."""
        if self.name_attr is None:
            return self.id
        else:
            return self.name_attr

    def __getattr__(self, item):
        if item in self.__data:
            return self.__data[item]

    @staticmethod
    def lookup_child(document, element):
        return ChannelStateElements


class ChannelStateElements(BaseUJMLElement):
    """
        This element is used to define a channel state.

**UJML attributes**

.. attribute:: type

   **type:** string

.. attribute:: required

   **type:** bool

.. attribute:: readonly

   **type:** bool

.. attribute:: nullable

   **type:** bool

.. attribute:: minlength

   **type:** int

.. attribute:: maxlength

   **type:** int

.. attribute:: min

   **type:** float

.. attribute:: max

   **type:** float

.. attribute:: empty

   **type:** bool

.. attribute:: regex

   **type:** string

.. attribute:: shape

   **type:** list

**Members**
    """

    # Standard Cerberus rules
    type = attr.string_t(optional_value=None)
    required = attr.bool_t(optional_value=None)
    readonly = attr.bool_t(optional_value=None)
    nullable = attr.bool_t(optional_value=None)
    minlength = attr.int_t(optional_value=None)
    maxlength = attr.int_t(optional_value=None)
    min = attr.float_t(optional_value=None)
    max = attr.float_t(optional_value=None)
    empty = attr.bool_t(optional_value=None)
    regex = attr.string_t(optional_value=None)
    shape = attr.list_t(optional_value=None)

    def _init(self):
        super()._init()
        self.rules = [
            "type",
            "required",
            "readonly",
            "nullable",
            "minlength",
            "maxlength",
            "min",
            "max",
            "empty",
            "regex",
            "shape"
        ]

    @property
    def name(self):
        """The state name."""
        return self.tag

    @property
    def schema(self):
        """A dictionary with the state schema information."""
        schema = {}
        for rule in self.rules:
            val = getattr(self, rule)
            if val is not None:
                schema[rule] = val
        return schema
