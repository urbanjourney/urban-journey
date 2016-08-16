from urban_journey.ujml.element_types.dtsml import DTSMLElement
from urban_journey.ujml.element_types.test_element import TestElement
from urban_journey.ujml.element_types.vehicle import VehicleElement
from urban_journey.ujml.element_types.data_elements.csv import CsvLoaderClass
from urban_journey.ujml.element_types.data_elements.pickle import PickleLoaderClass
from urban_journey.ujml.element_types.ref import ReferenceElementClass

element_type_registry = {
    # General DTSML elemets
    'test_element': TestElement,
    'dtsml': DTSMLElement,
    'vehicle': VehicleElement,
    'ref': ReferenceElementClass,

    # Data loading and operator elements
    'csv': CsvLoaderClass,
    'pickle': PickleLoaderClass,
}
