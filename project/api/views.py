from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .utils import *

from .services.helpers_service import HelpersService
from .services.track_service import get_track_info
from .services.lyrics_service import LyricsService
from .services.database_service import UserManagementService, TrackManagementService, StatsManagementService


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


class AddTrackService:
    def add_track(self, username, track_url):
        try:
            track_title, artists, cover_url = get_track_info(track_url)
            success, result = LyricsService.get_lyrics(track_title, artists)
            if not success:
                return False, f'Couldnt find song lyrics ({track_title}, {artists})'
            track_id = HelpersService().generate_track_id()
            is_saved = TrackManagementService().save_track(username, track_id, artists, track_title, cover_url, result)
            if is_saved:
                StatsManagementService().increase_tracks_count(username)
                return True, f'Track {track_title} by {artists} added (ID: {track_id})'
            else:
                return False, f'Track {track_title} by {artists} already exists'
        except ValueError as e:
            return False, str(e)


class AddTrack(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        track_url = request.data.get('url')

        success, message = AddTrackService().add_track(username, track_url)
        if success:
            return Response({'is_added': True, 'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response({'is_added': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)


class RecentTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username

        try:
            tracks = TrackManagementService().recent_tracks(username)
            serializer = TrackSerializer(tracks, many=True)
            return Response({'recent_tracks': serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TrackCursorPagination(CursorPagination):
    page_size = 20
    ordering = 'added_date'
    cursor_query_param = 'cursor'


class AllTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = TrackCursorPagination

    def get(self, request, *args, **kwargs):
        username = request.user.username

        try:
            tracks = TrackManagementService().all_tracks(username)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(tracks, request, view=self)
            serializer = TrackSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TrackLyrics(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        track_id = request.query_params.get('track_id')

        try:
            track_info = TrackManagementService().track_lyrics(track_id)
            serializer = LyricsSerializer(track_info)
            return Response({'track_lyrics': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username

        try:
            profile_info = UserManagementService().profile_info(username)
            serializer = ProfileSerializer(profile_info)
            return Response({'profile_info': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchTracks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        query = request.query_params.get('query')

        try:
            tracks = search_track(username, query)
            serializer = SearchSerializer(tracks, many=True)
            return Response({"search_tracks": serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
