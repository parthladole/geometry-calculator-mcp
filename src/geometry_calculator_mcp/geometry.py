from __future__ import annotations

import math
from typing import Any, Literal, Optional

from geometry_calculator_mcp.types import Point

TOLERANCE = 1e-9


def calculate_trigonometry(
    operation: str,
    value: Optional[float] = None,
    angle_unit: Literal["deg", "rad"] = "deg",
    adjacent: Optional[float] = None,
    opposite: Optional[float] = None,
    hypotenuse: Optional[float] = None,
) -> dict:
    operation = operation.lower()
    if operation in {"sin", "cos", "tan"}:
        if value is None:
            raise ValueError("value is required for trigonometric functions")
        angle = _angle_to_radians(value, angle_unit)
        result = getattr(math, operation)(angle)
    elif operation in {"asin", "acos", "atan"}:
        if value is None:
            raise ValueError("value is required for inverse trigonometric functions")
        result_angle = getattr(math, operation)(value)
        result = _angle_from_radians(result_angle, angle_unit)
    elif operation == "atan2":
        if opposite is None or adjacent is None:
            raise ValueError("opposite and adjacent are required for atan2")
        result = _angle_from_radians(math.atan2(opposite, adjacent), angle_unit)
    elif operation == "degrees":
        if value is None:
            raise ValueError("value is required")
        result = math.degrees(value)
    elif operation == "radians":
        if value is None:
            raise ValueError("value is required")
        result = math.radians(value)
    elif operation == "right_triangle":
        result = _right_triangle(adjacent, opposite, hypotenuse, angle_unit)
    else:
        raise ValueError(f"Unsupported trigonometry operation: {operation}")

    return _result({"value": result, "operation": operation}, "2d", {"angle": angle_unit})


def calculate_distance(point_a: dict, point_b: dict, unit: str = "mm") -> dict:
    a = _point(point_a)
    b = _point(point_b)
    dx = b.x - a.x
    dy = b.y - a.y
    dz = _z(b) - _z(a)
    dimension = "3d-basic" if a.z is not None or b.z is not None else "2d"
    return _result({"distance": math.sqrt(dx * dx + dy * dy + dz * dz)}, dimension, {"length": unit})


def calculate_angle(
    vector_a: Optional[dict] = None,
    vector_b: Optional[dict] = None,
    point_a: Optional[dict] = None,
    vertex: Optional[dict] = None,
    point_b: Optional[dict] = None,
    output_unit: Literal["deg", "rad"] = "deg",
) -> dict:
    if vector_a is not None and vector_b is not None:
        va = _vector(vector_a)
        vb = _vector(vector_b)
    elif point_a is not None and vertex is not None and point_b is not None:
        pa = _point(point_a)
        pv = _point(vertex)
        pb = _point(point_b)
        va = (pa.x - pv.x, pa.y - pv.y, _z(pa) - _z(pv))
        vb = (pb.x - pv.x, pb.y - pv.y, _z(pb) - _z(pv))
    else:
        raise ValueError("Provide either vector_a/vector_b or point_a/vertex/point_b")

    mag_a = _magnitude(va)
    mag_b = _magnitude(vb)
    if mag_a <= TOLERANCE or mag_b <= TOLERANCE:
        raise ValueError("Cannot calculate angle for zero-length vector")
    cosine = max(-1.0, min(1.0, _dot(va, vb) / (mag_a * mag_b)))
    angle = math.acos(cosine)
    dimension = "3d-basic" if abs(va[2]) > TOLERANCE or abs(vb[2]) > TOLERANCE else "2d"
    return _result({"angle": _angle_from_radians(angle, output_unit)}, dimension, {"angle": output_unit})


def calculate_next_point(
    start: dict,
    distance: float,
    angle: float,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    if distance < 0:
        raise ValueError("distance must be non-negative")
    start_point = _point2d(start, "calculate_next_point")
    theta = _angle_to_radians(angle, angle_unit)
    point = Point(x=start_point.x + distance * math.cos(theta), y=start_point.y + distance * math.sin(theta))
    return _result({"point": _dump_point(point)}, "2d", {"length": unit, "angle": angle_unit})


def calculate_midpoint(point_a: dict, point_b: dict, unit: str = "mm") -> dict:
    a = _point(point_a)
    b = _point(point_b)
    z = (a.z + b.z) / 2 if a.z is not None and b.z is not None else None
    dimension = "3d-basic" if z is not None else "2d"
    return _result({"point": _dump_point(Point(x=(a.x + b.x) / 2, y=(a.y + b.y) / 2, z=z))}, dimension, {"length": unit})


def divide_segment(point_a: dict, point_b: dict, divisions: int, unit: str = "mm") -> dict:
    if divisions < 1:
        raise ValueError("divisions must be at least 1")
    a = _point(point_a)
    b = _point(point_b)
    points = []
    for index in range(1, divisions):
        ratio = index / divisions
        z = _interpolated_z(a, b, ratio)
        points.append(_dump_point(Point(x=a.x + (b.x - a.x) * ratio, y=a.y + (b.y - a.y) * ratio, z=z)))
    dimension = "3d-basic" if a.z is not None and b.z is not None else "2d"
    return _result({"points": points, "division_count": divisions}, dimension, {"length": unit})


def translate_point(point: dict, vector: Optional[dict] = None, dx: float = 0, dy: float = 0, dz: Optional[float] = None, unit: str = "mm") -> dict:
    source = _point(point)
    if vector is not None:
        vector_values = _vector(vector)
        dx, dy, vector_z = vector_values
        dz = vector_z if vector.get("z") is not None else dz
    result_z = None
    if source.z is not None or dz is not None:
        result_z = _z(source) + (dz or 0)
    dimension = "3d-basic" if result_z is not None else "2d"
    return _result({"point": _dump_point(Point(x=source.x + dx, y=source.y + dy, z=result_z))}, dimension, {"length": unit})


def rotate_point_2d(point: dict, center: dict, angle: float, angle_unit: Literal["deg", "rad"] = "deg", unit: str = "mm") -> dict:
    source = _point2d(point, "rotate_point_2d")
    origin = _point2d(center, "rotate_point_2d")
    theta = _angle_to_radians(angle, angle_unit)
    dx = source.x - origin.x
    dy = source.y - origin.y
    rotated = Point(
        x=origin.x + dx * math.cos(theta) - dy * math.sin(theta),
        y=origin.y + dx * math.sin(theta) + dy * math.cos(theta),
    )
    return _result({"point": _dump_point(rotated)}, "2d", {"length": unit, "angle": angle_unit})


def mirror_point_2d(point: dict, axis: Optional[Literal["x", "y"]] = None, line: Optional[dict] = None, unit: str = "mm") -> dict:
    source = _point2d(point, "mirror_point_2d")
    if axis == "x":
        mirrored = Point(x=source.x, y=-source.y)
    elif axis == "y":
        mirrored = Point(x=-source.x, y=source.y)
    elif line is not None:
        p1 = _point2d(line["start"], "mirror_point_2d")
        p2 = _point2d(line["end"], "mirror_point_2d")
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        denom = dx * dx + dy * dy
        if denom <= TOLERANCE:
            raise ValueError("Mirror line must have non-zero length")
        t = ((source.x - p1.x) * dx + (source.y - p1.y) * dy) / denom
        projection = Point(x=p1.x + t * dx, y=p1.y + t * dy)
        mirrored = Point(x=2 * projection.x - source.x, y=2 * projection.y - source.y)
    else:
        raise ValueError("Provide axis='x', axis='y', or a line")
    return _result({"point": _dump_point(mirrored)}, "2d", {"length": unit})


def calculate_intersection_2d(entity_a: dict, entity_b: dict, unit: str = "mm") -> dict:
    type_a = entity_a.get("type")
    type_b = entity_b.get("type")
    if type_a in {"line", "ray", "segment"} and type_b in {"line", "ray", "segment"}:
        points = _intersect_lines(entity_a, entity_b)
    elif type_a == "circle" and type_b == "circle":
        points = _intersect_circles(entity_a, entity_b)
    elif type_a in {"line", "ray", "segment"} and type_b == "circle":
        points = _intersect_line_circle(entity_a, entity_b)
    elif type_a == "circle" and type_b in {"line", "ray", "segment"}:
        points = _intersect_line_circle(entity_b, entity_a)
    else:
        raise ValueError("Supported v1 intersections are line/ray/segment with line/ray/segment/circle and circle-circle")
    return _result({"points": [_dump_point(point) for point in points], "count": len(points)}, "2d", {"length": unit})


def calculate_circle_points(center: dict, radius: float, count: int, start_angle: float = 0, angle_unit: Literal["deg", "rad"] = "deg", unit: str = "mm") -> dict:
    if radius < 0:
        raise ValueError("radius must be non-negative")
    if count < 1:
        raise ValueError("count must be at least 1")
    origin = _point2d(center, "calculate_circle_points")
    start = _angle_to_radians(start_angle, angle_unit)
    step = math.tau / count
    points = [
        _dump_point(Point(x=origin.x + radius * math.cos(start + step * index), y=origin.y + radius * math.sin(start + step * index)))
        for index in range(count)
    ]
    return _result({"points": points}, "2d", {"length": unit, "angle": angle_unit})


def calculate_polygon_points(
    sides: int,
    center: dict,
    radius: Optional[float] = None,
    side_length: Optional[float] = None,
    start_angle: float = 0,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    if sides < 3:
        raise ValueError("sides must be at least 3")
    if radius is None and side_length is None:
        raise ValueError("Provide radius or side_length")
    if radius is None:
        if side_length is None or side_length <= 0:
            raise ValueError("side_length must be positive")
        radius = side_length / (2 * math.sin(math.pi / sides))
    return _result(
        {
            "points": calculate_circle_points(center, radius, sides, start_angle, angle_unit, unit)["points"],
            "circumradius": radius,
            "side_length": 2 * radius * math.sin(math.pi / sides),
        },
        "2d",
        {"length": unit, "angle": angle_unit},
    )


def calculate_star_points(
    points: int,
    center: dict,
    outer_radius: float,
    inner_radius: float,
    start_angle: float = 90,
    angle_unit: Literal["deg", "rad"] = "deg",
    unit: str = "mm",
) -> dict:
    if points < 2:
        raise ValueError("points must be at least 2")
    if outer_radius <= 0 or inner_radius <= 0:
        raise ValueError("outer_radius and inner_radius must be positive")
    origin = _point2d(center, "calculate_star_points")
    start = _angle_to_radians(start_angle, angle_unit)
    step = math.pi / points
    vertices = []
    for index in range(points * 2):
        radius = outer_radius if index % 2 == 0 else inner_radius
        theta = start + step * index
        vertices.append(_dump_point(Point(x=origin.x + radius * math.cos(theta), y=origin.y + radius * math.sin(theta))))
    return _result({"points": vertices}, "2d", {"length": unit, "angle": angle_unit})


def calculate_arc_2d(start: dict, mid: dict, end: dict, unit: str = "mm", output_angle_unit: Literal["deg", "rad"] = "deg") -> dict:
    p1 = _point2d(start, "calculate_arc_2d")
    p2 = _point2d(mid, "calculate_arc_2d")
    p3 = _point2d(end, "calculate_arc_2d")
    center = _circumcenter(p1, p2, p3)
    radius = math.dist((center.x, center.y), (p1.x, p1.y))
    start_angle = math.atan2(p1.y - center.y, p1.x - center.x)
    mid_angle = math.atan2(p2.y - center.y, p2.x - center.x)
    end_angle = math.atan2(p3.y - center.y, p3.x - center.x)
    clockwise = not _angle_between_ccw(start_angle, mid_angle, end_angle)
    return _result(
        {
            "center": _dump_point(center),
            "radius": radius,
            "start_angle": _angle_from_radians(start_angle, output_angle_unit),
            "mid_angle": _angle_from_radians(mid_angle, output_angle_unit),
            "end_angle": _angle_from_radians(end_angle, output_angle_unit),
            "clockwise": clockwise,
        },
        "2d",
        {"length": unit, "angle": output_angle_unit},
    )


def calculate_bounding_box(points: list[dict], unit: str = "mm") -> dict:
    if not points:
        raise ValueError("points must not be empty")
    parsed = [_point(point) for point in points]
    zs = [point.z for point in parsed if point.z is not None]
    minimum = Point(x=min(point.x for point in parsed), y=min(point.y for point in parsed), z=min(zs) if zs else None)
    maximum = Point(x=max(point.x for point in parsed), y=max(point.y for point in parsed), z=max(zs) if zs else None)
    dimension = "3d-basic" if zs else "2d"
    return _result({"min": _dump_point(minimum), "max": _dump_point(maximum)}, dimension, {"length": unit})


def validate_geometry(operation: str, payload: dict) -> dict:
    try:
        if operation in {"rotate_point_2d", "mirror_point_2d", "calculate_intersection_2d", "calculate_arc_2d"}:
            _reject_nested_z(payload, operation)
        return _result({"valid": True, "errors": []}, "2d", {})
    except Exception as exc:
        return _result({"valid": False, "errors": [str(exc)]}, "2d", {})


def _result(payload: dict, dimension: str, units: dict[str, str]) -> dict:
    payload["meta"] = {"dimension": dimension, "units": units, "tolerance": TOLERANCE, "deterministic": True}
    return payload


def _point(data: dict) -> Point:
    return Point(**data)


def _point2d(data: dict, operation: str) -> Point:
    point = _point(data)
    if point.z is not None:
        raise ValueError(f"{operation} is a 2D-only tool; z is unsupported in v1")
    return point


def _dump_point(point: Point) -> dict:
    data = {"x": point.x, "y": point.y}
    if point.z is not None:
        data["z"] = point.z
    return data


def _z(point: Point) -> float:
    return point.z if point.z is not None else 0.0


def _vector(data: dict) -> tuple[float, float, float]:
    return (float(data["x"]), float(data["y"]), float(data.get("z", 0.0)))


def _magnitude(vector: tuple[float, float, float]) -> float:
    return math.sqrt(_dot(vector, vector))


def _dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _angle_to_radians(angle: float, angle_unit: str) -> float:
    if angle_unit == "rad":
        return angle
    if angle_unit == "deg":
        return math.radians(angle)
    raise ValueError("angle_unit must be 'deg' or 'rad'")


def _angle_from_radians(angle: float, angle_unit: str) -> float:
    if angle_unit == "rad":
        return angle
    if angle_unit == "deg":
        return math.degrees(angle)
    raise ValueError("angle_unit must be 'deg' or 'rad'")


def _right_triangle(adjacent: Optional[float], opposite: Optional[float], hypotenuse: Optional[float], angle_unit: str) -> dict:
    values = [adjacent is not None, opposite is not None, hypotenuse is not None]
    if sum(values) < 2:
        raise ValueError("Provide at least two triangle sides")
    if hypotenuse is None:
        hypotenuse = math.hypot(adjacent or 0, opposite or 0)
    elif adjacent is None:
        adjacent = math.sqrt(hypotenuse * hypotenuse - (opposite or 0) ** 2)
    elif opposite is None:
        opposite = math.sqrt(hypotenuse * hypotenuse - adjacent * adjacent)
    if hypotenuse <= TOLERANCE:
        raise ValueError("hypotenuse must be positive")
    return {
        "adjacent": adjacent,
        "opposite": opposite,
        "hypotenuse": hypotenuse,
        "angle": _angle_from_radians(math.atan2(opposite or 0, adjacent or 0), angle_unit),
    }


def _interpolated_z(a: Point, b: Point, ratio: float) -> Optional[float]:
    if a.z is None and b.z is None:
        return None
    return _z(a) + (_z(b) - _z(a)) * ratio


def _intersect_lines(entity_a: dict, entity_b: dict) -> list[Point]:
    p = _point2d(entity_a["start"], "calculate_intersection_2d")
    p2 = _point2d(entity_a["end"], "calculate_intersection_2d")
    q = _point2d(entity_b["start"], "calculate_intersection_2d")
    q2 = _point2d(entity_b["end"], "calculate_intersection_2d")
    r = (p2.x - p.x, p2.y - p.y)
    s = (q2.x - q.x, q2.y - q.y)
    denom = _cross2(r, s)
    if abs(denom) <= TOLERANCE:
        return []
    qp = (q.x - p.x, q.y - p.y)
    t = _cross2(qp, s) / denom
    u = _cross2(qp, r) / denom
    point = Point(x=p.x + t * r[0], y=p.y + t * r[1])
    return [point] if _within_entity(entity_a.get("type", "line"), t) and _within_entity(entity_b.get("type", "line"), u) else []


def _intersect_line_circle(line: dict, circle: dict) -> list[Point]:
    p1 = _point2d(line["start"], "calculate_intersection_2d")
    p2 = _point2d(line["end"], "calculate_intersection_2d")
    center = _point2d(circle["center"], "calculate_intersection_2d")
    radius = float(circle["radius"])
    if radius < 0:
        raise ValueError("circle radius must be non-negative")
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    a = dx * dx + dy * dy
    if a <= TOLERANCE:
        raise ValueError("line entity must have non-zero length")
    fx = p1.x - center.x
    fy = p1.y - center.y
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius
    discriminant = b * b - 4 * a * c
    if discriminant < -TOLERANCE:
        return []
    discriminant = max(0.0, discriminant)
    roots = [(-b + math.sqrt(discriminant)) / (2 * a)]
    if discriminant > TOLERANCE:
        roots.append((-b - math.sqrt(discriminant)) / (2 * a))
    return [Point(x=p1.x + root * dx, y=p1.y + root * dy) for root in roots if _within_entity(line.get("type", "line"), root)]


def _intersect_circles(circle_a: dict, circle_b: dict) -> list[Point]:
    c1 = _point2d(circle_a["center"], "calculate_intersection_2d")
    c2 = _point2d(circle_b["center"], "calculate_intersection_2d")
    r1 = float(circle_a["radius"])
    r2 = float(circle_b["radius"])
    if r1 < 0 or r2 < 0:
        raise ValueError("circle radius must be non-negative")
    distance = math.dist((c1.x, c1.y), (c2.x, c2.y))
    if distance <= TOLERANCE or distance > r1 + r2 + TOLERANCE or distance < abs(r1 - r2) - TOLERANCE:
        return []
    a = (r1 * r1 - r2 * r2 + distance * distance) / (2 * distance)
    h_squared = r1 * r1 - a * a
    if h_squared < -TOLERANCE:
        return []
    h = math.sqrt(max(0.0, h_squared))
    x2 = c1.x + a * (c2.x - c1.x) / distance
    y2 = c1.y + a * (c2.y - c1.y) / distance
    rx = -(c2.y - c1.y) * (h / distance)
    ry = (c2.x - c1.x) * (h / distance)
    points = [Point(x=x2 + rx, y=y2 + ry)]
    if h > TOLERANCE:
        points.append(Point(x=x2 - rx, y=y2 - ry))
    return points


def _within_entity(entity_type: str, parameter: float) -> bool:
    if entity_type == "line":
        return True
    if entity_type == "ray":
        return parameter >= -TOLERANCE
    if entity_type == "segment":
        return -TOLERANCE <= parameter <= 1 + TOLERANCE
    return False


def _cross2(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _circumcenter(a: Point, b: Point, c: Point) -> Point:
    d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
    if abs(d) <= TOLERANCE:
        raise ValueError("Arc points must not be collinear")
    ux = (
        (a.x * a.x + a.y * a.y) * (b.y - c.y)
        + (b.x * b.x + b.y * b.y) * (c.y - a.y)
        + (c.x * c.x + c.y * c.y) * (a.y - b.y)
    ) / d
    uy = (
        (a.x * a.x + a.y * a.y) * (c.x - b.x)
        + (b.x * b.x + b.y * b.y) * (a.x - c.x)
        + (c.x * c.x + c.y * c.y) * (b.x - a.x)
    ) / d
    return Point(x=ux, y=uy)


def _angle_between_ccw(start: float, middle: float, end: float) -> bool:
    start %= math.tau
    middle %= math.tau
    end %= math.tau
    if end < start:
        end += math.tau
    if middle < start:
        middle += math.tau
    return start <= middle <= end


def _reject_nested_z(value: Any, operation: str) -> None:
    if isinstance(value, dict):
        if "z" in value and value["z"] is not None:
            raise ValueError(f"{operation} is a 2D-only tool; z is unsupported in v1")
        for child in value.values():
            _reject_nested_z(child, operation)
    elif isinstance(value, list):
        for child in value:
            _reject_nested_z(child, operation)
