from pydantic import Field
from services import YouTubeService
import os
from fastmcp import Context, FastMCP
from mcp.types import Icon
import base64
from pathlib import Path


# YouTube API configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# Inicializar el servicio de YouTube
try:
    youtube_service = YouTubeService()
except ValueError as e:
    youtube_service = None
    print(f"Advertencia: {e}")

search_mcp = FastMCP(
    name="YouTube Video Search Tool",
    instructions="Tools and prompts for searching videos on Youtube",
)


# Icon for the tool
icon_path = Path(__file__).parent.parent.parent / "assets" / \
    "icons" / "youtube-videos.png"
icon_data = icon_path.read_bytes()
icon_data_uri = f"data:image/png;base64,{base64.b64encode(icon_data).decode()}"
icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])


@search_mcp.tool(
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


@search_mcp.prompt()
def search_prompt(ctx: Context, topic: str, language: str = Field(examples=["English", "Spanish", "French"]), max_results: int = 5) -> str:
    """Generates a prompt for searching YouTube videos based on the topic and language."""

    ctx.debug(
        f"Generating search prompt for topic: {topic}, language: {language}, max_results: {max_results}")

    return f"Busca máximo {max_results} vídeos relacionados con {topic} en {language}"
