from ..floor import Floor
import unittest
from ..floor import Floor
from ..default import Default


class FloorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.floor = Floor()
        self.default = Default()
        self.floor.set_successor(self.default)

    def test_positive_float(self):
        self.assertEqual(self.floor.format('3.7', None, {'floor-precision': 1}), '3.0')

    def test_negative_float(self):
        self.assertEqual(self.floor.format('-3.7', None, {'floor-precision': 5}), '-5.0')

    def test_zero(self):
        self.assertEqual(self.floor.format('0', None, {'floor-precision': 1}), '0.0')

    def test_large_positive_float(self):
        self.assertEqual(self.floor.format('122223321', None, {'floor-precision': 5}), '122223320.0')

    def test_large_negative_float(self):
        self.assertEqual(self.floor.format('-122223320.1', None, {'floor-precision': 1}), '-122223321.0')


if __name__ == '__main__':
    unittest.main()
