import unittest

from geometry_calculator_mcp.geometry import (
    calculate_angle,
    calculate_arc_2d,
    calculate_bounding_box,
    calculate_circle_points,
    calculate_distance,
    calculate_intersection_2d,
    calculate_midpoint,
    calculate_next_point,
    calculate_polygon_points,
    calculate_star_points,
    divide_segment,
    mirror_point_2d,
    rotate_point_2d,
    translate_point,
    validate_geometry,
)


class GeometryToolTests(unittest.TestCase):
    def test_calculate_next_point_from_angle_and_distance(self):
        result = calculate_next_point({"x": 0, "y": 0}, distance=10, angle=30)

        self.assertAlmostEqual(result["point"]["x"], 8.6602540378)
        self.assertAlmostEqual(result["point"]["y"], 5.0)
        self.assertEqual(result["meta"]["dimension"], "2d")

    def test_polygon_from_side_length(self):
        result = calculate_polygon_points(sides=6, center={"x": 0, "y": 0}, side_length=10)

        self.assertEqual(len(result["points"]), 6)
        self.assertAlmostEqual(result["circumradius"], 10.0)
        self.assertAlmostEqual(result["side_length"], 10.0)

    def test_circle_and_star_points(self):
        circle = calculate_circle_points(center={"x": 0, "y": 0}, radius=5, count=4)
        star = calculate_star_points(points=5, center={"x": 0, "y": 0}, outer_radius=10, inner_radius=5)

        self.assertEqual(len(circle["points"]), 4)
        self.assertEqual(len(star["points"]), 10)

    def test_rotate_and_mirror_point_2d(self):
        rotated = rotate_point_2d({"x": 1, "y": 0}, {"x": 0, "y": 0}, 90)
        mirrored = mirror_point_2d({"x": 3, "y": 4}, axis="x")

        self.assertAlmostEqual(rotated["point"]["x"], 0.0)
        self.assertAlmostEqual(rotated["point"]["y"], 1.0)
        self.assertEqual(mirrored["point"], {"x": 3.0, "y": -4.0})

    def test_intersections_for_segments_and_circles(self):
        line_result = calculate_intersection_2d(
            {"type": "segment", "start": {"x": 0, "y": 0}, "end": {"x": 10, "y": 10}},
            {"type": "segment", "start": {"x": 0, "y": 10}, "end": {"x": 10, "y": 0}},
        )
        circle_result = calculate_intersection_2d(
            {"type": "circle", "center": {"x": 0, "y": 0}, "radius": 5},
            {"type": "circle", "center": {"x": 8, "y": 0}, "radius": 5},
        )

        self.assertEqual(line_result["count"], 1)
        self.assertAlmostEqual(line_result["points"][0]["x"], 5.0)
        self.assertEqual(circle_result["count"], 2)

    def test_arc_from_three_points(self):
        result = calculate_arc_2d({"x": 1, "y": 0}, {"x": 0, "y": 1}, {"x": -1, "y": 0})

        self.assertAlmostEqual(result["center"]["x"], 0.0)
        self.assertAlmostEqual(result["center"]["y"], 0.0)
        self.assertAlmostEqual(result["radius"], 1.0)

    def test_3d_basic_operations(self):
        distance = calculate_distance({"x": 0, "y": 0, "z": 0}, {"x": 0, "y": 0, "z": 5})
        midpoint = calculate_midpoint({"x": 0, "y": 0, "z": 0}, {"x": 2, "y": 2, "z": 2})
        translated = translate_point({"x": 1, "y": 1, "z": 1}, dz=4)
        angle = calculate_angle(vector_a={"x": 1, "y": 0, "z": 0}, vector_b={"x": 0, "y": 1, "z": 0})

        self.assertEqual(distance["meta"]["dimension"], "3d-basic")
        self.assertAlmostEqual(distance["distance"], 5.0)
        self.assertEqual(midpoint["point"], {"x": 1.0, "y": 1.0, "z": 1.0})
        self.assertEqual(translated["point"], {"x": 1.0, "y": 1.0, "z": 5.0})
        self.assertAlmostEqual(angle["angle"], 90.0)

    def test_segment_division_and_bounding_box(self):
        divided = divide_segment({"x": 0, "y": 0}, {"x": 9, "y": 0}, 3)
        bounds = calculate_bounding_box([{"x": -1, "y": 2}, {"x": 5, "y": -3}])

        self.assertEqual(divided["points"], [{"x": 3.0, "y": 0.0}, {"x": 6.0, "y": 0.0}])
        self.assertEqual(bounds["min"], {"x": -1.0, "y": -3.0})
        self.assertEqual(bounds["max"], {"x": 5.0, "y": 2.0})

    def test_2d_tools_reject_z(self):
        with self.assertRaises(ValueError):
            rotate_point_2d({"x": 1, "y": 0, "z": 0}, {"x": 0, "y": 0}, 90)

        validation = validate_geometry("rotate_point_2d", {"point": {"x": 1, "y": 0, "z": 0}})
        self.assertFalse(validation["valid"])

    def test_deterministic_output(self):
        first = calculate_next_point({"x": 2, "y": 3}, distance=7, angle=45)
        second = calculate_next_point({"x": 2, "y": 3}, distance=7, angle=45)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
