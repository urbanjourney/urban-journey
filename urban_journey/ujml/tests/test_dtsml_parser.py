import unittest
from urban_journey import __version__ as dtst_version
import urban_journey.ujml as dtsml
from urban_journey.ujml import namespace as dtsml_namespace
import numpy as np
import os

from urban_journey.ujml.exceptions import MissingRequiredAttributeError, \
                                  InvalidTypeError, \
                                  InvalidShapeError, \
                                  MissingRequiredInput


class TestUJMLParser(unittest.TestCase):
    def setUp(self):
        self.old_path = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("x_example_2.dtsml") as f:
            self.dtsml_example_2 = f.read().format(version=dtst_version, namespace=dtsml_namespace)

        with open("x_example_3.dtsml") as f:
            self.dtsml_example_3 = f.read().format(version=dtst_version)

    def tearDown(self):
        os.chdir(self.old_path)

    def test_root_element_type(self):
        '''Tests whether the root element is of the correct type. If succesfull this means that the custom parser was used.'''
        import urban_journey.ujml as dtsml
        from urban_journey.ujml.element_types.dtsml import UJMLElement
        elem_dtsml = dtsml.fromstring("<dtsml version='{}'/>".format(dtst_version))
        self.assertTrue(isinstance(elem_dtsml, UJMLElement))

    def test_basic(self):
        '''Tests whether the root element is of the correct type. If succesfull this means that the custom parser was used.'''
        import urban_journey.ujml as dtsml
        dtsml_elem = dtsml.fromstring("<?xml version='1.0'?><dtsml version='{}'></dtsml>"
                                      .format(dtst_version))
        list(dtsml_elem)
        self.assertEqual(dtst_version, dtsml_elem.req_version)

    def test_case_element_type(self):
        '''Test whether the case element is of type CaseElement. This is just a basic test to check whether the custom lxml lookup is working.'''
        import urban_journey.ujml as dtsml
        from urban_journey.ujml.element_types.case import CaseElement
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <case/>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)
        self.assertIsInstance(dtsml_elem[0], CaseElement)

    def test_attribute_types(self):
        """Basic test to see if the basic attribute type are running fine."""
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <test_element a_str="qwerty"
                          a_int="9001"
                          a_bool="True"
                          a_float="1.2"
                          a_list="1,2,3,4"
                          a_eval="2+2"
                          a_exec="x=3+3">

            </test_element>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)

        self.assertEqual("qwerty", dtsml_elem[0].a_str)
        self.assertEqual(9001, dtsml_elem[0].a_int)
        self.assertTrue(dtsml_elem[0].a_bool)
        self.assertEqual(1.2, dtsml_elem[0].a_float)
        self.assertEqual([1, 2, 3, 4], dtsml_elem[0].a_list)

        self.assertEqual(4, dtsml_elem[0].a_eval)
        dtsml_elem.interpreter.run_src_object(dtsml_elem[0].a_exec)
        self.assertEqual(6, dtsml_elem.interpreter['x'])

    def test_two_attributes_same_type(self):
        """Check to see if two attributes of the same type can be defined in the same module."""
        # For some reason I though this could fail. Maybe this test should be removed, it's nonsense.
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <test_element a_str="qwerty" a_str2="azerty">
            </test_element>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)

        self.assertEqual("qwerty", dtsml_elem[0].a_str)
        self.assertEqual("azerty", dtsml_elem[0].a_str2)

    def test_optional_and_required_attributes(self):
        # Test to see if optional and required attributes are handled correctly in case they are missing.
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <test_element a_optional_1="qwerty" />
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)
        self.assertEqual("qwerty", dtsml_elem[0].a_optional_1)
        self.assertEqual("bar", dtsml_elem[0].a_optional_2)
        try:
            dtsml_elem[0].a_required
            self.assertTrue(False)
        except MissingRequiredAttributeError:
            self.assertTrue(True)

    def test_vehicle_element(self):
        """Test to see if the vehicle element is working properly."""
        # I was thing of removing the vehicle element and just define the name by case and add some description element.
        # Maybe I'll do this at some point.
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <case>
                <vehicle name="dummy II++" version="1.2.3">
                    The quick brown fox jumps over the lazy dog.
                </vehicle>
            </case>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)

        self.assertEqual("dummy II++", dtsml_elem[0][0].name)
        self.assertEqual("1.2.3", dtsml_elem[0][0].version)
        self.assertEqual("The quick brown fox jumps over the lazy dog.", dtsml_elem[0][0].description)

    def test_csv_data_loading(self):
        """Test to see if the csv element can load in the csv data correctly."""
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <csv file="csv_test.csv"/>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertTrue((correct == dtsml_elem[0].data).all())

    def test_pickle_data_loading(self):
        """Test to see if the pickle element can load in pickle data correctly."""
        import urban_journey.ujml as dtsml
        import pickle
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        pickle.dump(correct, open("pickle_test.i.p", "wb"))
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <pickle file="pickle_test.i.p"/>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)
        self.assertTrue((correct == dtsml_elem[0].data).all())

    def test_ref_element(self):
        """Check to see if the ref element works correctly."""
        import urban_journey.ujml as dtsml
        dtsml_code = '<?xml version="1.0"?><dtsml version="{}">'.format(dtst_version) + '''
            <csv id="a" file="csv_test.csv" time="new_channel"/>
            <ref id="a"/>
        </dtsml>
        '''
        dtsml_elem = dtsml.fromstring(dtsml_code)
        self.assertTrue((dtsml_elem[0].data == dtsml_elem[1].data).all())

    @unittest.skip
    def test_find_simulations_modules(self):
        """Test to see if the __init__ in the modules package finds and loads in the module classes correctly."""
        import urban_journey.modules as mods
        self.assertTrue(hasattr(mods, "ExampleModule"))
        # Somehow this worked on the first try without having to debug. All hail stackoverflow.

    @unittest.skip
    def test_simple_module_loading(self):
        """Test to see if modules are loaded in correctly in the dtsml document."""
        import urban_journey.ujml as dtsml
        from urban_journey.modules import ExampleModule
        dtsml_elem = dtsml.fromstring(self.dtsml_example_2)
        module_elem = dtsml_elem[0][0][0]
        self.assertTrue(isinstance(module_elem, ExampleModule))

    @unittest.skip
    def test_module_input_loading(self):
        import urban_journey.ujml as dtsml
        from urban_journey.ujml.element_types.input import InputElement
        dtsml_elem = dtsml.fromstring(self.dtsml_example_2)

        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        eval_input = dtsml_elem[0][0][0][0]
        csv_input = dtsml_elem[0][0][0][1]
        ref_input = dtsml_elem[0][0][0][2]

        self.assertTrue(isinstance(eval_input, InputElement))
        self.assertTrue(isinstance(csv_input, InputElement))
        self.assertTrue(isinstance(ref_input, InputElement))

        self.assertEqual(eval_input.data, 42)
        self.assertTrue((correct == csv_input.data).all())
        self.assertTrue((correct == ref_input.data).all())

    @unittest.skip
    def test_module_input_attribute(self):
        import urban_journey.ujml as dtsml
        dtsml_elem = dtsml.fromstring(self.dtsml_example_2)
        example_module = dtsml_elem[0][0][0]

        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(example_module.eval_input, 42)
        self.assertTrue((correct == example_module.csv_input).all())
        self.assertTrue((correct == example_module.ref_input).all())

        self.assertTrue((correct == example_module.optional_input).all())
        try:
            example_module.required_input
            self.assertTrue(False)
        except MissingRequiredInput:
            self.assertTrue(True)

        self.assertEqual(example_module.type_check_input, "This is a string")

        self.assertTrue((correct == example_module.shape_check_1).all())
        self.assertTrue((correct == example_module.shape_check_2).all())

        try:
            example_module.shape_check_3
            self.assertTrue(False)
        except InvalidShapeError:
            self.assertTrue(True)

        try:
            example_module.shape_check_4
            self.assertTrue(False)
        except InvalidShapeError:
            self.assertTrue(True)

        try:
            example_module.shape_check_5
            self.assertTrue(False)
        except InvalidTypeError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    @unittest.skip
    def test_internal_states(self):
        dtsml_elem = dtsml.fromstring(self.dtsml_example_2)
        example_module = dtsml_elem[0][0][0]

        self.assertEqual(example_module.int_state, 123456789)
        self.assertEqual(example_module.not_int_state, 987654321)

        example_module.int_state = 42
        example_module.not_int_state = 24

        self.assertEqual(example_module.int_state, 42)
        self.assertEqual(example_module.not_int_state, 24)

        example_module.restore()

        self.assertEqual(example_module.int_state, 123456789)
        self.assertEqual(example_module.not_int_state, 24)

        example_module.int_state = 91
        example_module.not_int_state = 19

        example_module.save()
        example_module.restore()

        self.assertEqual(example_module.int_state, 91)
        self.assertEqual(example_module.not_int_state, 19)

    @unittest.skip
    def test_channel_in_case(self):
        from urban_journey.ujml.element_types.channel import ChannelElement
        dtsml_elem = dtsml.fromstring(self.dtsml_example_3)
        channel_elem = dtsml_elem.xpath("/dtsml/case/channel")[0]
        self.assertIsInstance(channel_elem, ChannelElement)


if __name__ == '__main__':
    unittest.main()
