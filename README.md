# youtube-mcp-server-with-fastmcp

Servidor MCP (Model Context Protocol) construido con FastMCP para integración completa con la API de YouTube Data v3.

## 🚀 Características

- 🔍 Búsqueda de vídeos con filtros avanzados
- 📺 Información detallada de vídeos (estadísticas, duración, tags)
- 👤 Búsqueda y detalles de canales
- 📝 Obtención de comentarios de vídeos
- 🎯 Servicio centralizado de API con manejo de errores robusto
- ⚡ FastMCP integration para herramientas y prompts

## 📋 Requisitos Previos

- Python 3.10 o superior
- Poetry (gestor de dependencias)
- API Key de YouTube Data v3

### Obtener API Key de YouTube

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **YouTube Data API v3**
4. Crea credenciales (API Key)
5. Copia tu API key

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd youtube-mcp-with-fastmcp
```

2. Instala las dependencias:
```bash
poetry install
```

3. Configura tu API key:
```bash
cp .env.example .env
# Edita .env y añade tu YOUTUBE_API_KEY
```

## 🎯 Uso

### Opción 1: Ejecutar directamente

```bash
export YOUTUBE_API_KEY=tu_api_key_aqui
poetry run python src/app.py
```

### Opción 2: Usando FastMCP CLI (Recomendado)

```bash
source .env
poetry run fastmcp run src/app.py:mcp --transport http --port 8000
```

### Opción 3: Con archivo .env

```bash
# Asegúrate de tener tu .env configurado
poetry run python src/app.py
```

## 🛠️ Estructura del Proyecto

```
youtube-mcp-with-fastmcp/
├── src/
│   ├── __init__.py
│   ├── app.py              # Aplicación FastMCP principal
│   └── youtube_service.py  # Servicio de API de YouTube
├── docs/
│   └── YOUTUBE_SERVICE.md  # Documentación del servicio
├── assets/
│   └── icons/              # Iconos SVG
├── pyproject.toml          # Configuración de Poetry
├── .env.example            # Ejemplo de configuración
└── README.md
```

## 📚 Herramientas Disponibles (MCP Tools)

### 1. `search_videos`
Busca vídeos en YouTube por término de búsqueda.

**Parámetros:**
- `topic` (str): Término de búsqueda
- `max_results` (int): Número máximo de resultados (default: 5)

**Ejemplo:**
```python
result = search_videos("Python tutorials", max_results=10)
```

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
