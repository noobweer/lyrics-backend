import requests
from ..keys import MUSIXMATCH_KEY


class LyricsService:
    @staticmethod
    def get_lyrics(track, artist):
        try:
            url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

            querystring = {'apikey': MUSIXMATCH_KEY, 'q_track': track, 'q_artist': artist}
            response = requests.request("GET", url, params=querystring).json()
            lyrics = response['message']['body']['lyrics']['lyrics_body']
            return True, lyrics
        except Exception as e:
            return False, str(e)
