from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.exceptions import IdNotFoundError


class ReferenceElementClass(BaseUJMLElement):
    """Reference element. It can be used to reference to an other element within the dtsml file."""
    # def __init__(self, elm):
    #     self._referenced_element = elm

    def _init(self):
        dtsml = super().__getattribute__("getroottree")().getroot()
        result = dtsml.get_by_id(super().__getattribute__("id"))
        super().__setattr__("_referenced_element", None)
        for elem in result:
            if not isinstance(elem, ReferenceElementClass):
                super().__setattr__("_referenced_element", elem)
                break
        if super().__getattribute__("_referenced_element") is None:
            raise IdNotFoundError(dtsml.filename,
                                  super().__getattribute__("sourceline"),
                                  super().__getattribute__("id"))

    def __getattribute__(self, name):
        try:
            if super().__getattribute__("_referenced_element") is None:
                return super().__getattribute__(name)
            else:
                try:
                    return getattr(object.__getattribute__(self, "_referenced_element"), name)
                except AttributeError as e:
                    raise e
        except AttributeError:
            return super().__getattribute__(name)

    def __setattr__(self, key, value):
        if key == "_referenced_element":
            super().__setattr__(key, value)
        else:
            setattr(object.__getattribute__(self, "_referenced_element"), key, value)

    def __getitem__(self, item):
        return object.__getattribute__(self, "_referenced_element").__getitem__(item)

    def __setitem__(self, key, value):
        object.__getattribute__(self, "_referenced_element").__setitem__(key, value)
