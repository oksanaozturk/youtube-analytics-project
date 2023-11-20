import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется. Дальше все данные будут подтягиваться по API.
        channel_id - id канала
        title - название канала
        description - описание канала
        url - ссылка на канал
        subscribers_count - количество подписчиков
        video_count - количество видео
        total_views - общее количество просмотров

        :param channel_id: id канала
        """

        self.__channel_id = channel_id
        self.info_channel = Channel.dict_channel(self.__channel_id)

        self.title = self.info_channel['items'][0]['snippet']['title']
        self.description: str = self.info_channel['items'][0]['snippet']['description']
        self.url: str = f'https://www.youtube.com/{self.info_channel["items"][0]["snippet"]["customUrl"]}'
        self.subscribers_count: int = int(self.info_channel['items'][0]['statistics']['subscriberCount'])
        self.video_count: int = int(self.info_channel['items'][0]['statistics']['videoCount'])
        self.total_views: int = int(self.info_channel['items'][0]['statistics']['viewCount'])

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону"""
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        """Складывает количество подписчиков двух каналов"""
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other):
        """Вычитает количество подписчиков у двух каналов"""
        return self.subscribers_count - other.subscribers_count

    def __gt__(self, other):
        """Сравнивает на каком канале большее количество подписчиков"""
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other):
        """Сравнивает «больше или равно»"""
        return self.subscribers_count >= other.subscribers_count

    def __lt__(self, other):
        """Сравнивает на каком канале меньшее количество подписчиков"""
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        """Сравнивает «меньше или равно»"""
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other):
        """Определяет равенство"""
        return self.subscribers_count == other.subscribers_count

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def dict_channel(cls, channel_id: str) -> dict:
        """
        создает словарь с данными по каналу
        :returns: Dictionary with info about the channel
        """
        info_channel = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return info_channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info_channel_print = json.dumps(channel, indent=2, ensure_ascii=False)
        print(info_channel_print)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename) -> None:
        """Метод, сохраняющий в файл значения атрибутов экземпляра Channel"""

        data = {
            'id_канала': self.__channel_id,
            'название_канала': self.title,
            'описание_канала': self.description,
            'ссылка_на_канал': self.url,
            'количество_подписчиков': self.subscribers_count,
            'количество_видео': self.video_count,
            'общее_количество_просмотров': self.total_views
        }
        with open(filename, 'w', encoding= 'UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
