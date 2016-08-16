# python standard imports

# Third party imports
from lxml import etree


def fromfile(f, filename="<ujml_input>"):
    # TODO: test this function.
    if isinstance(filename, str):
        ujml_elem = etree.parse(f, lxml_parser(filename)).getroot()
        ujml_elem.filename = f
    else:
        ujml_elem = etree.parse(f, lxml_parser(filename)).getroot()
        ujml_elem.filename = filename

    return ujml_elem


def fromstring(ujml_string, filename='<ujml_input>'):
    ujml_elem = etree.fromstring(ujml_string, lxml_parser(filename))
    # ujml_elem.filename = filename
    return ujml_elem


def lxml_parser(filename):
    # Not pep8, but necessary. I can't remember why. Probably because of circular import thingy.
    from urban_journey.ujml.parser_lookup import UJMLLookup

    parser = etree.XMLParser()
    parser.set_element_class_lookup(UJMLLookup(filename))
    return parser
