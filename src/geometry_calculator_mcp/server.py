from __future__ import annotations

from typing import Dict, Literal, Optional

from mcp.server.fastmcp import FastMCP

from geometry_calculator_mcp.expression import calculate_expression as evaluate_expression
from geometry_calculator_mcp.geometry import (
    calculate_angle as geometry_calculate_angle,
    calculate_arc_2d as geometry_calculate_arc_2d,
    calculate_bounding_box as geometry_calculate_bounding_box,
    calculate_circle_points as geometry_calculate_circle_points,
    calculate_distance as geometry_calculate_distance,
    calculate_intersection_2d as geometry_calculate_intersection_2d,
    calculate_midpoint as geometry_calculate_midpoint,
    calculate_next_point as geometry_calculate_next_point,
    calculate_polygon_points as geometry_calculate_polygon_points,
    calculate_star_points as geometry_calculate_star_points,
    calculate_trigonometry as geometry_calculate_trigonometry,
    divide_segment as geometry_divide_segment,
    mirror_point_2d as geometry_mirror_point_2d,
    rotate_point_2d as geometry_rotate_point_2d,
    translate_point as geometry_translate_point,
    validate_geometry as geometry_validate_geometry,
)
from geometry_calculator_mcp.units import convert_units as convert_unit_values

mcp = FastMCP("Geometry Calculator MCP")


@mcp.tool()
def calculate_expression(expression: str, variables: Optional[Dict[str, float]] = None) -> dict:
    """2d: Safely evaluate arithmetic expressions with variables, constants, powers, roots, and trig functions."""
    return evaluate_expression(expression, variables)


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """2d: Convert supported length or angle units without external unit libraries."""
    return convert_unit_values(value, from_unit, to_unit)


@mcp.tool()
def calculate_trigonometry(
    operation: str,
    value: Optional[float] = None,
    angle_unit: Literal["deg", "rad"] = "deg",
    adjacent: Optional[float] = None,
    opposite: Optional[float] = None,
    hypotenuse: Optional[float] = None,
) -> dict:
    """2d: Compute trig, inverse trig, angle conversions, or right-triangle values."""
    return geometry_calculate_trigonometry(operation, value, angle_unit, adjacent, opposite, hypotenuse)


@mcp.tool()
def calculate_distance(point_a: dict, point_b: dict, unit: str = "mm") -> dict:
    """3d-basic: Calculate 2D distance, with optional z support for simple 3D point distance."""
    return geometry_calculate_distance(point_a, point_b, unit)


@mcp.tool()
def calculate_angle(
    vector_a: Optional[dict] = None,
    vector_b: Optional[dict] = None,
    point_a: Optional[dict] = None,
    vertex: Optional[dict] = None,
    point_b: Optional[dict] = None,
    output_unit: Literal["deg", "rad"] = "deg",
) -> dict:
    """3d-basic: Calculate angle between vectors or connected point segments."""
    return geometry_calculate_angle(vector_a, vector_b, point_a, vertex, point_b, output_unit)


@mcp.tool()
def calculate_next_point(
    start: dict,
    distance: float,
    angle: float,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    """2d: Return a point from a start point, distance, and direction angle."""
    return geometry_calculate_next_point(start, distance, angle, angle_unit, unit)


@mcp.tool()
def calculate_midpoint(point_a: dict, point_b: dict, unit: str = "mm") -> dict:
    """3d-basic: Return midpoint between two 2D points, with optional simple z midpoint."""
    return geometry_calculate_midpoint(point_a, point_b, unit)


@mcp.tool()
def divide_segment(point_a: dict, point_b: dict, divisions: int, unit: str = "mm") -> dict:
    """3d-basic: Divide a segment into equal parts and return intermediate points."""
    return geometry_divide_segment(point_a, point_b, divisions, unit)


@mcp.tool()
def translate_point(
    point: dict,
    vector: Optional[dict] = None,
    dx: float = 0,
    dy: float = 0,
    dz: Optional[float] = None,
    unit: str = "mm",
) -> dict:
    """3d-basic: Translate a point by offsets or vector, with optional z support."""
    return geometry_translate_point(point, vector, dx, dy, dz, unit)


@mcp.tool()
def rotate_point_2d(point: dict, center: dict, angle: float, angle_unit: Literal["deg", "rad"] = "deg", unit: str = "mm") -> dict:
    """2d: Rotate a point around a 2D center."""
    return geometry_rotate_point_2d(point, center, angle, angle_unit, unit)


@mcp.tool()
def mirror_point_2d(point: dict, axis: Optional[Literal["x", "y"]] = None, line: Optional[dict] = None, unit: str = "mm") -> dict:
    """2d: Mirror a point across the x/y axis or a 2D line."""
    return geometry_mirror_point_2d(point, axis, line, unit)


@mcp.tool()
def calculate_intersection_2d(entity_a: dict, entity_b: dict, unit: str = "mm") -> dict:
    """2d: Intersect 2D lines, rays, segments, and circles."""
    return geometry_calculate_intersection_2d(entity_a, entity_b, unit)


@mcp.tool()
def calculate_circle_points(
    center: dict,
    radius: float,
    count: int,
    start_angle: float = 0,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    """2d: Return evenly spaced points on a circle."""
    return geometry_calculate_circle_points(center, radius, count, start_angle, angle_unit, unit)


@mcp.tool()
def calculate_polygon_points(
    sides: int,
    center: dict,
    radius: Optional[float] = None,
    side_length: Optional[float] = None,
    start_angle: float = 0,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    """2d: Return regular polygon vertices from side count and radius or side length."""
    return geometry_calculate_polygon_points(sides, center, radius, side_length, start_angle, angle_unit, unit)


@mcp.tool()
def calculate_star_points(
    points: int,
    center: dict,
    outer_radius: float,
    inner_radius: float,
    start_angle: float = 90,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    """2d: Return alternating outer/inner points for a star-like sketch."""
    return geometry_calculate_star_points(points, center, outer_radius, inner_radius, start_angle, angle_unit, unit)


@mcp.tool()
def calculate_arc_2d(start: dict, mid: dict, end: dict, unit: str = "mm", output_angle_unit: Literal["deg", "rad"] = "deg") -> dict:
    """2d: Calculate center, radius, angles, and direction for an arc through three points."""
    return geometry_calculate_arc_2d(start, mid, end, unit, output_angle_unit)


@mcp.tool()
def calculate_bounding_box(points: list[dict], unit: str = "mm") -> dict:
    """3d-basic: Return min and max bounds for 2D points, with optional z bounds."""
    return geometry_calculate_bounding_box(points, unit)


@mcp.tool()
def validate_geometry(operation: str, payload: dict) -> dict:
    """2d: Validate solvability and reject unsupported advanced 3D sketch operations."""
    return geometry_validate_geometry(operation, payload)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
