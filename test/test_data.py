import unittest
import pickle
import os
import inspect

import numpy as np

from urban_journey.ujml.loaders import from_string
from urban_journey import __version__ as uj_version


def abs_path(relative_path):
    """Returns an absolute path based on a path relative to this file."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


def file_name():
    """Returns the name of this file + name of the test from which it's being called."""
    return "{}.{}".format(__file__, inspect.stack()[1][3])


class TestData(unittest.TestCase):
    def test_csv(self):
        """Test to see if the csv element can load in the csv data correctly."""
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
            <csv file="csv_test.csv"/>
        </ujml>
        '''
        ujml_elem = from_string(ujml_code, file_name())
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert (correct == ujml_elem[0].data).all()

    def test_pickle(self):
        """Test to see if the pickle element can load in pickle data correctly."""
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with open(abs_path("pickle_test_1.i.p"), "wb") as f:
            pickle.dump(correct, f)
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
            <pickle file="pickle_test_1.i.p"/>
        </ujml>
        '''
        ujml_elem = from_string(ujml_code, file_name())
        assert (correct == ujml_elem[0].data).all()

    def test_data(self):
        correct1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        correct2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        with open(abs_path("pickle_test_2.i.p"), "wb") as f:
            pickle.dump(correct2, f)
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                    <data>
                        np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
                    </data>
                    <data>
                        <pickle file="pickle_test_2.i.p"/>
                    </data>
                </ujml>
                '''
        ujml_elem = from_string(ujml_code, file_name())
        assert (correct1 == ujml_elem[0].data).all()
        assert (correct2 == ujml_elem[1].data).all()

    def test_data_array_preprocessor(self):
        correct1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        correct2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        with open(abs_path("pickle_test_2.i.p"), "wb") as f:
            pickle.dump(correct2, f)
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                            <data>
                                1, 2, 3; 4, 5, 6; 7, 8, 9
                            </data>
                            <data ndarray="false">
                                9, 8, 7; 6, 5, 4; 3, 2, 1
                            </data>
                        </ujml>
                        '''
        ujml_elem = from_string(ujml_code, file_name())
        assert (correct1 == ujml_elem[0].data).all()
        assert (correct2 == ujml_elem[1].data).all()
        assert isinstance(ujml_elem[0].data, np.ndarray)
        assert isinstance(ujml_elem[1].data, list)
