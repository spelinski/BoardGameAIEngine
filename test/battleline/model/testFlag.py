import unittest
from battleline.model.Flag import Flag

class TestFlag(unittest.TestCase):
    def test_flag_is_empty_by_default(self):
        self.assertTrue(Flag().is_empty())
