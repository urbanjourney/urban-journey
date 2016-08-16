import unittest
import os
import os.path
from dtst import __version__ as dtst_version
from urban_journey.ujml.element_types.datcom.datcom_namelists import Namelist
from urban_journey.ujml.dtsml_loaders import fromstring


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.old_path = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("example_1.dtsml") as f:
            self.dtsml_example_1 = f.read().format(version=dtst_version)
        os.chdir(self.old_path)

    def test_parametric_finset_number(self):
        dtsml_elem = fromstring()

        nm = Namelist()
        nm.set_value("CHORD", [3, 4, 5], "FINSET1")
        self.assertTrue(nm.set_value("SSPAN", [9, 6, 5], "FINSET1"))

    def test_wrong_list_size(self):
        nm = Namelist()
        nm.set_value("PTYPE", ["VCYL", "HCYL", "LUG"], "PROTUB")
        self.assertFalse(nm.set_value("NPROT", 4, "PROTUB"))

    def test_wrong_types(self):
        nm = Namelist()
        self.assertFalse(nm.set_value("NPROT", "sdgmhv", "PROTUB"))
        self.assertFalse(nm.set_value("PTYPE", 234, "PROTUB"))
        self.assertFalse(nm.set_value("CHORD", 2.4356, "FINSET1"))

        self.assertTrue(nm.set_value("NPROT", 2, "PROTUB"))
        self.assertTrue(nm.set_value("PTYPE", ["VCYL", "HCYL"], "PROTUB"))  # Has to be same size as NPROT
        self.assertTrue(nm.set_value("CHORD", [3.1, 2.5, 5.2], "FINSET1"))

    def test_wrong_parents(self):
        nm = Namelist()
        self.assertFalse(nm.set_value("NPROT", 2, "FINSET1"))
        self.assertFalse(nm.set_value("PTYPE", ["VCYL", "HCYL"], "WHATEVER"))  # Has to be same size as NPROT
        self.assertFalse(nm.set_value("CHORD", [3.1, 2.5, 5.2], "PROTUB"))

    def test_get_namesets(self):
        nm = Namelist()
        nm.set_value("NPROT", 2, "PROTUB")
        nm.set_value("PTYPE", ["VCYL", "HCYL"], "PROTUB")  # Has to be same size as NPROT
        nm.set_value("CHORD", [3.1, 2.5, 5.2], "FINSET1")
        nm.set_value("TNOSE", "POWER", "AXIBOD")
        nm.set_value("LREF", 4.5, "REFQ")
        nm.set_value("ALPHA", [-3.0, -1.0, 0, 2.0, 5], "FLTCON")
        nm.set_value("NMACH", 5, "FLTCON")
        self.assertEqual(set(nm.list_of_namesets()), set(['PROTUB', 'AXIBOD', 'REFQ', 'FINSET', 'FLTCON']))

    def test_cases_generation(self):
        nm = Namelist()
        nm.set_value("BETA", [1, 2, 3], "FLTCON")
        nm.set_value("PHI", [1.5, 2.5, 3.5], "FLTCON")
        nm.set_value("ALT", [4, 5, 6, 7, 8, 9, 10], "FLTCON")
        nm.generate_cases()
        self.assertEqual(len(nm.secondaryCases), 9)

if __name__ == '__main__':
    unittest.main()
