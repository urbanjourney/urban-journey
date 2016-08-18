import unittest
import os
import inspect

from urban_journey import __version__ as uj_version
from urban_journey.ujml.register import node_register, update_node_register, extension_paths
from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.root_ujml_node import UjmlNode
from ..loaders import from_string

from .test_extentions import __path__ as test_ext_path
from .test_extentions import stoffs
from ..base_nodes import path as default_ext_path

test_ext_path = test_ext_path[0]

from urban_journey.ujml.exceptions import IncompatibleUJVersion, RequiredAttributeError, IdMustBeUniqueError, \
    IdNotFoundError


class TestParser(unittest.TestCase):
    def setUp(self):
        self.old_path = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("x_example_2.ujml") as f:
            self.ujml_example_2 = f.read().format(version=uj_version)

        with open("x_example_3.ujml") as f:
            self.ujml_example_3 = f.read().format(version=uj_version)

        with open("x_example_4.ujml") as f:
            self.ujml_example_4 = f.read().format(version=uj_version)

        # Add the test extensions.
        if test_ext_path[0] not in extension_paths:
            extension_paths.append(test_ext_path)
            update_node_register()

    def tearDown(self):
        os.chdir(self.old_path)

    def test_register(self):
        assert test_ext_path in extension_paths
        assert default_ext_path in extension_paths
        for member_name, member in inspect.getmembers(stoffs):
            if isinstance(member, type):
                if issubclass(member, NodeBase):
                    assert member_name in node_register

    def test_root_element(self):
        ujml_element = from_string(self.ujml_example_4)
        assert isinstance(ujml_element, UjmlNode)

    def test_version_checking(self):
        ujml_code = '<?xml version="1.0"?><ujml version="0.0.1234567890"/>'

        try:
            ujml_elem = from_string(ujml_code)
            assert False
        except IncompatibleUJVersion:
            assert True

    def test_attributes(self):
        """Basic test to see if the basic attribute type are running fine."""
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
            <a_stoff a_str="qwerty"
                     a_int="9001"
                     a_bool="True"
                     a_float="1.2"
                     a_list="1,2,3,4"
                     a_eval="2+2"
                     a_exec="global x; x=3+3*b">

            </a_stoff>
        </ujml>
        '''
        a_stoff = from_string(ujml_code)[0]

        self.assertEqual("qwerty", a_stoff.a_str)
        self.assertEqual(9001, a_stoff.a_int)
        self.assertTrue(a_stoff.a_bool)
        self.assertEqual(1.2, a_stoff.a_float)
        self.assertEqual([1, 2, 3, 4], a_stoff.a_list)
        self.assertEqual(4, a_stoff.a_eval)
        a_stoff.a_exec(b=4)
        self.assertEqual(15, a_stoff.root.interpreter['x'])

    def test_attribute_multiple_same_type(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
           <b_stoff a_str1="qwerty"
                    a_str2="azerty"/>
        </ujml>'''
        b_stoff = from_string(ujml_code)[0]
        assert b_stoff.a_str1 == "qwerty"
        assert b_stoff.a_str2 == "azerty"

    def test_attribute_optional_required(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                   <bn_stoff a_optional_1="qwerty"/>
                </ujml>'''
        bn_stoff = from_string(ujml_code)[0]
        assert bn_stoff.a_optional_1 == "qwerty"
        assert bn_stoff.a_optional_2 == "bar"
        try:
            bn_stoff.a_required
            assert False
        except RequiredAttributeError:
            assert True

    def test_find_node_by_id(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                           <br_stoff id="foo"/>
                           <br_stoff id="bar"/>
                        </ujml>'''
        ujml = from_string(ujml_code)

        foo = ujml.find_node_by_id("foo")
        bar = ujml.find_node_by_id("bar")

        assert foo is ujml[0]
        assert bar is ujml[1]

    def test_find_node_by_id_duplicate_id(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                                   <br_stoff id="foo"/>
                                   <br_stoff id="foo"/>
                                </ujml>'''
        try:
            from_string(ujml_code)
            assert False
        except IdMustBeUniqueError:
            assert True

    def test_ref(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                                   <csv id="foo" file="csv_test.csv"/>
                                   <data><ref id="foo"/></data>
                                </ujml>'''
        ujml = from_string(ujml_code)
        # True if the first node in ujml is the same node as the first node in data.
        assert ujml[0] is ujml[1][0]

    def test_ref_id_not_found(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                                           <csv id="foo" file="csv_test.csv"/>
                                           <data><ref id="bar"/></data>
                                        </ujml>'''
        try:
            from_string(ujml_code)[1][0]
            assert False
        except IdNotFoundError:
            assert True
