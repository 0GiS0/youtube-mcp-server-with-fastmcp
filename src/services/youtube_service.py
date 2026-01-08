"""
🎥 YouTube API Service

Este módulo centraliza toda la configuración y las llamadas a la API de Google YouTube.
Proporciona una capa de abstracción para interactuar con la API de YouTube de manera
consistente y manejando errores apropiadamente.

📚 Conceptos clave:
- Configuración centralizada de la API key
- Manejo de errores robusto con try/except
- Métodos reutilizables para diferentes operaciones de YouTube
- Uso de dataclasses para configuración tipada
"""

import os
from typing import Optional, Dict, List, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass


@dataclass
class YouTubeConfig:
    """🔧 Configuración para el servicio de YouTube API.

    Usa dataclass para crear una clase simple que almacena la configuración.
    Es como un "contenedor" de datos con valores por defecto.
    """
    api_key: str  # 🔑 La clave API obtenida de Google Cloud Console
    # 📺 Nombre del servicio (siempre 'youtube')
    api_service_name: str = "youtube"
    api_version: str = "v3"  # 📌 Versión de la API (v3 es la actual)

    @classmethod
    def from_env(cls) -> 'YouTubeConfig':
        """🌍 Crea una configuración desde variables de entorno.

        Esto es útil para no hardcodear la API key en el código.
        La API key se lee de la variable de entorno YOUTUBE_API_KEY.
        """
        api_key = os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            raise ValueError(
                "YOUTUBE_API_KEY no está configurada. "
                "Por favor, configura la variable de entorno. "
                "Obtén tu API key desde: https://console.cloud.google.com/apis/credentials"
            )
        return cls(api_key=api_key)


class YouTubeService:
    """🎬 Servicio para interactuar con la API de YouTube.

    Esta clase encapsula todas las operaciones con la API de YouTube.
    Proporciona métodos simples para buscar videos, canales, obtener detalles, etc.
    """

    def __init__(self, config: Optional[YouTubeConfig] = None):
        """🚀 Inicializa el servicio de YouTube.

        Args:
            config: Configuración del servicio. Si es None, se carga desde variables de entorno.

        Ejemplo:
            # Con configuración automática desde .env
            service = YouTubeService()

            # Con configuración manual
            config = YouTubeConfig(api_key="tu_api_key_aqui")
            service = YouTubeService(config)
        """
        self.config = config or YouTubeConfig.from_env()
        self._client = None

    @property
    def client(self):
        """🔌 Cliente de la API de YouTube (lazy loading).

        Lazy loading significa que el cliente solo se crea cuando se usa por primera vez.
        Esto ahorra recursos si creamos el servicio pero no lo usamos inmediatamente.

        💡 Patrón de diseño: Singleton + Lazy Initialization
        """
        if self._client is None:
            self._client = build(
                self.config.api_service_name,
                self.config.api_version,
                developerKey=self.config.api_key
            )
        return self._client

    def search_videos(
        self,
        query: str,
        max_results: int = 5,
        order: str = 'relevance',
        region_code: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """🔍 Busca vídeos en YouTube basándose en una consulta.

        Args:
            query: 🔎 Término de búsqueda (ej: "Python tutorial")
            max_results: 🔢 Número máximo de resultados (1-50, por defecto 5)
            order: 📊 Orden de los resultados:
                - 'relevance': Por relevancia (default) ⭐
                - 'date': Más recientes primero 📅
                - 'rating': Mejor valorados ⭐⭐⭐⭐⭐
                - 'viewCount': Más vistos primero 👀
                - 'title': Orden alfabético 🔤
            region_code: 🌍 Código de región ISO 3166-1 alpha-2 (ej: 'ES', 'US', 'MX')
            language: 🗣️ Código de idioma ISO 639-1 (ej: 'es', 'en', 'fr')

        Returns:
            📦 Diccionario con los resultados de la búsqueda:
            {
                'success': bool,      # ✅ True si la búsqueda fue exitosa
                'query': str,         # 🔎 Término buscado
                'total_results': int, # 🔢 Cantidad de videos encontrados
                'videos': [...]       # 📹 Lista de videos con sus datos
            }

        Raises:
            HttpError: ❌ Si hay un error en la llamada a la API de YouTube

        Ejemplo:
            >>> service = YouTubeService()
            >>> results = service.search_videos("Python", max_results=3)
            >>> print(f"Encontrados: {results['total_results']} videos")
        """
        try:
            # 🎯 Configuramos los parámetros de búsqueda
            search_params = {
                'q': query,  # 🔎 Query de búsqueda
                'part': 'id,snippet',  # 📦 Pedimos ID y datos básicos (snippet)
                # 🛡️ Limitamos a 50 (límite de la API)
                'maxResults': min(max_results, 50),
                # � Solo buscamos videos (no canales ni playlists)
                'type': 'video',
                'order': order  # 📊 Orden de resultados
            }

            # 🌍 Agregar filtro de región si se especificó
            if region_code:
                search_params['regionCode'] = region_code

            # 🗣️ Agregar preferencia de idioma si se especificó
            if language:
                search_params['relevanceLanguage'] = language

            # 🚀 Ejecutamos la búsqueda en la API de YouTube
            search_response = self.client.search().list(**search_params).execute()

            # 📝 Procesamos los resultados y los convertimos a un formato más amigable
            videos = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                video = {
                    'video_id': video_id,  # 🆔 ID único del video
                    'title': item['snippet']['title'],  # 📌 Título del video
                    # 📄 Descripción
                    'description': item['snippet']['description'],
                    # 🔗 URL completa
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    # 🖼️ Miniatura normal
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    # 👤 Nombre del canal
                    'channel_title': item['snippet']['channelTitle'],
                    # 📅 Fecha de publicación
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video)

            # ✅ Retornamos los resultados en un formato estructurado
            return {
                'success': True,
                'query': query,
                'total_results': len(videos),
                'videos': videos
            }

        except HttpError as e:
            # ❌ Error específico de la API de YouTube (cuota excedida, credenciales inválidas, etc.)
            return {
                'success': False,
                'error': f'Error de API de YouTube: {e.resp.status} - {e.content.decode()}',
                'query': query
            }
        except Exception as e:
            # ⚠️ Cualquier otro error inesperado (red, timeout, etc.)
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}',
                'query': query
            }

    def search_channels(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """📺 Busca canales en YouTube con información detallada.

        Combina dos llamadas a la API:
        1. search().list() - Para buscar canales por texto
        2. channels().list() - Para obtener estadísticas y detalles completos

        Args:
            query: 🔎 Término de búsqueda (ej: "returngis")
            max_results: 🔢 Número máximo de canales a retornar (default: 5)

        Returns:
            📦 Diccionario con los canales encontrados e información detallada:
            {
                'success': bool,
                'query': str,
                'total_results': int,
                'channels': [
                    {
                        'channel_id': str,
                        'title': str,
                        'description': str,
                        'url': str,
                        'thumbnail': str,
                        'published_at': str,
                        'subscriber_count': int,  # 👥 Número de suscriptores
                        'video_count': int,       # 📹 Total de videos
                        'view_count': int,        # 👀 Vistas totales
                        'country': str            # 🌍 País del canal
                    }
                ]
            }

        Ejemplo:
            >>> service = YouTubeService()
            >>> canales = service.search_channels("Python", max_results=3)
            >>> print(f"Canal: {canales['channels'][0]['title']}")
            >>> print(f"Suscriptores: {canales['channels'][0]['subscriber_count']}")
        """
        try:
            # 🔍 Paso 1: Buscar canales por texto (obtiene IDs y snippet básico)
            search_response = self.client.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='channel'
            ).execute()

            # 📋 Extraer los IDs de los canales encontrados
            channel_ids = [item['id']['channelId']
                           for item in search_response.get('items', [])]

            if not channel_ids:
                return {
                    'success': True,
                    'query': query,
                    'total_results': 0,
                    'channels': []
                }

            # 📊 Paso 2: Obtener información detallada de los canales
            channels_response = self.client.channels().list(
                part='snippet,statistics,brandingSettings',
                id=','.join(channel_ids)
            ).execute()

            # 🎯 Procesar y combinar la información
            channels = []
            for item in channels_response.get('items', []):
                channel_id = item['id']
                snippet = item['snippet']
                statistics = item.get('statistics', {})
                branding = item.get('brandingSettings', {}).get('channel', {})

                channel = {
                    'channel_id': channel_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'url': f'https://www.youtube.com/channel/{channel_id}',
                    'thumbnail': snippet['thumbnails']['default']['url'],
                    'published_at': snippet['publishedAt'],
                    # 📊 Estadísticas detalladas
                    'subscriber_count': int(statistics.get('subscriberCount', 0)),
                    'video_count': int(statistics.get('videoCount', 0)),
                    'view_count': int(statistics.get('viewCount', 0)),
                    # 🎨 Branding info
                    'country': branding.get('country', 'N/A')
                }
                channels.append(channel)

            return {
                'success': True,
                'query': query,
                'total_results': len(channels),
                'channels': channels
            }

        except HttpError as e:
            return {
                'success': False,
                'error': f'Error de API de YouTube: {e.resp.status} - {e.content.decode()}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
