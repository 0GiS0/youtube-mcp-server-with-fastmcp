"""
YouTube API Service

Este módulo centraliza toda la configuración y las llamadas a la API de Google YouTube.
Proporciona una capa de abstracción para interactuar con la API de YouTube de manera
consistente y manejando errores apropiadamente.
"""

import os
from typing import Optional, Dict, List, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass


@dataclass
class YouTubeConfig:
    """Configuración para el servicio de YouTube API."""
    api_key: str
    api_service_name: str = "youtube"
    api_version: str = "v3"

    @classmethod
    def from_env(cls) -> 'YouTubeConfig':
        """Crea una configuración desde variables de entorno."""
        api_key = os.getenv("YOUTUBE_API_KEY", "")
        if not api_key:
            raise ValueError(
                "YOUTUBE_API_KEY no está configurada. "
                "Por favor, configura la variable de entorno. "
                "Obtén tu API key desde: https://console.cloud.google.com/apis/credentials"
            )
        return cls(api_key=api_key)


class YouTubeService:
    """Servicio para interactuar con la API de YouTube."""

    def __init__(self, config: Optional[YouTubeConfig] = None):
        """
        Inicializa el servicio de YouTube.

        Args:
            config: Configuración del servicio. Si es None, se carga desde variables de entorno.
        """
        self.config = config or YouTubeConfig.from_env()
        self._client = None

    @property
    def client(self):
        """Cliente de la API de YouTube (lazy loading)."""
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
        """
        Busca vídeos en YouTube basándose en una consulta.

        Args:
            query: Término de búsqueda.
            max_results: Número máximo de resultados (1-50).
            order: Orden de los resultados (relevance, date, rating, viewCount, title).
            region_code: Código de región ISO 3166-1 alpha-2 (ej: 'ES', 'US').
            language: Código de idioma ISO 639-1 (ej: 'es', 'en').

        Returns:
            Diccionario con los resultados de la búsqueda.

        Raises:
            HttpError: Si hay un error en la llamada a la API.
        """
        try:
            search_params = {
                'q': query,
                'part': 'id,snippet',
                'maxResults': min(max_results, 50),  # API limit
                'type': 'video',
                'order': order
            }

            if region_code:
                search_params['regionCode'] = region_code

            if language:
                search_params['relevanceLanguage'] = language

            search_response = self.client.search().list(**search_params).execute()

            videos = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                video = {
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'thumbnail_high': item['snippet']['thumbnails'].get('high', {}).get('url'),
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video)

            return {
                'success': True,
                'query': query,
                'total_results': len(videos),
                'videos': videos
            }

        except HttpError as e:
            return {
                'success': False,
                'error': f'Error de API de YouTube: {e.resp.status} - {e.content.decode()}',
                'query': query
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}',
                'query': query
            }

    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un vídeo específico.

        Args:
            video_id: ID del vídeo de YouTube.

        Returns:
            Diccionario con la información del vídeo.
        """
        try:
            video_response = self.client.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()

            items = video_response.get('items', [])
            if not items:
                return {
                    'success': False,
                    'error': 'Vídeo no encontrado'
                }

            item = items[0]
            snippet = item['snippet']
            statistics = item.get('statistics', {})
            content_details = item.get('contentDetails', {})

            return {
                'success': True,
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'channel_id': snippet['channelId'],
                'channel_title': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'duration': content_details.get('duration'),
                'view_count': statistics.get('viewCount'),
                'like_count': statistics.get('likeCount'),
                'comment_count': statistics.get('commentCount'),
                'tags': snippet.get('tags', []),
                'category_id': snippet.get('categoryId'),
                'url': f'https://www.youtube.com/watch?v={video_id}'
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

    def search_channels(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Busca canales en YouTube.

        Args:
            query: Término de búsqueda.
            max_results: Número máximo de resultados.

        Returns:
            Diccionario con los canales encontrados.
        """
        try:
            search_response = self.client.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='channel'
            ).execute()

            channels = []
            for item in search_response.get('items', []):
                channel_id = item['id']['channelId']
                channel = {
                    'channel_id': channel_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f'https://www.youtube.com/channel/{channel_id}',
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'published_at': item['snippet']['publishedAt']
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

    def get_channel_details(
        self,
        channel_id: str,
        include_statistics: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene información detallada de un canal.

        Args:
            channel_id: ID del canal de YouTube.
            include_statistics: Si se deben incluir estadísticas del canal.

        Returns:
            Diccionario con la información del canal.
        """
        try:
            parts = ['snippet', 'contentDetails']
            if include_statistics:
                parts.append('statistics')

            channel_response = self.client.channels().list(
                part=','.join(parts),
                id=channel_id
            ).execute()

            items = channel_response.get('items', [])
            if not items:
                return {
                    'success': False,
                    'error': 'Canal no encontrado'
                }

            item = items[0]
            snippet = item['snippet']
            statistics = item.get('statistics', {})
            content_details = item.get('contentDetails', {})

            result = {
                'success': True,
                'channel_id': channel_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'custom_url': snippet.get('customUrl'),
                'published_at': snippet['publishedAt'],
                'thumbnail': snippet['thumbnails']['default']['url'],
                'url': f'https://www.youtube.com/channel/{channel_id}',
                'uploads_playlist_id': content_details.get('relatedPlaylists', {}).get('uploads')
            }

            if include_statistics:
                result.update({
                    'subscriber_count': statistics.get('subscriberCount'),
                    'video_count': statistics.get('videoCount'),
                    'view_count': statistics.get('viewCount')
                })

            return result

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

    def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 5,
        order: str = 'date'
    ) -> Dict[str, Any]:
        """
        Obtiene los vídeos más recientes de un canal.

        Args:
            channel_id: ID del canal de YouTube.
            max_results: Número máximo de vídeos a obtener.
            order: Orden de los vídeos (date, rating, relevance, title, viewCount).

        Returns:
            Diccionario con los vídeos del canal.
        """
        try:
            # Primero obtenemos el ID de la playlist de uploads
            channel_details = self.get_channel_details(
                channel_id, include_statistics=False)

            if not channel_details.get('success'):
                return channel_details

            uploads_playlist_id = channel_details.get('uploads_playlist_id')
            if not uploads_playlist_id:
                return {
                    'success': False,
                    'error': 'No se pudo obtener la playlist de vídeos del canal'
                }

            # Obtenemos los vídeos de la playlist
            playlist_response = self.client.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='snippet,contentDetails',
                maxResults=max_results
            ).execute()

            videos = []
            for item in playlist_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                video = {
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video)

            return {
                'success': True,
                'channel_id': channel_id,
                'total_results': len(videos),
                'videos': videos
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

    def get_video_comments(
        self,
        video_id: str,
        max_results: int = 20,
        order: str = 'relevance'
    ) -> Dict[str, Any]:
        """
        Obtiene los comentarios de un vídeo.

        Args:
            video_id: ID del vídeo de YouTube.
            max_results: Número máximo de comentarios.
            order: Orden de los comentarios (relevance, time).

        Returns:
            Diccionario con los comentarios del vídeo.
        """
        try:
            comments_response = self.client.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                order=order,
                textFormat='plainText'
            ).execute()

            comments = []
            for item in comments_response.get('items', []):
                top_comment = item['snippet']['topLevelComment']['snippet']
                comment = {
                    'author': top_comment['authorDisplayName'],
                    'text': top_comment['textDisplay'],
                    'like_count': top_comment['likeCount'],
                    'published_at': top_comment['publishedAt'],
                    'updated_at': top_comment['updatedAt']
                }
                comments.append(comment)

            return {
                'success': True,
                'video_id': video_id,
                'total_results': len(comments),
                'comments': comments
            }

        except HttpError as e:
            # Los comentarios pueden estar deshabilitados
            if e.resp.status == 403:
                return {
                    'success': False,
                    'error': 'Los comentarios están deshabilitados para este vídeo'
                }
            return {
                'success': False,
                'error': f'Error de API de YouTube: {e.resp.status} - {e.content.decode()}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
