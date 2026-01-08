# 📦 Importaciones principales del proyecto
# FastMCP: Framework para crear servidores MCP (Model Context Protocol)
from utils.icons import load_icon
from tools.search_youtube_channel import elicitation_mcp_demo
from tools.generate_title import sampling_mcp_demo
from tools.search_videos import search_mcp
from fastmcp import FastMCP

# 🔑 Cargar variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

# 🔧 Importar las herramientas (tools) que hemos creado

# 🎨 Importar utilidades para manejo de iconos


# 🎨 Configuración del icono del servidor
server_icons = load_icon("youtube.png")

# 🚀 Inicializamos el servidor MCP principal
# Este es el punto de entrada de nuestra aplicación
mcp = FastMCP(name="YouTube MCP Server",
              instructions="A FastMCP server that provides YouTube video information.",
              icons=server_icons)

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
