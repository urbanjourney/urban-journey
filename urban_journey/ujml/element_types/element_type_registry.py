from urban_journey.ujml.element_types.ujml import UJMLElement
from urban_journey.ujml.element_types.test_element import TestElement
from urban_journey.ujml.element_types.vehicle import VehicleElement
from urban_journey.ujml.element_types.data_elements.csv import CsvLoaderClass
from urban_journey.ujml.element_types.data_elements.pickle import PickleLoaderClass
from urban_journey.ujml.element_types.ref import ReferenceElementClass

element_type_registry = {
    # General UJML elemets
    'test_element': TestElement,
    'ujml': UJMLElement,
    'vehicle': VehicleElement,
    'ref': ReferenceElementClass,

    # Data loading and operator elements
    'csv': CsvLoaderClass,
    'pickle': PickleLoaderClass,
}
