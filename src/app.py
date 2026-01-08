# 📦 Importaciones principales del proyecto
# FastMCP: Framework para crear servidores MCP (Model Context Protocol)
# Icon: Tipo para manejar iconos en el servidor MCP
from fastmcp import FastMCP
from mcp.types import Icon

# 🔑 Cargar variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# 🔧 Importar las herramientas (tools) que hemos creado
# Cada tool representa una funcionalidad específica del servidor
from tools.search_videos import search_mcp
from tools.generate_title import sampling_mcp_demo
from tools.search_youtube_channel import elicitation_mcp_demo

# 🛠️ Librerías estándar de Python
import base64  # Para codificar el icono en base64
from pathlib import Path  # Para manejar rutas de archivos de forma multiplataforma


# 🎨 Configuración del icono del servidor
# Cargamos el icono de YouTube y lo convertimos a un formato data URI
# que puede ser utilizado directamente en la web sin necesidad de archivos externos
icon_path = Path(__file__).parent.parent / "assets" / "icons" / \
    "youtube.png"  # 📂 Ruta relativa desde este archivo
# 🔐 Codificamos la imagen en base64
icon_data = base64.standard_b64encode(icon_path.read_bytes()).decode()
# �️ Creamos el data URI completo
icon_data_uri = f"data:image/png;base64,{icon_data}"

# ✨ Creamos el objeto Icon que utilizará el servidor
icon_data = Icon(src=icon_data_uri, mimeType="image/png", sizes=["64x64"])

# 🚀 Inicializamos el servidor MCP principal
# Este es el punto de entrada de nuestra aplicación
mcp = FastMCP(name="YouTube MCP Server",
              instructions="A FastMCP server that provides YouTube video information.",
              icons=[icon_data])

# 🔍 Tool #1: Búsqueda de videos
# Ejemplo básico de tool y prompt para buscar videos en YouTube
mcp.mount(search_mcp)

# 🤖 Tool #2: Generación de títulos con IA (Sampling)
# Demuestra cómo con MCP puedes "pedir prestado" un modelo de IA al cliente
# para usarlo en tu herramienta. El cliente provee el modelo, tu tool lo usa.
mcp.mount(sampling_mcp_demo)

# 💬 Tool #3: Búsqueda de canales (Elicitation)
# Ejemplo de cómo solicitar información adicional al usuario de forma interactiva
# Elicitation permite que tu tool "pregunte" datos al usuario cuando los necesite
mcp.mount(elicitation_mcp_demo)

# 🎬 Punto de entrada de la aplicación
# Solo se ejecuta cuando corremos este archivo directamente (no cuando se importa)
if __name__ == "__main__":
    # 🌐 Iniciamos el servidor en modo HTTP en el puerto 8000
    # Puedes acceder al servidor en: http://localhost:8000
    mcp.run(transport="http", port=8000)
