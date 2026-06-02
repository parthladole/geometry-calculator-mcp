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

## Host Configuration

Use Python 3.11+ and install the project into a virtual environment:

```powershell
cd path\to\geometry-calculator-mcp
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

Then configure your MCP host to run the server with:

```powershell
.\.venv\Scripts\python.exe -m geometry_calculator_mcp
```

### Claude Desktop

Add the server to `%APPDATA%\Claude\claude_desktop_config.json`.

Use `examples/claude-desktop-config.example.json` as a template and replace the `command` path with the absolute path to your virtual environment's Python executable.

### Continue

Create a config file such as `%USERPROFILE%\.continue\mcpServers\geometry-calculator.json`.

Use `examples/continue-mcp-server.example.json` as a template and replace the `command` path with the absolute path to your virtual environment's Python executable.

### Notes

- Do not commit personal host config files.
- Do not commit API keys, tokens, or machine-specific secrets.
- Keep absolute local paths in personal config only; examples should use placeholders.

## Test

```powershell
pip install -e ".[test]"
pytest
```
