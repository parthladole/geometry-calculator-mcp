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

The server runs over stdio by default for local MCP hosts.

### Transport Modes

Stdio:

```powershell
geometry-calculator-mcp
```

Streamable HTTP:

```powershell
geometry-calculator-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Use this URL in compatible clients:

```text
http://127.0.0.1:8000/mcp
```

Legacy SSE:

```powershell
geometry-calculator-mcp --transport sse --host 127.0.0.1 --port 8000
```

Use this URL in compatible clients:

```text
http://127.0.0.1:8000/sse
```

You can also set defaults with environment variables:

```powershell
$env:GEOMETRY_MCP_TRANSPORT = "streamable-http"
$env:GEOMETRY_MCP_HOST = "127.0.0.1"
$env:GEOMETRY_MCP_PORT = "8000"
geometry-calculator-mcp
```

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

For HTTP-capable clients, start the server separately and use:

- `examples/http-streamable-client.example.json` for Streamable HTTP
- `examples/http-sse-client.example.json` for legacy SSE

Prefer Streamable HTTP for new clients. Use SSE only when a host still requires the older transport.

### Notes

- Do not commit personal host config files.
- Do not commit API keys, tokens, or machine-specific secrets.
- Keep absolute local paths in personal config only; examples should use placeholders.

## Test

```powershell
pip install -e ".[test]"
pytest
```
