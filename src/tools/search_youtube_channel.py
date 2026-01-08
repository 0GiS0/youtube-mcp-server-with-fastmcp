import os
from fastmcp import FastMCP, Context
from mcp.types import Icon

from dataclasses import dataclass
from services import YouTubeService

import base64
from pathlib import Path
import sys


@dataclass
class YouTubeChannelInfo:
    include_latest_videos: bool = True


# YouTube API configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# Inicializar el servicio de YouTube
try:
    youtube_service = YouTubeService()
except ValueError as e:
    youtube_service = None
    print(f"Advertencia: {e}")


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
    """Searches for a YouTube channel by name and retrieves its details.

    Args:
        channel_name (str): The name of the YouTube channel to search for.
    Returns:
        dict: A dictionary containing channel information such as title, description, and URL.
    """
    result = await ctx.elicit(
        message="Por favor, proporciona el nombre del canal de YouTube que deseas buscar.",
        response_type=YouTubeChannelInfo
    )

    if result.action == "accept":
        channel = result.data
    elif result.action == "decline":
        return "Information not provided"
    else:  # cancel
        return "Operation cancelled"

    if not youtube_service:
        return {
            "error": "YOUTUBE_API_KEY not set. Please set the environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/apis/credentials"
        }

    # Buscar el canal
    search_result = youtube_service.search_channels(
        query=channel_name, max_results=1)

    if not search_result.get('success') or not search_result.get('channels'):
        return {"error": "Channel not found"}

    channel_data = search_result['channels'][0]
    channel_id = channel_data['channel_id']

    # Obtener detalles completos del canal
    channel_details = youtube_service.get_channel_details(
        channel_id, include_statistics=True)

    if not channel_details.get('success'):
        return channel_details

    channel_info = {
        'title': channel_details['title'],
        'description': channel_details['description'],
        'url': channel_details['url'],
        'thumbnail': channel_details['thumbnail'],
        'subscriber_count': channel_details.get('subscriber_count'),
        'video_count': channel_details.get('video_count'),
        'view_count': channel_details.get('view_count')
    }

    if channel.include_latest_videos:
        # Obtener los últimos vídeos del canal
        videos_result = youtube_service.get_channel_videos(
            channel_id, max_results=5)

        if videos_result.get('success'):
            channel_info['latest_videos'] = videos_result['videos']

    return channel_info
