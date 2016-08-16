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
    from dtst.dtsml.parser_lookup import DTSMLLookup  # Not pep8, but necessary
    parser = etree.XMLParser()
    parser.set_element_class_lookup(DTSMLLookup(filename))
    return parser