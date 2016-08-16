from dtst.dtsml.element_types.dtsml import DTSMLElement
from dtst.dtsml.element_types.test_element import TestElement
from dtst.dtsml.element_types.vehicle import VehicleElement
from dtst.dtsml.element_types.data_elements.csv import CsvLoaderClass
from dtst.dtsml.element_types.data_elements.pickle import PickleLoaderClass
from dtst.dtsml.element_types.ref import ReferenceElementClass
from dtst.dtsml.element_types.datcom import DatcomElement

element_type_registry = {
    # General DTSML elemets
    'test_element': TestElement,
    'dtsml': DTSMLElement,
    'vehicle': VehicleElement,
    'ref': ReferenceElementClass,

    # Data loading and operator elements
    'csv': CsvLoaderClass,
    'pickle': PickleLoaderClass,

    'datcom': DatcomElement,
}
