from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('api/find-add-track-lyrics/', FindAddTrackLyrics.as_view(), name='find_add_track_lyrics'),
    path('api/recent-tracks/', RecentTracks.as_view(), name='recent_tracks'),
    path('api/all-tracks/', AllTracks.as_view(), name='all_tracks'),
    path('api/track-lyrics/', TrackLyrics.as_view(), name='track-lyrics'),
    path('api/profile-info/', ProfileInfo.as_view(), name='profile-info'),
    path('api/search-tracks/', SearchTracks.as_view(), name='search-tracks'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]