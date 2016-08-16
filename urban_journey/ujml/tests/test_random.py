"""Just for some random test that don't belong anywhere else."""
import unittest
from urban_journey import __version__ as dtst_version


class TestRandom(unittest.TestCase):
    def test_text_element(self):
        print("test")

if __name__ == "__main__":
    unittest.main()


