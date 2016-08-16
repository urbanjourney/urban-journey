import unittest
from ..transformations import *

class Transformations(unittest.TestCase):
    def test_TCI(self):
        dcm = TCI(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
    
    def test_TIC(self):
        dcm = TIC(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_Tab(self):
        dcm = Tab(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_Tba(self):
        dcm = Tba(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_TEC(self):
        dcm = TEC(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_TCE(self):
        dcm = TCE(0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
    
    def test_TbE(self):
        dcm = TbE(0, 0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_TEb(self):
        dcm = TEb(0, 0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_TaE(self):
        dcm = TaE(0, 0, 0)
        self.assertEqual(np.linalg.det(dcm),1)
        
    def test_TEa(self):
        dcm = TEa(0, 0, 0)
        self.assertEqual(np.linalg.det(dcm),1)