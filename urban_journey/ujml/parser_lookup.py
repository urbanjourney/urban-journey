from lxml import etree
from urban_journey.ujml.element_types.element_type_registry import element_type_registry
from urban_journey.ujml.element_types.dtsml import UJMLElement
from urban_journey.ujml.exceptions import UnknownElementError
from urban_journey.common.xml_tag_proc import is_default_namespace


# Element types
from urban_journey.ujml.element_types.base import BaseUJMLElement


class UJMLLookup(etree.PythonElementClassLookup):
    def __init__(self, filename):
        self.filename = filename
        self.dtsml_read_elements = {}
        self.module_list = {}

    def lookup(self, document, element):
        '''Looks up the type of the element read by calling actual_lookup(...) and mantains a history of all elemnents read.'''
        # Calls the actual_lookup function to lookup the element type
        # Stores that type in a dictionary
        # Return the type.

        a = document

        if is_default_namespace(element.tag):
            element_type = self.dtsml_lookup(document, element)
            self.dtsml_read_elements[get_path(element)] = element_type
            return element_type
        else:
            return None

    def dtsml_lookup(self, document, element):
        '''Looks up the type of the element read.'''
        # print('')s
        # print('tag: ', element.tag)
        # print('type: ', type(element))

        # This is the root element, since it has no parent it has to be dealt with seperately.
        if element.tag == "dtsml":
            return UJMLElement

        # Initialize the elements and paths lists with the current tag and it's parent.
        elements = [element, element.getparent()]
        paths = [get_path(x) for x in elements]

        # Look for a parent
        while not paths[-1] in self.dtsml_read_elements:
            elements.append(elements[-1].getparent())
            paths.append(get_path(elements[-1]))

        for i in reversed(range(len(elements)-1)):
            klass = self.dtsml_read_elements[paths[i+1]].lookup_child(self.filename, elements[i])
            if klass is None:
                if elements[i].tag in element_type_registry:
                    self.dtsml_read_elements[paths[i]] = element_type_registry[elements[i].tag]
                else:
                    self.dtsml_read_elements.pop(paths[i], None)
                    # Raise an error if the element was not found.
                    raise UnknownElementError(self.filename, element.sourceline, elements[i].tag)
            else:
                self.dtsml_read_elements[paths[i]] = klass
        return self.dtsml_read_elements[paths[0]]


def get_path(element):
    path = "/" + element.tag
    parent = element.getparent()
    while parent is not None:
        path = "/" + parent.tag + path
        parent = parent.getparent()
    return path


def get_parent_path(element):
    path = ""
    parent = element.getparent()
    while parent is not None:
        path = "/" + parent.tag + path
        parent = parent.getparent()
    return path
