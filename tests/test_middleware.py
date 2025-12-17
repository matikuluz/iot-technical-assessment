import math
import unittest

from bridge.middleware import try_parse_float

class TestTryParseFloat(unittest.TestCase):
    def test_none_returns_none(self):
        self.assertIsNone(try_parse_float(None))

    def test_int_converts_to_float(self):
        self.assertEqual(try_parse_float(5), 5.0)

    def test_float_passthrough(self):
        self.assertEqual(try_parse_float(2.5), 2.5)

    def test_numeric_string(self):
        self.assertEqual(try_parse_float("3.14"), 3.14)

    def test_numeric_string_with_whitespace(self):
        self.assertEqual(try_parse_float("  3.14  "), 3.14)

    def test_scientific_notation(self):
        self.assertEqual(try_parse_float("1e3"), 1000.0)

    def test_invalid_string_returns_none(self):
        self.assertIsNone(try_parse_float("error"))

    def test_non_numeric_type_returns_none(self):
        self.assertIsNone(try_parse_float({"x": 1}))
        self.assertIsNone(try_parse_float([1, 2, 3]))

    def test_inf_is_rejected(self):
        self.assertIsNone(try_parse_float("inf"))

    def test_nan_is_rejected(self):
        self.assertIsNone(try_parse_float("nan"))



if __name__ == "__main__":
    unittest.main()
