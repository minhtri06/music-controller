from rest_framework import serializers

from .models import Room, SpotifyToken


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "code",
            "host",
            "guest_can_pause",
            "votes_to_skip",
            "created_at",
            "spotify_token",
        ]


class SpotifyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyToken
        fields = [
            "access_token",
            "refresh_token",
            "created_at",
            "expires_in",
            "token_type",
        ]
