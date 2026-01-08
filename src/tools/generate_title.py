# 📦 Importaciones necesarias
from fastmcp import Context, FastMCP  # Framework MCP
from utils.icons import get_icon_or_empty  # Utilidad para cargar iconos

# 🤖 Creamos una instancia de FastMCP para esta herramienta específica
# Esta herramienta demuestra el concepto de "sampling" (usar IA del cliente)
sampling_mcp_demo = FastMCP("Tools and prompt for generating cool titles")


# 🎨 Cargamos el icono de la tool usando la utilidad
tool_icons = get_icon_or_empty("youtube-title.png")


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
