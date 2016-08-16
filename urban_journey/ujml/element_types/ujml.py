from lxml import etree

from urban_journey import __version__ as dtst_version
from urban_journey.ujml import attribute_types
from urban_journey.ujml.element_types.base import BaseUJMLElement
from urban_journey.ujml.element_types.case import CaseElement
from urban_journey.ujml.exceptions import MissingRequiredAttributeError, UJMLTagMustBeRootError, IncompatibleDTSTVersion
from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass


class UJMLElement(BaseUJMLElement):
    """The root element for all ujml files.

    **UJML attribute**
    .. attribute:: req_version (version in ujml)

           **type:** string\n
           The name of this attribute in ujml is ``version``

    **Members**
    """
    # Attributes
    req_version = attribute_types.string_t('version', True)

    def _init(self):
        self.filename = "<ujml_input>"
        self.interpreter = UJMLPythonInterpreterClass()

        self.configure_interpreter()
        self.check_dtst_version()

    def get_by_id(self, id):
        """Get an element by id.

           .. warning::

              Deprecated, use the css selector instead.
        """
        return self.xpath("//*[@id='{}']".format(id))

    def check_if_root_element(self):
        """Checks whether it is the root element of the xml file"""
        if not self.getparent() is None:
            raise UJMLTagMustBeRootError(self.filename, self.sourceline)

    def check_dtst_version(self):
        """Check whether the currently installed version of dtst satisfies the requirements set in the ujml file."""
        if self.req_version:
            rv = [int(x) for x in self.req_version.split('.')]
            dv = [int(x) for x in dtst_version.split('.')]
            if not (rv[0] == dv[0] and
                    rv[1] == dv[1] and
                    rv[2] <= dv[2]):
                raise IncompatibleDTSTVersion(self.filename, self.sourceline, self.req_version, dtst_version)
        else:
            raise MissingRequiredAttributeError(self.filename, self.sourceline, 'dtst', 'version')

    def configure_interpreter(self):
        """Configures the interpreter."""
        pass

    @staticmethod
    def lookup_child(document, element):
        if element.tag == "case":
            return CaseElement
