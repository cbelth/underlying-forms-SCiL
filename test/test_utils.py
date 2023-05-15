import unittest
import sys
sys.path.append('../src/')
from utils import powerset

class TestUtils(unittest.TestCase):
    def test_powerset_1(self):
        assert(powerset({1, 2, 3}) == {(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)})

    def test_powerset_2(self):
        assert(powerset({1}) == {(), (1,)})

    def test_powerset_3(self):
        assert(powerset({}) == {()})

if __name__ == "__main__":
    unittest.main()