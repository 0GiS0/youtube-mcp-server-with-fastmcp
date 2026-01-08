# 📦 Importaciones
from pydantic import Field  # Para validación de campos en prompts
from services import YouTubeService  # Nuestro servicio de YouTube
import os  # Para leer variables de entorno
from fastmcp import Context, FastMCP  # Framework MCP
from utils.icons import load_icon  # Utilidad para cargar iconos


# 🔑 Configuración de la API de YouTube
# Leemos la API key desde las variables de entorno
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🚀 Inicializar el servicio de YouTube
# Usamos try/except para manejar el caso de que no esté configurada la API key
try:
    youtube_service = YouTubeService()
except ValueError as e:
    # ⚠️ Si no hay API key, el servicio será None y lo manejaremos en cada tool
    youtube_service = None
    print(f"Advertencia: {e}")

# 🔍 Creamos una instancia de FastMCP para la búsqueda de videos
# Esta herramienta agrupa todo lo relacionado con buscar videos
search_mcp = FastMCP(
    name="YouTube Video Search Tool",
    instructions="Tools and prompts for searching videos on Youtube",
)


# 🎨 Cargamos el icono de la tool
tool_icons = load_icon("youtube-videos.png")


@search_mcp.tool(
    icons=tool_icons,
)
def search_videos(topic: str, max_results: int = 5) -> dict:
    """🔍 Busca videos relacionados con un tema en YouTube.

    Esta es una herramienta simple que encapsula la funcionalidad de búsqueda.
    El decorador @search_mcp.tool hace que esta función esté disponible
    como una "tool" que los clientes MCP pueden invocar.

    Args:
        topic (str): 🎯 El tema o título del video a buscar
                     (ej: "Tutorial de Python", "Recetas veganas")
        max_results (int): 🔢 Número máximo de resultados a retornar (default: 5)
                           Rango válido: 1-50

    Returns:
        dict: 📦 Diccionario con la información de los videos:
        {
            'success': bool,      # ✅ True si la búsqueda fue exitosa
            'videos': [           # 📹 Lista de videos encontrados
                {
                    'video_id': str,        # 🆔 ID del video
                    'title': str,           # 📌 Título
                    'description': str,     # 📄 Descripción
                    'url': str,             # 🔗 URL completa
                    'thumbnail': str,       # 🖼️ URL de la miniatura
                    'channel_title': str,   # 👤 Nombre del canal
                    ...
                }
            ]
        }

    Ejemplo de uso:
        >>> results = search_videos("Python tutorial", max_results=3)
        >>> for video in results['videos']:
        ...     print(f"{video['title']} - {video['url']}")
    """
    # 🔒 Verificamos que el servicio de YouTube esté disponible
    # Si no hay API key configurada, retornamos un error descriptivo
    if not youtube_service:
        return {
            "error": "YOUTUBE_API_KEY not set. Please set the environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/apis/credentials"
        }

    # 🚀 Delegamos la búsqueda al servicio de YouTube
    # Esto mantiene la lógica de negocio separada de la tool
    return youtube_service.search_videos(
        query=topic,
        max_results=max_results,
        order='relevance'  # 📊 Ordenamos por relevancia
    )


@search_mcp.prompt()
def search_prompt(ctx: Context, topic: str, language: str = Field(examples=["English", "Spanish", "French"]), max_results: int = 5) -> str:
    """📝 Genera un prompt para buscar videos de YouTube.

    💡 ¿Qué son los "prompts" en MCP?
    Los prompts son plantillas de texto que los clientes pueden usar.
    Son útiles para:
    - Dar ejemplos de cómo usar tus tools 📚
    - Crear comandos rápidos 🚀
    - Estandarizar consultas comunes ⚡

    Este prompt específicamente crea un texto en español para buscar videos.

    Args:
        ctx: 🔧 Contexto de MCP (usado para debug y logging)
        topic: 🎯 Tema de búsqueda
        language: 🗣️ Idioma de los videos (con ejemplos para el usuario)
        max_results: 🔢 Cantidad de resultados deseados

    Returns:
        str: 📄 Un prompt formateado listo para usar
    """

    # 🐛 Registramos información de debug para troubleshooting
    ctx.debug(
        f"Generating search prompt for topic: {topic}, language: {language}, max_results: {max_results}")

    # ✨ Retornamos el prompt formateado en español
    return f"Busca máximo {max_results} vídeos relacionados con {topic} en {language}"
