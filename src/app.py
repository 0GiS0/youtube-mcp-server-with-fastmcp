import os
from fastmcp import FastMCP
from mcp.types import Icon
from googleapiclient.discovery import build

mcp = FastMCP(
    name="YouTube MCP Server",
    instructions="A FastMCP server that provides YouTube video information.",
    icons=[
        Icon(
            src="https://cdn.jsdelivr.net/gh/0GiS0/youtube-mcp-server-with-fastmcp/assets/icons/youtube-server.svg",
            mimeType="image/svg+xml",
            sizes="48x48"),
    ]
)

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


@mcp.tool
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


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
