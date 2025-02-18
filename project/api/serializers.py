from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class TrackSerializer(serializers.Serializer):
    track_id = serializers.CharField()
    artist = serializers.CharField()
    track_title = serializers.CharField()
    cover_url = serializers.URLField()
    lyrics = serializers.CharField()
    added_date = serializers.DateTimeField()


class LyricsSerializer(serializers.Serializer):
    artist = serializers.CharField()
    track_title = serializers.CharField()
    cover_url = serializers.URLField()
    lyrics = serializers.CharField()


class ProfileInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
    tracks_count = serializers.IntegerField()
    favorite_artist = serializers.CharField()