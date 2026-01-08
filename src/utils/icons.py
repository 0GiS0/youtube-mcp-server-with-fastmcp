"""
🎨 Utilidades para manejo de iconos en MCP

Este módulo centraliza la lógica de carga y conversión de iconos a base64
para ser utilizados en servidores y tools de FastMCP.

Evita código repetido y proporciona funciones reutilizables con manejo de errores.
"""

import base64
from pathlib import Path
from typing import Optional, List
from mcp.types import Icon


def load_icon(
    icon_filename: str,
    icons_dir: Optional[Path] = None,
    mime_type: str = "image/png",
    sizes: Optional[List[str]] = None
) -> Optional[Icon]:
    """
    🖼️ Carga un icono desde el directorio de assets y lo convierte a base64.

    Esta función:
    1. Localiza el archivo del icono en el directorio especificado
    2. Lee los bytes del archivo
    3. Los codifica en base64
    4. Crea un data URI (data:image/png;base64,...)
    5. Retorna un objeto Icon listo para usar en FastMCP

    Args:
        icon_filename (str): Nombre del archivo del icono (ej: "youtube.png")
        icons_dir (Path, optional): Directorio donde buscar el icono.
                                   Si es None, usa assets/icons/ desde la raíz del proyecto.
        mime_type (str): Tipo MIME del icono (default: "image/png")
        sizes (List[str], optional): Tamaños del icono (default: ["64x64"])

    Returns:
        Icon | None: Objeto Icon si se cargó correctamente, None si hubo error

    Ejemplo:
        >>> from utils.icons import load_icon
        >>> icon = load_icon("youtube.png")
        >>> if icon:
        ...     mcp = FastMCP(name="My Server", icons=[icon])

    Raises:
        No lanza excepciones. Imprime advertencias y retorna None en caso de error.
    """
    try:
        # 📂 Determinar el directorio de iconos
        if icons_dir is None:
            # Por defecto: assets/icons/ desde la raíz del proyecto
            # Asumimos que este archivo está en src/utils/
            project_root = Path(__file__).parent.parent.parent
            icons_dir = project_root / "assets" / "icons"

        # 🔍 Construir la ruta completa al icono
        icon_path = icons_dir / icon_filename

        # ✅ Verificar que el archivo existe
        if not icon_path.exists():
            raise FileNotFoundError(f"Icon file not found at: {icon_path}")

        # 📖 Leer los bytes del archivo
        icon_bytes = icon_path.read_bytes()

        # 🔐 Codificar en base64
        icon_base64 = base64.standard_b64encode(icon_bytes).decode()

        # 🌐 Crear el data URI
        icon_data_uri = f"data:{mime_type};base64,{icon_base64}"

        # 🎨 Crear el objeto Icon
        sizes = sizes or ["64x64"]
        icon = Icon(src=icon_data_uri, mimeType=mime_type, sizes=sizes)

        print(f"✓ Icon loaded successfully from: {icon_path}")
        return icon

    except (FileNotFoundError, OSError) as e:
        print(f"⚠ Warning: Could not load icon '{icon_filename}': {e}")
        print(
            f"  Searched at: {icon_path if 'icon_path' in locals() else 'unknown'}")
        return None


def load_icons(*icon_filenames: str, **kwargs) -> List[Icon]:
    """
    🖼️ Carga múltiples iconos a la vez.

    Función de conveniencia para cargar varios iconos con la misma configuración.
    Solo retorna los iconos que se cargaron exitosamente.

    Args:
        *icon_filenames: Nombres de archivos de iconos a cargar
        **kwargs: Argumentos adicionales para load_icon()
                 (icons_dir, mime_type, sizes)

    Returns:
        List[Icon]: Lista de iconos cargados exitosamente (puede estar vacía)

    Ejemplo:
        >>> icons = load_icons("youtube.png", "github.png", "discord.png")
        >>> print(f"Loaded {len(icons)} icons")
    """
    loaded_icons = []
    for filename in icon_filenames:
        icon = load_icon(filename, **kwargs)
        if icon is not None:
            loaded_icons.append(icon)
    return loaded_icons


def get_icon_or_empty(icon_filename: str, **kwargs) -> List[Icon]:
    """
    🎯 Carga un icono y retorna una lista para usar directamente con @tool(icons=...).

    Esta función es útil para decoradores donde necesitas una lista de iconos.
    Si el icono se carga, retorna [icon], si no, retorna [].

    Args:
        icon_filename (str): Nombre del archivo del icono
        **kwargs: Argumentos adicionales para load_icon()

    Returns:
        List[Icon]: Lista con el icono [icon] o lista vacía []

    Ejemplo:
        >>> from utils.icons import get_icon_or_empty
        >>> 
        >>> @mcp.tool(icons=get_icon_or_empty("youtube-videos.png"))
        >>> def search_videos(topic: str):
        ...     pass
    """
    icon = load_icon(icon_filename, **kwargs)
    return [icon] if icon is not None else []
