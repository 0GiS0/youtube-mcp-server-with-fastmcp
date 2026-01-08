# 📦 Importaciones
import os
from fastmcp import FastMCP, Context  # Framework MCP
from mcp.types import Icon  # Para iconos

from dataclasses import dataclass  # Para crear clases de datos simples
from services import YouTubeService  # Nuestro servicio de YouTube

import base64  # Para codificar imágenes
from pathlib import Path  # Manejo de rutas
import sys


# 📋 Clase de datos para la configuración del canal
# Esta clase se usa en el proceso de "elicitation" (pedir info al usuario)
@dataclass
class YouTubeChannelInfo:
    """🎬 Configuración de qué información del canal queremos.

    💡 Esta clase se usa con elicitation para preguntarle al usuario
    si quiere incluir los últimos videos del canal o solo la info básica.
    """
    include_latest_videos: bool = True  # ¿Incluir los últimos videos? 📹


# 🔑 Configuración de la API de YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🚀 Inicializar el servicio de YouTube
try:
    youtube_service = YouTubeService()
except ValueError as e:
    youtube_service = None
    print(f"Advertencia: {e}")


# 💬 Creamos una instancia de FastMCP para demostrar "elicitation"
# Elicitation = pedir información adicional al usuario de forma interactiva
elicitation_mcp_demo = FastMCP(
    "Tool that allow us to search a youtube channel")


# Icon for the tool
try:
    # Obtener la ruta base del proyecto (workspace root)
    # Subir desde src/tools/ hasta la raíz del proyecto
    project_root = Path(__file__).parent.parent.parent
    icon_path = project_root / "assets" / "icons" / "youtube-channel.png"

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


@elicitation_mcp_demo.tool(icons=tool_icons)
async def search_youtube_channel(ctx: Context, channel_name: str) -> dict:
    """📺 Busca un canal de YouTube por nombre y obtiene sus detalles.

    💡 ¿Qué es "elicitation"?
    Elicitation permite que tu tool PREGUNTE información adicional al usuario
    de forma interactiva, DESPUÉS de ser invocada. Es como un "wizard" o diálogo.

    🔄 Flujo de esta tool:
    1. Usuario invoca la tool con el nombre del canal 📥
    2. La tool usa elicitation para preguntar: "¿Quieres los últimos videos?" 💬
    3. Usuario responde (accept/decline/cancel) 👤
    4. Basándose en la respuesta, obtenemos info básica o completa 📊
    5. Retornamos los resultados 📤

    Esto es útil para:
    - Evitar parámetros complicados en la firma de la función 🎯
    - Permitir flujos dinámicos basados en contexto 🌊
    - Mejorar la experiencia del usuario con diálogos 💬

    Args:
        channel_name (str): 👤 El nombre del canal de YouTube a buscar
                            (ej: "CódigoFacilito", "freeCodeCamp")

    Returns:
        dict: 📦 Diccionario con información del canal:
        {
            'title': str,              # 📌 Nombre del canal
            'description': str,        # 📄 Descripción
            'url': str,                # 🔗 URL del canal
            'subscriber_count': str,   # 👥 Número de suscriptores
            'video_count': str,        # 📹 Cantidad de videos
            'view_count': str,         # 👀 Vistas totales
            'latest_videos': [...]     # 🎬 Últimos videos (si se solicitó)
        }

    Ejemplo:
        >>> canal = await search_youtube_channel(ctx, "Python en español")
        >>> print(f"{canal['title']} tiene {canal['subscriber_count']} subs")
    """
    # 💬 Aquí ocurre la "elicitation" - pedimos info adicional al usuario
    # Le preguntamos si quiere incluir los últimos videos del canal
    result = await ctx.elicit(
        message="Por favor, proporciona el nombre del canal de YouTube que deseas buscar.",
        response_type=YouTubeChannelInfo  # 📋 Tipo de dato que esperamos recibir
    )

    # 🔀 Manejamos las diferentes respuestas del usuario
    if result.action == "accept":
        # ✅ Usuario aceptó y proporcionó la información
        channel = result.data
    elif result.action == "decline":
        # ❌ Usuario rechazó proporcionar la información
        return "Information not provided"
    else:  # cancel
        # 🚫 Usuario canceló la operación
        return "Operation cancelled"

    # 🔒 Verificamos que el servicio de YouTube esté disponible
    if not youtube_service:
        return {
            "error": "YOUTUBE_API_KEY not set. Please set the environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/apis/credentials"
        }

    # 🔍 Buscar canales por nombre
    # Obtenemos hasta 5 resultados para dar más opciones
    search_result = youtube_service.search_channels(
        query=channel_name, max_results=5)

    # ❌ Verificamos que encontramos canales
    if not search_result.get('success'):
        return {"error": f"Search failed: {search_result.get('error')}"}

    if not search_result.get('channels'):
        return {"error": "No channels found matching that name"}

    # 📦 Construimos la respuesta con todos los canales encontrados
    channels_info = {
        'query': channel_name,
        'total_results': search_result['total_results'],
        'channels': []
    }

    # 📋 Agregamos la información de cada canal encontrado
    for channel_data in search_result['channels']:
        channel_info = {
            'channel_id': channel_data['channel_id'],  # 🆔 ID del canal
            'title': channel_data['title'],  # 📌 Nombre del canal
            'description': channel_data['description'],  # 📄 Descripción
            'url': channel_data['url'],  # 🔗 URL del canal
            'thumbnail': channel_data['thumbnail'],  # 🖼️ Imagen del canal
            # 📅 Fecha de creación
            'published_at': channel_data['published_at'],
            # � Estadísticas detalladas
            # � Suscriptores
            'subscriber_count': channel_data.get('subscriber_count', 0),
            # � Total de videos
            'video_count': channel_data.get('video_count', 0),
            # � Vistas totales
            'view_count': channel_data.get('view_count', 0),
            'country': channel_data.get('country', 'N/A')  # 🌍 País del canal
        }
        channels_info['channels'].append(channel_info)

    # 🎉 Retornamos toda la información de los canales encontrados
    return channels_info
