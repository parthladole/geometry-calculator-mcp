from __future__ import annotations

LENGTH_TO_MM = {
    "mm": 1.0,
    "cm": 10.0,
    "m": 1000.0,
    "in": 25.4,
    "ft": 304.8,
}

ANGLE_TO_RAD = {
    "rad": 1.0,
    "deg": 0.017453292519943295,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit in LENGTH_TO_MM and to_unit in LENGTH_TO_MM:
        base_value = value * LENGTH_TO_MM[from_unit]
        converted = base_value / LENGTH_TO_MM[to_unit]
        unit_type = "length"
    elif from_unit in ANGLE_TO_RAD and to_unit in ANGLE_TO_RAD:
        base_value = value * ANGLE_TO_RAD[from_unit]
        converted = base_value / ANGLE_TO_RAD[to_unit]
        unit_type = "angle"
    else:
        raise ValueError(f"Unsupported or incompatible units: {from_unit} to {to_unit}")

    return {
        "value": converted,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "unit_type": unit_type,
        "meta": {
            "dimension": "2d",
            "units": {"input": from_unit, "output": to_unit},
            "tolerance": 1e-9,
            "deterministic": True,
        },
    }
