from googleapiclient.discovery import build
import os
import isodate
import datetime


class PlayList:
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """
        Конструктор атрибутов экземпляра класса
        playlist_id - id плейлиста
        title - название плейлиста
        url - ссылка на плейлист
        :param playlist_id: id плейлиста
        self.playlist_id = self.get_playlist_info()["items"][0]["id"]
        """
        self.playlist_id = playlist_id
        self.title = self.get_playlist_info()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.get_playlist_info()["items"][0]["id"]}'

    def get_playlist_info(self) -> dict:
        """
        Метод создает словарь с данными по пейлисту
        """
        playlist_info = self.youtube.playlists().list(id=self.playlist_id,
                                                      part='contentDetails,snippet',
                                                      maxResults=50, ).execute()

        # playlist_info_1 = json.dumps(playlist_info, indent=2, ensure_ascii=False)
        return playlist_info

    @property
    def total_duration(self):
        """
        Метод для суммирования длительности всех видео в плейлисте.
        """
        # Получаем данные по видеороликам в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        # return json.dumps(playlist_videos, indent=2, ensure_ascii=False)

        # Получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Получение длительности видеороликов из плейлиста
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        # return json.dumps(video_response, indent=2, ensure_ascii=False)

        # Список, в который будет сохраняться информация о длительности видео
        video_list_duration = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            video_list_duration.append(duration)

        # Переменная для хранения общей длительности видео
        total_duration = sum(video_list_duration, datetime.timedelta())

        return total_duration

    def show_best_video(self):
        """
        Метод, возвращающий ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        # Получаем данные по видеороликам в плейлисте
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        # return json.dumps(playlist_videos, indent=2, ensure_ascii=False)

        # Получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # print(video_ids)

        # Получение статистики видео по его id
        video_statistics = self.youtube.videos().list(part='statistics', id=video_ids).execute()
        # print(json.dumps(video_statistics, indent=2, ensure_ascii=False))

        #  Получаем все like_count видео из video_response
        like_count_list = [(video['id'], int(video['statistics']['likeCount'])) for video in video_statistics['items']]
        # print(like_count_list)

        #  Получаем видео с максимальным like_count
        best_video_id, _ = max(like_count_list, key=lambda value: value[1])
        # print(best_video_id)
        return f"https://youtu.be/{best_video_id}"
