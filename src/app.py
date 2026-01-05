from fastmcp import FastMCP

mcp = FastMCP("YouTube MCP Server")


@mcp.tool
def get_video_info(topic: str) -> dict:
    """Fetches video information from YouTube based on the given topic.

    Args:
        topic (str): The topic or title of the video to search for.

    Returns:
        dict: A dictionary containing video information such as title, description, and URL.
    """
    # Simulated video information for demonstration purposes
    video_info = {
        "title": f"Sample Video on {topic}",
        "description": f"This is a sample description for a video about {topic}.",
        "url": f"https://www.youtube.com/watch?v=sample_{topic.replace(' ', '_')}"
    }
    return video_info


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
