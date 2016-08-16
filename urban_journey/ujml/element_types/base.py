from lxml import etree
from urban_journey.ujml import attribute_types
from urban_journey.ujml.internal_state import InternalState

import inspect


class BaseDTSMLElement(etree.ElementBase):
    """
        This is the base element type for all dtsml element. By default it already defines the following xml attributes.


        **DTSML attributes**

        .. attribute:: id

           **type:** string

        .. attribute:: elem_class (class in dtsml)

           **type:** string\n
           The name of this attribute in dtsml is ``class``

        **Members**

    """

    id = attribute_types.string_t()
    elem_class = attribute_types.string_t('class', optional_value="")

    def _init(self):
        self._dtsml = None
        self._case = None
        self._phase = None
        self.current_states_repo = {}
        self.backup_states_repo = {}
        self.internal_states_repo = []
        for key in self.__dir__():
            value = inspect.getattr_static(self, key)
            if isinstance(value, InternalState):
                self.internal_states_repo.append(value)

    # For some reason I implemented save and restore here instead than at the module base. I will move it over there
    # later as I'm planning to change the way this works anyway.
    def save(self):
        """Saves the internal states."""
        for state in self.internal_states_repo:
            state.save(self)

    def restore(self):
        """Restores the internal states to the last save"""
        for state in self.internal_states_repo:
            state.restore(self)

    @property
    def dtsml(self):
        """The root dtsml element."""
        if self._dtsml is None:
            self._dtsml = self.getroottree().getroot()
        return self._dtsml

    @property
    def case(self):
        """The ancestor ``case`` element of this element."""
        # TODO: Write a test for this function
        if self._case is None:
            res = self.xpath("ancestor-or-self::case")[0]
            if len(res):
                self._case = res[0]
        return self._case

    @property
    def phase(self):
        """The ancestor ``phase`` element of this element.
           """
        # TODO: Write a test for this function
        if self._phase is None:
            res = self.xpath("ancestor-or-self::phase")[0]
            if len(res):
                self._phase = res[0]
        return self._phase

    @staticmethod
    def lookup_child(document, element):
        return None
