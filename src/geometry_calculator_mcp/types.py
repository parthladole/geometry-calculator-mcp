from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Point:
    x: float
    y: float
    z: Optional[float] = None

    def __init__(self, x: float, y: float, z: Optional[float] = None, **extra: Any) -> None:
        if extra:
            extras = ", ".join(sorted(extra))
            raise ValueError(f"Unsupported point fields: {extras}")
        object.__setattr__(self, "x", float(x))
        object.__setattr__(self, "y", float(y))
        object.__setattr__(self, "z", float(z) if z is not None else None)


@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: Optional[float] = None


@dataclass(frozen=True)
class ResultMeta:
    dimension: str
    units: Dict[str, str]
    tolerance: float = 1e-9
    deterministic: bool = True
