from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('add-track/', AddTrack.as_view(), name='find_add_track_lyrics'),
    path('recent-tracks/', RecentTracks.as_view(), name='recent_tracks'),
    path('all-tracks/', AllTracks.as_view(), name='all_tracks'),
    path('track-lyrics/', TrackLyrics.as_view(), name='track-lyrics'),
    path('profile-info/', ProfileInfo.as_view(), name='profile-info'),
    path('search-tracks/', SearchTracks.as_view(), name='search-tracks'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]
