import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yandex_music import Client
from abc import ABC, abstractmethod
from ..keys import *
import re


class TrackService(ABC):
    @abstractmethod
    def is_valid_url(self, url):
        pass

    @abstractmethod
    def get_track_info(self, url):
        pass


class SpotifyTrackService(TrackService, ABC):
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=(
            SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SERVER)))

    @staticmethod
    def is_valid_spotify_track_url(url):
        pattern = r'^https://open.spotify.com/track/[a-zA-Z0-9]+(\?si=[a-zA-Z0-9]+)?$'
        return re.match(pattern, url) is not None

    def get_spotify_track_info(self, track_url):
        track_id = track_url.split('/')[-1].split('?')[0]
        info = self.sp.track(track_id)
        track_title = info['name']
        artists = [artist['name'] for artist in info['artists']]
        artists = ', '.join(artists)
        cover_url = info['album']['images'][1]['url']
        return track_title, artists, cover_url


class YandexTrackService(TrackService, ABC):
    def __init__(self):
        self.client = Client().init()

    @staticmethod
    def is_valid_yandex_track_url(url):
        pattern = r'^https://music.yandex.ru/album/\d+/track/\d+(\?[^ ]*)?$'
        return re.match(pattern, url) is not None

    def get_yandex_track_info(self, track_url):
        track_id = track_url.split('/track/')[1].split('?')[0]
        track = self.client.tracks(track_id)[0]
        track_title = track.title
        artists = ', '.join([artist.name for artist in track.artists])
        cover_url = 'https://' + track.cover_uri.replace('%%', '300x300')
        return track_title, artists, cover_url


class TrackServiceFactory:
    SERVICES = {
        'spotify': SpotifyTrackService,
        'yandex': YandexTrackService,
    }

    @staticmethod
    def get_service(url):
        for service_name, service_class in TrackServiceFactory.SERVICES.items():
            if service_class().is_valid_url(url):
                return service_class()
        raise ValueError("Invalid track URL")


def get_track_info(url):
    try:
        service = TrackServiceFactory.get_service(url)
        return service.get_track_info(url)
    except ValueError as e:
        raise ValueError(f"Error getting track info: {e}")
