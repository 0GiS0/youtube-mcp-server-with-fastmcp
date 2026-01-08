import os
from fastmcp import FastMCP, Context
from mcp.types import Icon

from dataclasses import dataclass
from services import YouTubeService
from src.tools.search_youtube_channel import search_youtube_channel
from tools.search_videos import search_mcp, youtube_service
from tools.generate_title import sampling_mcp_demo
from tools.search_youtube_channel import elicitation_mcp_demo


import base64
from pathlib import Path


# Load the icon file and convert to data URI
# Ruta relativa desde el archivo app.py
icon_path = Path(__file__).parent.parent / "assets" / "icons" / "youtube.png"
icon_data = base64.standard_b64encode(icon_path.read_bytes()).decode()
icon_data_uri = f"data:image/png;base64,{icon_data}"

icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])

mcp = FastMCP(name="YouTube MCP Server",
              instructions="A FastMCP server that provides YouTube video information.",
              icons=[icon_data])

# Ejemplo básico de tool y prompt
mcp.mount(search_mcp)

# Cómo con MCP puedes pedir prestado un modelo de IA al cliente para usarlo en tu tool
mcp.mount(sampling_mcp_demo)

# Ejemplo con Elicitation
mcp.mount(elicitation_mcp_demo)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
