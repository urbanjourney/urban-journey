import os
from lxml import etree

from urban_journey.ujml.root_ujml_node import UjmlNode
from ..ujml__lxml_element import UjmlElement


# Public
def from_string(ujml_string, file_name="<ujml_input>", globals=None) -> UjmlNode:
    """
    Used lo load in a ujml code from a string.


    :param string ujml_string: String containing the ujml code.
    :param string file_name: Source code file name.
    :param dict globals: Optional dictionary containing global values available in ujml local python interpreter
    :return: Ujml root node.
    :rtype: urban_journey.UjmlNode
    """

    parser = etree.XMLParser()
    lookup = etree.ElementDefaultClassLookup(element=UjmlElement)
    parser.set_element_class_lookup(lookup)
    root_elem = etree.fromstring(ujml_string, parser)

    ujml_node = UjmlNode(root_elem, file_name, globals or {})
    return ujml_node


def from_file(file_path, globals=None):
    """
    Used lo load in a ujml code from a file.


    :param string file_path: Path to ujml file
    :param dict globals: Optional dictionary containing global values available in ujml local python interpreter
    :return: Ujml root node.
    :rtype: urban_journey.UjmlNode
    """

    file_path = os.path.abspath(file_path)
    with open(file_path) as f:
        source = f.read()
    parser = etree.XMLParser()
    lookup = etree.ElementDefaultClassLookup(element=UjmlElement)
    parser.set_element_class_lookup(lookup)
    root_elem = etree.fromstring(source, parser)
    ujml_node = UjmlNode(root_elem, file_path, globals or {})
    return ujml_node
