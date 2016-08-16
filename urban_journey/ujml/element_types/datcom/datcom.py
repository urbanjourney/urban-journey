from dtst.dtsml.element_types.datcom.datcom_namelists import Namelist
from dtst.dtsml.element_types.base import BaseDTSMLElement

from dtst.dtsml.element_types.input import InputElement
from dtst.dtsml.exceptions import InvalidChildError, InvalidElementInputError


class DatcomElement(BaseDTSMLElement):
    def _init(self):
        pass

    def generate_tables(self):
        namelists = Namelist()

        # loop through childs
        for elem in self:
            if isinstance(elem, InputElement):
                pass
            elif isinstance(elem, NamelistElement):
                for child in elem:
                    if not namelists.set_value(child.tag.upper(), child.data, elem.tag):
                        raise InvalidElementInputError(self.dtsml.filename, self.sourceline, child.tag)
            else:
                pass

    def write_datcom_file(self, namelist):
        namelist.generate_cases()
        lines = namelist.generate_datcom_file()
        filename = "for005.dat"
        with open(filename, 'w') as f:
            f.write(lines)

    @staticmethod
    def lookup_child(document, element):
        element.tag = element.tag.upper()
        if element.tag in ["REFQ", "FLTCON", "AXIBOD"] or "FINSET" in element.tag:
            return NamelistElement
        elif element.tag in ["CASEID", "DIM", "DERIV"]:
            return InputElement


class NamelistElement(BaseDTSMLElement):
    @staticmethod
    def lookup_child(document, element):
        element.tag = element.tag.upper()
        if element.tag in Namelist.namelist:
            # TODO: check if parent is correct.
            if element.get_parent().tag == Namelist.namelist[element.tag]['parent']:
                return InputElement
            else:
                raise InvalidChildError(document, element.sourceline, element.get_parent().tag, element.tag)
        else:
            raise InvalidChildError(document, element.sourceline, element.get_parent().tag, element.tag)


