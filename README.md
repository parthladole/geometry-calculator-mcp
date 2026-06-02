# Geometry Calculator MCP

A calculation-only MCP server for deterministic math and geometry helpers used by sketching hosts.

This server does not create CAD entities, sketches, files, or SolidWorks objects. It returns structured numeric results that another MCP/client can use to create geometry.

## Capabilities

- Safe arithmetic expression evaluation
- Unit conversion for common length and angle units
- Trigonometry helpers
- 2D point, polygon, circle, star, arc, transform, mirror, and intersection calculations
- Basic 3D-safe operations for distance, midpoint, translation, and vector angle

## Run

```powershell
pip install -e .
geometry-calculator-mcp
```

The server runs over stdio for local MCP hosts.

## Test

```powershell
pip install -e ".[test]"
pytest
```
