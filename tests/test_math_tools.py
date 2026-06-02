import math
import unittest

from geometry_calculator_mcp.expression import calculate_expression
from geometry_calculator_mcp.geometry import calculate_trigonometry
from geometry_calculator_mcp.units import convert_units


class MathToolTests(unittest.TestCase):
    def test_calculate_expression_with_variables_and_functions(self):
        result = calculate_expression("sqrt(a^2 + b^2) + sin(pi / 2)", {"a": 3, "b": 4})

        self.assertAlmostEqual(result["value"], 6.0)
        self.assertEqual(result["meta"]["dimension"], "2d")

    def test_calculate_expression_rejects_unsafe_calls(self):
        with self.assertRaises(ValueError):
            calculate_expression("__import__('os').system('echo unsafe')")

    def test_calculate_expression_rejects_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_expression("10 / 0")

    def test_convert_units_length_and_angle(self):
        self.assertAlmostEqual(convert_units(1, "in", "mm")["value"], 25.4)
        self.assertAlmostEqual(convert_units(180, "deg", "rad")["value"], math.pi)

    def test_convert_units_rejects_incompatible_units(self):
        with self.assertRaises(ValueError):
            convert_units(10, "mm", "deg")

    def test_calculate_trigonometry_degrees(self):
        result = calculate_trigonometry("sin", value=30, angle_unit="deg")

        self.assertAlmostEqual(result["value"], 0.5)

    def test_calculate_trigonometry_right_triangle(self):
        result = calculate_trigonometry("right_triangle", adjacent=3, opposite=4)

        self.assertAlmostEqual(result["value"]["hypotenuse"], 5.0)


if __name__ == "__main__":
    unittest.main()
