# youtube-mcp-server-with-fastmcp

Proyecto Python con FastMCP para integración con YouTube.

## Instalación

```bash
poetry install
```

## Uso

```bash
poetry run python src/app.py
```

o bien usando el CLI de FastMCP

```bash
source .env
poetry run fastmcp run src/app.py:mcp --transport http --port 8000
