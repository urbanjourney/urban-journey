from lxml import etree

from dtst import __version__ as dtst_version
from dtst.dtsml import attribute_types
from dtst.dtsml.element_types.base import BaseDTSMLElement
from dtst.dtsml.element_types.case import CaseElement
from dtst.dtsml.exceptions import MissingRequiredAttributeError, DTSMLTagMustBeRootError, IncompatibleDTSTVersion
from dtst.dtsml.python_interpreter import DTSMLPythonInterpreterClass


class DTSMLElement(BaseDTSMLElement):
    """The root element for all dtsml files.

    **DTSML attribute**
    .. attribute:: req_version (version in dtsml)

           **type:** string\n
           The name of this attribute in dtsml is ``version``

    **Members**
    """
    # Attributes
    req_version = attribute_types.string_t('version', True)

    def _init(self):
        self.filename = "<dtsml_input>"
        self.interpreter = DTSMLPythonInterpreterClass()

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
            raise DTSMLTagMustBeRootError(self.filename, self.sourceline)

    def check_dtst_version(self):
        """Check whether the currently installed version of dtst satisfies the requirements set in the dtsml file."""
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
