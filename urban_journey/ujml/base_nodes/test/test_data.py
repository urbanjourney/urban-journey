import unittest
import pickle
import os

import numpy as np

from urban_journey.ujml.loaders import from_string
from urban_journey import __version__ as uj_version


def abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


class TestData(unittest.TestCase):
    def test_csv(self):
        """Test to see if the csv element can load in the csv data correctly."""
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
            <csv file="csv_test.csv"/>
        </ujml>
        '''
        ujml_elem = from_string(ujml_code, __file__)
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert (correct == ujml_elem[0].data).all()

    def test_pickle(self):
        """Test to see if the pickle element can load in pickle data correctly."""
        correct = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        pickle.dump(correct, open(abs_path("pickle_test_1.i.p"), "wb"))
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
            <pickle file="pickle_test_1.i.p"/>
        </ujml>
        '''
        ujml_elem = from_string(ujml_code, __file__)
        assert (correct == ujml_elem[0].data).all()

    def test_data(self):
        correct1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        correct2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        pickle.dump(correct2, open(abs_path("pickle_test_2.i.p"), "wb"))
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                    <data>import numpy as np
                          np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
                    </data>
                    <data>
                        <pickle file="pickle_test_2.i.p"/>
                    </data>
                </ujml>
                '''
        ujml_elem = from_string(ujml_code, __file__)
        assert (correct1 == ujml_elem[0].data).all()
        assert (correct2 == ujml_elem[1].data).all()
