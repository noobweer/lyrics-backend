from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .utils import *


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        name = request.data.get('name')

        if serializer.is_valid():
            serializer.save()
            register_user(username, name)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindAddTrackLyrics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        track_url = request.data.get('url')

        try:
            track_name, artist_name, cover_url = get_track_info(track_url)
            lyrics = get_song_lyrics(track_name, artist_name)
            track_id = generate_track_id()
            if not lyrics:
                return Response({'is_added': False, 'message': 'Could not find song lyrics'},
                                status=status.HTTP_404_NOT_FOUND)
            is_added = save_user_track_lyrics(username, track_id, artist_name, track_name, cover_url, lyrics)
            if is_added:
                increase_tracks_count(username)
                return Response({'is_added': True, 'message': f'Track {track_name} by {artist_name} added (ID: {track_id})'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'is_added': False, 'message': f'Track {track_name} by {artist_name} already exists'},
                                status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'is_added': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'is_added': False, 'message': 'An error occurred while processing the request'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecentTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username

        try:
            tracks = get_recent_tracks(username)
            serializer = TrackSerializer(tracks, many=True)
            return Response({'recent_tracks': serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        tracks = get_all_tracks(username)
        serializer = TrackSerializer(tracks, many=True)
        return Response({'all_tracks': serializer.data}, status=status.HTTP_200_OK)


class TrackLyrics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        track_id = request.data.get('track_id')
        track_info_lyrics = track_lyrics(track_id)
        serializer = LyricsSerializer(track_info_lyrics)
        return Response({'track_lyrics': serializer.data}, status=status.HTTP_200_OK)


class ProfileInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        profile_info = get_profile_info_stats(username)
        serializer = ProfileInfoSerializer(profile_info)
        return Response({'profile_info': serializer.data}, status=status.HTTP_200_OK)


class SearchTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        query = request.data.get('query')

        tracks = search_track(username, query)
        serializer = TrackSerializer(tracks, many=True)

        return Response({"search_tracks": serializer.data}, status=status.HTTP_200_OK)