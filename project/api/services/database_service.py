from ..models import AppUsers, UsersTracks
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q


class UserManagementService:
    def __init__(self):
        self.AppUsers = AppUsers.objects

    def register_user(self, username, name):
        if self.AppUsers.filter(username=username).exists():
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

    def profile_info(self, username):
        return self.AppUsers.get(username=username)


class TrackManagementService:
    def __init__(self):
        self.UsersTracks = UsersTracks.objects
        self.AppUsers = AppUsers.objects

    def save_track(self, username, track_id, artist, track, cover_url, lyrics):
        try:
            user = self.AppUsers.get(username=username)
            existing_track = self.UsersTracks.filter(
                username=user,
                artist=artist,
                track_title=track,
            ).exists()
            if existing_track:
                return False
            new_track = UsersTracks(
                username=user,
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

    def recent_tracks(self, username):
        return self.UsersTracks.filter(username=username).order_by('-added_date')[:5]

    def all_tracks(self, username):
        return self.UsersTracks.filter(username=username)

    def search_track(self, username, query):
        q_object = Q(track_title__icontains=query) | Q(artist__icontains=query)
        return self.UsersTracks.filter(username=username).filter(q_object)

    def track_lyrics(self, track_id):
        return self.UsersTracks.get(track_id=track_id)


class StatsManagementService:
    def __init__(self):
        self.AppUsers = AppUsers.objects

    def increase_tracks_count(self, username):
        user = self.AppUsers.select_for_update().get(username=username)
        user.tracks_count += 1
        user.save()

    def decrease_tracks_count(self, username):
        user = self.AppUsers.select_for_update().get(username=username)
        user.tracks_count -= 1
        user.save()
