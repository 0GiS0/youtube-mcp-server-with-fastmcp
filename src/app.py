import os
from fastmcp import FastMCP, Context
from mcp.types import Icon
from pydantic import Field
from dataclasses import dataclass
from services import YouTubeService

import base64
from pathlib import Path


# Load the icon file and convert to data URI
icon_path = Path(
    "/workspaces/youtube-mcp-with-fastmcp/assets/icons/youtube.png")
icon_data = base64.standard_b64encode(icon_path.read_bytes()).decode()
icon_data_uri = f"data:image/png;base64,{icon_data}"

icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])

mcp = FastMCP(name="YouTube MCP Server",
              instructions="A FastMCP server that provides YouTube video information.",    icons=[icon_data])

# TODO: Crear modulos para incluir las tools, prompt y demás en otros archivos y que sea más ordenado

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Inicializar el servicio de YouTube
try:
    youtube_service = YouTubeService()
except ValueError as e:
    youtube_service = None
    print(f"Advertencia: {e}")


# Icon for the tool
icon_path = Path(
    "/workspaces/youtube-mcp-with-fastmcp/assets/icons/youtube-videos.png")
icon_data = icon_path.read_bytes()
icon_data_uri = f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])


@mcp.tool(
    icons=[icon_data],
)
def search_videos(topic: str, max_results: int = 5) -> dict:
    """Fetches videos related to the given topic from YouTube.

    Args:
        topic (str): The topic or title of the video to search for.
        max_results (int): Maximum number of results to return (default: 5).

    Returns:
        dict: A dictionary containing video information such as title, description, and URL.
    """
    if not youtube_service:
        return {
            "error": "YOUTUBE_API_KEY not set. Please set the environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/apis/credentials"
        }

    return youtube_service.search_videos(
        query=topic,
        max_results=max_results,
        order='relevance'
    )


# FIXME: No está mostrando diferentes opciones de idioma a la hora de generar el prompt
@mcp.prompt()
def search_prompt(ctx: Context, topic: str, language: str = Field(examples=["English", "Spanish", "French"]), max_results: int = 5) -> str:
    """Generates a prompt for searching YouTube videos based on the topic and language."""

    ctx.debug(
        f"Generating search prompt for topic: {topic}, language: {language}, max_results: {max_results}")

    return f"Busca máximo {max_results} vídeos relacionados con {topic} en {language}"


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)


# Icon for the tool
icon_path = Path(
    "/workspaces/youtube-mcp-with-fastmcp/assets/icons/youtube-title.png")
icon_data = icon_path.read_bytes()
icon_data_uri = f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])


@mcp.tool(icons=[icon_data])
async def generate_youtube_title(ctx: Context, topic: str) -> str:
    """Generates a catchy YouTube video title based on the given topic.

    Args:
        topic (str): The topic for which to generate a video title.

    Returns:
        str: A catchy YouTube video title.
    """
    result = await ctx.sample(messages=f"Generate a catchy YouTube video title based on the topic: {topic}. Before generating the title, search for popular titles on YouTube related to the topic.",
                              model_preferences=[
                                  "claude-opus-4-5", "claude-sonnet-4-5"],
                              temperature=0.7
                              )
    return result.text or ""


@dataclass
class YouTubeChannelInfo:
    include_latest_videos: bool = True


# Icon for the tool
icon_path = Path(
    "/workspaces/youtube-mcp-with-fastmcp/assets/icons/youtube-channel.png")
icon_data = icon_path.read_bytes()
icon_data_uri = f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])


@mcp.tool(icons=[icon_data])
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
