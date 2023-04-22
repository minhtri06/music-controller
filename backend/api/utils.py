from requests import get, post, put

from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status

from .models import Room, SpotifyToken, CLIENT_ID, CLIENT_SECRET
from .serializers import SpotifyTokenSerializer


BASE_URL = "https://api.spotify.com/v1/me/"


def get_object(queryset):
    if queryset.exists():
        return queryset[0]
    else:
        return None


def refresh_spotify_token(spotify_token):
    expires_in = spotify_token.expires_in
    if expires_in > timezone.now():
        return True
    refresh_token = spotify_token.refresh_token

    response_data = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()

    serializer = SpotifyTokenSerializer(
        spotify_token,
        data={"access_token": response_data.get("access_token")},
        partial=True,
    )

    if serializer.is_valid():
        serializer.save()
        return True

    print(serializer.errors)
    return False


def create_session_if_not_exist(session):
    if not session.exists(session.session_key):
        session.create()
    return session


def request_spotify_api(access_token, endpoint, method="get"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    url = BASE_URL + endpoint
    if method == "post":
        return post(url, headers=headers)

    if method == "put":
        return put(url, headers=headers)

    return get(url, {}, headers=headers)


def get_song_dict(response_data):
    item = response_data.get("item")

    artist_string = ""

    for i, artist in enumerate(item.get("artists")):
        if i > 0:
            artist_string += ", "
        name = artist.get("name")
        artist_string += name

    return {
        "title": item.get("name"),
        "artist": artist_string,
        "duration": item.get("duration_ms"),
        "progress": response_data.get("progress_ms"),
        "image_url": item.get("album").get("images")[0].get("url"),
        "is_playing": response_data.get("is_playing"),
        "votes": 0,
        "id": item.get("id"),
    }


def play_song(access_token):
    return request_spotify_api(access_token, "player/play", method="put")


def pause_song(access_token):
    return request_spotify_api(access_token, "player/pause", method="put")


def forward_song(access_token):
    return request_spotify_api(access_token, "player/next", method="post")


def check_access_token_existent(room_code):
    room = get_object(Room.objects.filter(code=room_code))
    if room is None:
        return None, Response(
            {"detail": "you do not have a room code"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if room.spotify_token is None:
        return None, Response(
            {"detail": "room not found"}, status=status.HTTP_404_NOT_FOUND
        )

    return room.spotify_token.access_token, None


def room_code_get_room(room_code):
    room = get_object(Room.objects.filter(code=room_code))
    if room is None:
        return None, Response(
            {"detail": "you do not have a room code"},
            status=status.HTTP_404_NOT_FOUND,
        )
    return room, None


def room_get_token(room):
    if room.spotify_token is None:
        return None, Response(
            {"detail": "room not found"}, status=status.HTTP_404_NOT_FOUND
        )
    return room.spotify_token.access_token, None
