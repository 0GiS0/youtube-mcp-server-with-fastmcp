# 🎬 YouTube MCP Server con FastMCP

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1)
[![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0)
[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Sígueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/)
[![X Follow](https://img.shields.io/badge/X-Sígueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

¡Hola developer 👋🏻! Este es un servidor MCP (Model Context Protocol) construido con **FastMCP**, un framework que te permite crear servidores MCP de forma increíblemente sencilla. En este proyecto demostramos todas las capacidades de FastMCP: modularización con `mount`, herramientas (tools) y prompts con metadatos, iconos personalizados, y patrones avanzados como **Sampling** y **Elicitation**.

<a href="https://youtu.be/CÓDIGO_DEL_VIDEO">
 <img src="https://img.youtube.com/vi/CÓDIGO_DEL_VIDEO/maxresdefault.jpg" alt="Crea un Servidor MCP con FastMCP" width="100%" />
</a>

---

## 📑 Tabla de Contenidos
- [Características](#características)
- [📺 Contenido del Vídeo](#-contenido-del-vídeo)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Herramientas Disponibles](#herramientas-disponibles)
- [Despliegue en FastMCP Cloud](#despliegue-en-fastmcp-cloud)
- [Aprende MCP desde Cero](#aprende-mcp-desde-cero)
- [Sígueme](#sígueme-en-mis-redes-sociales)

---

## ✨ Características

- **Búsqueda de vídeos** con filtros avanzados en YouTube
- **Información detallada de canales** con estadísticas
- **3 Tools de demostración** con diferentes patrones MCP
- **Modularización con `mount`** para organizar tu servidor
- **Iconos personalizados** tanto para el servidor como para tools
- **Prompts con metadatos** que se reflejan en el cliente
- **Sampling MCP**: Invocar modelos de IA del cliente
- **Elicitation MCP**: Diálogos interactivos con el usuario
- **API Key segura** con gestión de variables de entorno
- **Despliegue gratuito** en FastMCP Cloud

---

## 📺 Contenido del Vídeo

Este vídeo cubre todo lo que necesitas saber para crear servidores MCP profesionales con FastMCP:

### 🎯 Temas Cubiertos:

- ✅ **¿Por qué FastMCP?** Comparación con el SDK de TypeScript
- ✅ **Lo fácil que es crear un servidor** - Setup en minutos
- ✅ **Modularización con `mount`** - Organiza tu código
  - Diferencia entre `mount` e `import server`
  - Ejemplo con modo estático
- ✅ **Anatomía de una Tool** - Parámetros, tipos, metadatos
- ✅ **Iconos profesionales** - Servidor y tools con estilo
- ✅ **Prompts y Metadatos** - Cómo se ven en el cliente
- ✅ **Sampling**: Usa modelos de IA del cliente
- ✅ **Elicitation**: Diálogos interactivos con el usuario
- ✅ **Despliegue gratuito** en FastMCP Cloud

---

## 🛠️ Tecnologías

- **Python 3.10+** - Lenguaje principal
- **FastMCP 2.14.2+** - Framework para MCP servers
- **Google API Python Client** - Integración con YouTube
- **Poetry** - Gestor de dependencias
- **python-dotenv** - Gestión de variables de entorno

---

## 📋 Requisitos Previos

- Python 3.10 o superior
- Poetry (gestor de dependencias)
- API Key de YouTube Data v3 (gratuita)
- Conexión a internet

### Obtener API Key de YouTube

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **YouTube Data API v3**
4. Crea credenciales (API Key)
5. Copia tu API key

---

## 🚀 Instalación

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/0GiS0/youtube-mcp-with-fastmcp.git
cd youtube-mcp-with-fastmcp
```

### Paso 2: Instalar dependencias
```bash
poetry install
```

### Paso 3: Configurar la API Key de YouTube
```bash
cp .env.example .env
# Edita .env y añade tu YOUTUBE_API_KEY
```

### Paso 4: Ejecutar el servidor
```bash
poetry run python src/app.py
```

El servidor se iniciará en `http://localhost:8000`

---

## 💻 Uso

### Ejecución Local

```bash
# Con archivo .env
poetry run python src/app.py

# O con variable de entorno
export YOUTUBE_API_KEY=tu_api_key_aqui
poetry run python src/app.py
```

### Usar con un Cliente MCP

Una vez que el servidor está corriendo, puedes conectarte desde:
- **VS Code con MCP Extension**
- **Cursor**
- **Claude Desktop**
- **Cualquier cliente MCP HTTP**

Apunta el cliente a: `http://localhost:8000`

### Ejemplo de Consumo

```python
# Las tools estarán disponibles en tu cliente MCP
# 1. search_videos - Busca vídeos por tema
# 2. generate_youtube_title - Genera títulos con IA
# 3. search_youtube_channel - Busca canales
```

---

## 📁 Estructura del Proyecto

```
youtube-mcp-with-fastmcp/
├── src/
│   ├── __init__.py
│   ├── app.py                      # 🚀 Servidor FastMCP principal
│   ├── services/
│   │   └── youtube_service.py      # 🎬 Lógica de YouTube API
│   ├── tools/
│   │   ├── search_videos.py        # 🔍 Tool: Buscar vídeos
│   │   ├── generate_title.py       # 🤖 Tool: Generar títulos (Sampling)
│   │   └── search_youtube_channel.py # 👤 Tool: Buscar canales (Elicitation)
│   ├── utils/
│   │   └── icons.py                # 🎨 Carga de iconos
│   └── prompts/
│       └── (prompts del servidor)
├── assets/
│   └── icons/                      # 🖼️ Iconos SVG
├── pyproject.toml                  # 📦 Configuración Poetry
├── .env.example                    # 🔑 Variables de entorno
└── README.md
```

---

## 📚 Herramientas Disponibles (MCP Tools)

### 1. 🔍 `search_videos`

Busca vídeos en YouTube por término de búsqueda.

**Parámetros:**
- `topic` (str): Término de búsqueda (ej: "Python tutorial")
- `max_results` (int): Número máximo de resultados (default: 5, max: 50)

**Descripción en código:**
```python
"""Busca videos relacionados con un tema en YouTube."""
```

**Respuesta:**
```json
{
  "success": true,
  "videos": [
    {
      "video_id": "...",
      "title": "...",
      "url": "https://youtube.com/watch?v=...",
      "description": "...",
      "thumbnail": "...",
      "channel_title": "..."
    }
  ]
}
```

---

### 2. 🤖 `generate_youtube_title` (Sampling)

Genera títulos llamativos para YouTube usando el modelo de IA del cliente.

**Parámetros:**
- `topic` (str): El tema para el título (ej: "Python para principiantes")

**Concepto: Sampling**
Esta tool demuestra el patrón **Sampling** de MCP:
- Tu tool hace una solicitud al cliente
- El cliente usa su modelo de IA
- El cliente devuelve el resultado
- Tu tool lo procesa y lo devuelve

**Descripción en código:**
```python
"""Genera un título llamativo para video de YouTube basado en un tema.

Sampling permite que tu herramienta "pida prestado" un modelo de IA al cliente MCP.
En lugar de tener que integrar tu propia IA, usas la que el cliente ya tiene.
"""
```

---

### 3. 💬 `search_youtube_channel` (Elicitation)

Busca un canal de YouTube e interactivamente pregunta si deseas más detalles.

**Parámetros:**
- `channel_name` (str): Nombre del canal a buscar

**Concepto: Elicitation**
Esta tool demuestra el patrón **Elicitation** de MCP:
- La tool se invoca
- El servidor pregunta información adicional al usuario
- El usuario responde (accept/decline/cancel)
- La tool se adapta según la respuesta

**Flujo:**
1. Búsqueda básica del canal
2. Pregunta: "¿Deseas ver los últimos vídeos?"
3. Según la respuesta, obtiene información completa o básica
4. Devuelve los resultados

---

## 🌐 Despliegue en FastMCP Cloud

FastMCP Cloud permite desplegar tu servidor de forma **gratuita** y **sencilla**.

### Pasos:

1. **Conecta tu repositorio:**
   ```bash
   # Sube este código a GitHub
   git push origin main
   ```

2. **Ve a [FastMCP Cloud](https://fastmcp.com)**

3. **Autoriza con GitHub** y selecciona este repositorio

4. **FastMCP Cloud detectará automáticamente:**
   - El archivo `app.py`
   - Las dependencias de `pyproject.toml`
   - Tu configuración

5. **Tu servidor estará en vivo en: `https://your-server.fastmcp.dev`**

### Variables de Entorno:
FastMCP Cloud permite configurar variables secretas:
- Añade tu `YOUTUBE_API_KEY` en el panel
- Se cargará automáticamente al desplegar

---

## 📖 Aprende MCP desde Cero

¿Nuevo en MCP? Te recomiendo que veas la serie completa de MCP antes de este vídeo:

> **[Serie MCP en mi Canal](https://youtube.com/c/GiselaTorres)** - Aprende qué son los MCP servers y por qué van a revolucionar cómo usamos IA

Algunos vídeos de charlas que podrían interesarte:
- Charla sobre Model Context Protocol
- MCP en la práctica: Casos de uso reales
- Comparación: FastMCP vs SDK TypeScript

---

## 🌐 Sígueme en Mis Redes Sociales

Si te ha gustado este proyecto y quieres ver más contenido sobre FastMCP, MCP servers y desarrollo con IA, no olvides suscribirte a mi canal de YouTube y seguirme en mis redes sociales:

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1)
[![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0)
[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Sígueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/)
[![X Follow](https://img.shields.io/badge/X-Sígueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

### 2. `search_youtube_channel`
Busca y obtiene información detallada de un canal de YouTube.

**Parámetros:**
- `channel_name` (str): Nombre del canal

**Retorna:**
- Información del canal
- Estadísticas (suscriptores, vídeos, vistas)
- Últimos vídeos publicados (opcional)

### 3. `generate_youtube_title`
Genera un título atractivo para un vídeo de YouTube usando IA.

**Parámetros:**
- `topic` (str): Tema del vídeo

## 🔧 Servicio de YouTube API

El proyecto incluye un servicio completo (`youtube_service.py`) que proporciona:

- ✅ Búsqueda de vídeos con filtros avanzados
- ✅ Detalles de vídeos (estadísticas, duración, etc.)
- ✅ Búsqueda y detalles de canales
- ✅ Vídeos de un canal específico
- ✅ Comentarios de vídeos
- ✅ Manejo de errores robusto
- ✅ Configuración centralizada

### Ejemplo de Uso del Servicio

```python
from youtube_service import YouTubeService

# Inicializar servicio
service = YouTubeService()

# Buscar vídeos
videos = service.search_videos(
    query="FastMCP tutorial",
    max_results=5,
    order='viewCount'
)

# Obtener detalles de un vídeo
details = service.get_video_details('video_id_aqui')

# Buscar canales
channels = service.search_channels("GitHub")
```

Ver [documentación completa del servicio](docs/YOUTUBE_SERVICE.md) para más detalles.

## 📖 Documentación Adicional

- [Documentación del Servicio de YouTube](docs/YOUTUBE_SERVICE.md)
- [YouTube Data API v3](https://developers.google.com/youtube/v3/docs)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## ⚙️ Configuración Avanzada

### Variables de Entorno

```bash
# .env
YOUTUBE_API_KEY=tu_api_key_aqui
```

### Límites de la API

La API de YouTube tiene cuotas diarias:
- **Cuota gratuita:** 10,000 unidades/día
- **Búsqueda:** ~100 unidades por solicitud
- **Detalles:** ~1 unidad por solicitud

Monitorea tu uso en [Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas).

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 👥 Autor

Gisela Torres

## 🙏 Agradecimientos

- [FastMCP](https://github.com/jlowin/fastmcp) por el framework MCP
- [Google YouTube API](https://developers.google.com/youtube) por la API
