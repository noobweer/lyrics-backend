from .models import AppUsers, UsersTracks
import spotipy
import requests
from yandex_music import Client
from spotipy.oauth2 import SpotifyClientCredentials
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Q
import re
import random
import string
from .keys import *

client_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SERVER)
sp = spotipy.Spotify(client_credentials_manager=client_manager)
client = Client().init()


def is_valid_spotify_track_url(url):
    pattern = r'^https://open.spotify.com/track/[a-zA-Z0-9]+(\?si=[a-zA-Z0-9]+)?$'
    return re.match(pattern, url) is not None


def is_valid_yandex_track_url(url):
    pattern = r'^https://music.yandex.ru/album/\d+/track/\d+(\?[^ ]*)?$'
    return re.match(pattern, url) is not None


# def get_track_info(track_url):
#     if is_valid_spotify_track_url(track_url):
#         return get_spotify_track_info(track_url)
#     elif is_valid_yandex_track_url(track_url):
#         return get_yandex_track_info(track_url)
#     else:
#         raise ValueError("Invalid track URL")


def get_spotify_track_info(track_url):
    track_id = track_url.split('/')[-1].split('?')[0]
    info = sp.track(track_id)
    track_name = info['name']
    artists = [artist['name'] for artist in info['artists']]
    artists_names = ', '.join(artists)
    album_cover = info['album']['images'][1]['url']
    return track_name, artists_names, album_cover


def get_yandex_track_info(track_url):
    track_id = track_url.split('/track/')[1].split('?')[0]
    track = client.tracks(track_id)[0]
    track_name = track.title
    artists = ', '.join([artist.name for artist in track.artists])
    album_cover = 'https://' + track.cover_uri.replace('%%', '300x300') if track.cover_uri else None
    return track_name, artists, album_cover


def get_lyrics(track, artist):
    try:
        url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

        querystring = {'apikey': MUSIXMATCH_KEY, 'q_track': track, 'q_artist': artist}
        response = requests.request("GET", url, params=querystring).json()
        lyrics = response['message']['body']['lyrics']['lyrics_body']
        return lyrics
    except Exception as e:
        return False


# def generate_track_id():
#     characters = string.ascii_lowercase + string.digits
#     while True:
#         track_id = ''.join(random.choice(characters) for _ in range(6))
#         try:
#             if not UsersTracks.objects.filter(track_id=track_id).exists():
#                 return track_id
#         except IntegrityError:
#             continue


def save_user_track_lyrics(username, track_id, artist, track, cover_url, lyrics):
    try:
        username = AppUsers.objects.get(username=username)
        existing_track = UsersTracks.objects.filter(
            username=username,
            artist=artist,
            track_title=track,
        ).exists()

        if existing_track:
            return False

        new_track = UsersTracks(
            username=username,
            artist=artist,
            track_id=track_id,
            track_title=track,
            cover_url=cover_url,
            lyrics=lyrics
        )
        new_track.save()
        return True

    except ObjectDoesNotExist:
        print(f"User {username} does not exist.")
        return False
    except Exception as e:
        print(f"Error saving track: {e}")
        return False


def register_user(username, name):
    if AppUsers.objects.filter(username=username).exists():
        print(f"User already exists: {username}")
        return False

    new_user = AppUsers(
        username=username,
        name=name,
        registration_date=timezone.now()
    )
    new_user.save()
    print(f"User registered: {username}")
    return True


def get_recent_tracks(username):
    tracks = UsersTracks.objects.filter(username=username).order_by('-added_date')[:5]
    return tracks


def get_all_tracks(username):
    tracks = UsersTracks.objects.filter(username=username)
    return tracks


def track_lyrics(track_id):
    track = UsersTracks.objects.get(track_id=track_id)
    return track


def get_profile_info_stats(username):
    profile_info = AppUsers.objects.get(username=username)
    return profile_info


def increase_tracks_count(username):
    user = AppUsers.objects.select_for_update().get(username=username)
    user.tracks_count += 1
    user.save()


def search_track(username, query):
    q_object = Q(track_title__icontains=query) | Q(artist__icontains=query)
    tracks = UsersTracks.objects.filter(username=username).filter(q_object)
    return tracks
