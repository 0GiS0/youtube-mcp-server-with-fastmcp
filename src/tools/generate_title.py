from fastmcp import Context, FastMCP
from mcp.types import Icon
import base64
from pathlib import Path
import sys

sampling_mcp_demo = FastMCP("Tools and prompt for generating cool titles")


# Icon for the tool
try:
    # Obtener la ruta base del proyecto (workspace root)
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
