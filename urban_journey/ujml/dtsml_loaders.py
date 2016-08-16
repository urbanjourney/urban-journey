# python standard imports

# Third party imports
from lxml import etree


def fromfile(f, filename="<dtsml_input>"):
    # TODO: test this function.
    if isinstance(filename, str):
        dtsml_elem = etree.parse(f, lxml_parser(filename)).getroot()
        dtsml_elem.filename = f
    else:
        dtsml_elem = etree.parse(f, lxml_parser(filename)).getroot()
        dtsml_elem.filename = filename

    return dtsml_elem


def fromstring(dtsml_string, filename='<dtsml_input>'):
    dtsml_elem = etree.fromstring(dtsml_string, lxml_parser(filename))
    # dtsml_elem.filename = filename
    return dtsml_elem


def lxml_parser(filename):
    # Not pep8, but necessary. I can't remember why. Probably because of circular import thingy.
    from urban_journey.ujml.parser_lookup import DTSMLLookup

    parser = etree.XMLParser()
    parser.set_element_class_lookup(DTSMLLookup(filename))
    return parser
