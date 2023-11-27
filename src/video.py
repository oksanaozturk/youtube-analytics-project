from googleapiclient.discovery import build
import os


class Video:
    """Класс для видео на youtube-канале"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Конструктор атрибутов экземпляра класса
        video_id - id видео
        title - название видео
        url_video - ссылка на видео
        view_count - количество просмотров
        like_count - количество лайков

        :param video_id: id канала
        """
        self.video_id = video_id
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url_video = "https://youtu.be/" + self.video_id
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает название видео"""
        return f"{self.video_title}"


class PLVideo(Video):
    """Класс для плейлиста видео на youtube-канале"""
    def __init__(self, video_id, playlist_id):
        """инициализируется по 'id видео' и 'id плейлиста' """
        super().__init__(video_id)
        self.playlist_id = playlist_id
