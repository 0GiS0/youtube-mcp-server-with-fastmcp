# 📦 Importaciones necesarias
from fastmcp import Context, FastMCP  # Framework MCP
from mcp.types import Icon  # Tipo para iconos
import base64  # Para codificar imágenes
from pathlib import Path  # Manejo de rutas
import sys

# 🤖 Creamos una instancia de FastMCP para esta herramienta específica
# Esta herramienta demuestra el concepto de "sampling" (usar IA del cliente)
sampling_mcp_demo = FastMCP("Tools and prompt for generating cool titles")


# 🎨 Configuración del icono para esta herramienta
try:
    # 📂 Obtener la ruta base del proyecto (workspace root)
    # Desde src/tools/ subimos dos niveles (../../) para llegar a la raíz
    project_root = Path(__file__).parent.parent.parent
    icon_path = project_root / "assets" / "icons" / "youtube-title.png"

    if not icon_path.exists():
        raise FileNotFoundError(f"Icon file not found at: {icon_path}")

    icon_data = icon_path.read_bytes()
    icon_data_uri = f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
    icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])
    tool_icons = [icon_data]
    print(f"✓ Icon loaded successfully from: {icon_path}")
except (FileNotFoundError, OSError) as e:
    print(f"⚠ Warning: Icon not found, using tool without icon: {e}")
    print(
        f"  Searched at: {icon_path if 'icon_path' in locals() else 'unknown'}")
    tool_icons = []


@sampling_mcp_demo.tool(icons=tool_icons)
async def generate_youtube_title(ctx: Context, topic: str) -> str:
    """🎬 Genera un título llamativo para video de YouTube basado en un tema.

    💡 ¿Qué es "sampling"?
    Sampling permite que tu herramienta "pida prestado" un modelo de IA al cliente MCP.
    En lugar de tener que integrar tu propia IA, usas la que el cliente ya tiene.

    🔄 Flujo:
    1. Tu tool recibe un topic del usuario 📥
    2. Creas un prompt pidiendo generar un título 📝
    3. Le pides al cliente que use SU modelo de IA 🤖
    4. El cliente ejecuta el modelo y te devuelve el resultado 📤
    5. Retornas el título generado ✨

    Args:
        topic (str): 📌 El tema sobre el que quieres generar el título
                     (ej: "Cómo aprender Python en 2024")

    Returns:
        str: 🎯 Un título llamativo y optimizado para YouTube

    Ejemplo:
        >>> title = await generate_youtube_title(ctx, "Python para principiantes")
        >>> print(title)
        "🐍 Python para PRINCIPIANTES: ¡Aprende en 30 Minutos! 🚀"
    """
    # 🤖 Aquí es donde ocurre la "magia" del sampling
    # Le pedimos al CLIENTE que use su modelo de IA para generar el título
    result = await ctx.sample(
        # 📝 El prompt que enviamos al modelo
        messages=f"Generate a catchy YouTube video title based on the topic: {topic}. Before generating the title, search for popular titles on YouTube related to the topic.",
        # 🎯 Preferencia de modelos (el cliente elegirá el primero disponible)
        model_preferences=["claude-opus-4-5", "claude-sonnet-4-5"],
        # 🌡️ Temperature: 0.7 = balance entre creatividad y coherencia
        # (0.0 = muy predecible, 1.0 = muy creativo/aleatorio)
        temperature=0.7
    )
    # ✅ Retornamos el texto generado (o string vacío si falla)
    return result.text or ""
