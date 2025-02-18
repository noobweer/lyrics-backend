from django.db import models
from django.utils import timezone

# Create your models here.


class AppUsers(models.Model):
    username = models.CharField(primary_key=True, max_length=16, unique=True)
    name = models.CharField(max_length=16, default='default_name')
    tracks_count = models.IntegerField(default=0)
    favorite_artist = models.CharField(max_length=255, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UsersTracks(models.Model):
    username = models.ForeignKey(AppUsers, on_delete=models.CASCADE)
    track_id = models.CharField(max_length=6 ,unique=True)
    artist = models.CharField(max_length=255, default='default_artist')
    track_title = models.CharField(max_length=255, default='default_title')
    cover_url = models.URLField(max_length=500, blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.track_title} by {self.artist}"


class UsersFriends(models.Model):
    username = models.ForeignKey(AppUsers, on_delete=models.CASCADE)
    friend_username = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.track_title} by {self.artist}"