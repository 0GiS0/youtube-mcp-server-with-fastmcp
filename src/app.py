import os
from fastmcp import FastMCP, Context
from mcp.types import Icon
from googleapiclient.discovery import build
from pydantic import Field

mcp = FastMCP(
    name="YouTube MCP Server",
    instructions="A FastMCP server that provides YouTube video information.",
    icons=[
        Icon(
            src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQgbWVldCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8IS0tIFNlcnZpZG9yL0Jhc2UgLS0+CiAgPHJlY3QgeD0iOCIgeT0iMTIiIHdpZHRoPSIzMiIgaGVpZ2h0PSI4IiByeD0iMiIgZmlsbD0iI0ZGMDAwMCIgc3Ryb2tlPSIjQjMwMDAwIiBzdHJva2Utd2lkdGg9IjEuNSIvPgogIDxyZWN0IHg9IjgiIHk9IjIyIiB3aWR0aD0iMzIiIGhlaWdodD0iOCIgcng9IjIiIGZpbGw9IiNGRjAwMDAiIHN0cm9rZT0iI0IzMDAwMCIgc3Ryb2tlLXdpZHRoPSIxLjUiLz4KICA8cmVjdCB4PSI4IiB5PSIzMiIgd2lkdGg9IjMyIiBoZWlnaHQ9IjgiIHJ4PSIyIiBmaWxsPSIjRkYwMDAwIiBzdHJva2U9IiNCMzAwMDAiIHN0cm9rZS13aWR0aD0iMS41Ii8+CiAgCiAgPCEtLSBJbmRpY2Fkb3JlcyBkZWwgc2Vydmlkb3IgLS0+CiAgPGNpcmNsZSBjeD0iMTIiIGN5PSIxNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgPGNpcmNsZSBjeD0iMTIiIGN5PSIyNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgPGNpcmNsZSBjeD0iMTYiIGN5PSIyNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgPGNpcmNsZSBjeD0iMTIiIGN5PSIzNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgPGNpcmNsZSBjeD0iMTYiIGN5PSIzNiIgcj0iMS41IiBmaWxsPSIjMDBGRjAwIi8+CiAgCiAgPCEtLSBMb2dvIFlvdVR1YmUgZW4gZWwgc2Vydmlkb3IgLS0+CiAgPHBhdGggZD0iTSAyOCAxNSBMIDI4IDE3IEwgMzQgMTYgWiIgZmlsbD0id2hpdGUiLz4KICA8cGF0aCBkPSJNIDI4IDI1IEwgMjggMjcgTCAzNCAyNiBaIiBmaWxsPSJ3aGl0ZSIvPgogIDxwYXRoIGQ9Ik0gMjggMzUgTCAyOCAzNyBMIDM0IDM2IFoiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo=",
            mimeType="image/svg+xml",
            sizes=["48x48"])

    ]
)

# TODO: Crear modulos para incluir las tools, prompt y demás en otros archivos y que sea más ordenado

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


@mcp.tool(
    icons=[Icon(
        src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQgbWVldCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8IS0tIEx1cGEgLS0+CiAgPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTIiIGZpbGw9IiNGRjAwMDAiIHN0cm9rZT0iI0IzMDAwMCIgc3Ryb2tlLXdpZHRoPSIyIi8+CiAgPGxpbmUgeDE9IjI5IiB5MT0iMjkiIHgyPSI0MCIgeTI9IjQwIiBzdHJva2U9IiNCMzAwMDAiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CiAgCiAgPCEtLSBQbGF5IGJ1dHRvbiBkZW50cm8gZGUgbGEgbHVwYSAtLT4KICA8Y2lyY2xlIGN4PSIyMCIgY3k9IjIwIiByPSI4IiBmaWxsPSJ3aGl0ZSIvPgogIDxwYXRoIGQ9Ik0gMTcgMTYgTCAxNyAyNCBMIDI1IDIwIFoiIGZpbGw9IiNGRjAwMDAiLz4KICAKICA8IS0tIERldGFsbGVzIGRlIGLDunNxdWVkYSAtLT4KICA8Y2lyY2xlIGN4PSI0MCIgY3k9IjQwIiByPSIyIiBmaWxsPSIjQjMwMDAwIi8+Cjwvc3ZnPgo=",
        mimeType="image/svg+xml",
        sizes=["48x48"])],
)
def search_videos(topic: str, max_results: int = 5) -> dict:
    """Fetches videos related to the given topic from YouTube.

    Args:
        topic (str): The topic or title of the video to search for.
        max_results (int): Maximum number of results to return (default: 5).

    Returns:
        dict: A dictionary containing video information such as title, description, and URL.
    """
    if not YOUTUBE_API_KEY:
        return {
            "error": "YOUTUBE_API_KEY not set. Please set the environment variable.",
            "instructions": "Get your API key from https://console.cloud.google.com/apis/credentials"
        }

    try:
        # Build YouTube API client
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Search for videos
        search_response = youtube.search().list(
            q=topic,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            order='relevance'
        ).execute()

        # Parse results
        videos = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'channel': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt']
            }
            videos.append(video)

        return {
            'query': topic,
            'total_results': len(videos),
            'videos': videos
        }

    except Exception as e:
        return {
            'error': str(e),
            'query': topic
        }


# FIXME: No está mostrando diferentes opciones de idioma a la hora de generar el prompt
@mcp.prompt()
def search_prompt(ctx: Context, topic: str, language: str = Field(examples=["English", "Spanish", "French"]), max_results: int = 5) -> str:
    """Generates a prompt for searching YouTube videos based on the topic and language."""

    ctx.debug(
        f"Generating search prompt for topic: {topic}, language: {language}, max_results: {max_results}")

    return f"Busca máximo {max_results} vídeos relacionados con {topic} en {language}"


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)


@mcp.tool(icons=[Icon(
    src="https://cdn.jsdelivr.net/gh/0gis0/my-assets/icons/heart.svg",
    mimeType="image/svg+xml",
    sizes=["48x48"])])
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

# TODO: Ejemplo de elicitation
