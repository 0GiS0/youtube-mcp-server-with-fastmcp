"""
🎨 Utilidades para manejo de iconos en MCP

Este módulo centraliza la lógica de carga y conversión de iconos a base64
para ser utilizados en servidores y tools de FastMCP.
"""

import base64
from pathlib import Path
from typing import List
from mcp.types import Icon


def load_icon(icon_filename: str) -> List[Icon]:
    """
    🖼️ Carga un icono y retorna una lista para usar con FastMCP.

    Lee el icono desde assets/icons/, lo convierte a base64 y retorna
    una lista [Icon] lista para usar en servidores o tools.
    Si hay error, retorna lista vacía [].

    Args:
        icon_filename (str): Nombre del archivo (ej: "youtube.png")

    Returns:
        List[Icon]: [icon] si se cargó correctamente, [] si hubo error

    Ejemplo:
        >>> from utils.icons import load_icon
        >>> 
        >>> # Para servidores
        >>> mcp = FastMCP(name="Server", icons=load_icon("youtube.png"))
        >>> 
        >>> # Para tools
        >>> @mcp.tool(icons=load_icon("youtube-videos.png"))
        >>> def search_videos(topic: str):
        ...     pass
    """
    try:
        # 📂 Ruta al directorio de iconos (desde src/utils/ -> raíz/assets/icons/)
        project_root = Path(__file__).parent.parent.parent
        icon_path = project_root / "assets" / "icons" / icon_filename

        # ✅ Verificar que existe
        if not icon_path.exists():
            raise FileNotFoundError(f"Icon not found at: {icon_path}")

        # 🔐 Leer y codificar en base64
        icon_bytes = icon_path.read_bytes()
        icon_base64 = base64.standard_b64encode(icon_bytes).decode()

        # 🌐 Crear data URI y objeto Icon
        icon_data_uri = f"data:image/png;base64,{icon_base64}"
        icon = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])

        print(f"🖼️ Icon loaded: {icon_path}")
        return [icon]

    except (FileNotFoundError, OSError) as e:
        print(f"⚠ Warning: Could not load icon '{icon_filename}': {e}")
        return []
