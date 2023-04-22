from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from rest_framework import status

from .serializers import RoomSerializer, SpotifyTokenSerializer
from .models import Room, SpotifyToken, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# from .utils import (
#     get_object,
#     refresh_spotify_token,
#     create_session_if_not_exist,
#     request_spotify_api,
#     get_song_dict,
#     play_song,

# )
from . import utils

import requests


class RoomList(APIView):
    def get(self, request):
        """
        Get information of all rooms
        """
        session = self.request.session
        if not session.exists(session.session_key):
            print("RoomList:get")
            session.create()

        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a room
        """
        session = self.request.session
        if not session.exists(session.session_key):
            print("RoomList:post")
            session.create()

        data = request.data
        data["host"] = session.session_key

        serializer = RoomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            new_room = serializer.data
            self.request.session["room_code"] = new_room["code"]
            return Response(new_room, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(APIView):
    def get_object(self, code):
        return get_object_or_404(Room, code=code)

    def get(self, request, code):
        """
        Get information of a room
        """
        session = self.request.session
        if not session.exists(session.session_key):
            print("RoomDetail:get")
            session.create()

        # Find the room that the user host
        roomQuerySet = Room.objects.filter(host=session.session_key)

        if roomQuerySet.exists():
            # If user already host a room
            room = roomQuerySet[0]
            if room.code != code:
                # If the room wanna join is not the room that user host, forbidden.
                return Response(
                    {"message": "you host another room, you cannot join"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                # If the user don't host a room, user can join.
                session["room_code"] = code
                data = RoomSerializer(room).data
                data["is_host"] = data["host"] == session.session_key
                return Response(data, status=status.HTTP_200_OK)
        else:
            # If user not host any room
            room = self.get_object(code)
            session["room_code"] = code
            data = RoomSerializer(room).data
            data["is_host"] = data["host"] == session.session_key
            return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, code):
        """
        Update a room
        """
        session = self.request.session
        if not session.exists(session.session_key):
            print("RoomDetail:patch")
            session.create()

        room = self.get_object(code)
        # If the user is not the host of the room, that user cannot modify
        # that room
        if room.host != session.session_key:
            return Response(
                {"message": "just the host can modify room"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = RoomSerializer(
            room,
            data={
                "guest_can_pause": request.data.get("guest_can_pause"),
                "votes_to_skip": request.data.get("votes_to_skip"),
            },
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    def post(self, request, code):
        """
        Join a room
        """
        session = self.request.session

        if not session.exists(session.session_key):
            print("JoinRoom:post")
            session.create()

        # If the user already host another room, that user can not join
        if Room.objects.filter(host=session.session_key).exists():
            return Response(
                {"message": "you can not join a room when host another room"},
                status=status.HTTP_403_FORBIDDEN,
            )

        room = get_object_or_404(Room, code=code)
        self.request.session["room_code"] = room.code
        return Response(
            {
                "message": "room joined",
                "room_code": room.code,
            },
            status=status.HTTP_200_OK,
        )


class GetCurrentRoomCode(APIView):
    def get(self, request):
        """
        Get the current room the user joined
        """
        session = self.request.session
        if not session.exists(session.session_key):
            print("GetCurrentRoomCode")
            session.create()

        room_code = self.request.session.get("room_code")
        return Response({"room_code": room_code}, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request):
        session = self.request.session

        if session.exists(session.session_key):

            room_code = session.pop("room_code")
            try:
                # If the session leaves the room is the host of that room,
                # then delete that room
                room = Room.objects.get(code=room_code, host=session.session_key)
                room.delete()
            except Room.DoesNotExist:
                pass

        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_auth_url(request):
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    url = (
        requests.Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "scope": scope,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
            },
        )
        .prepare()
        .url
    )
    return Response({"url": url}, status=status.HTTP_200_OK)


class HandleSpotifyRedirect(APIView):
    def post(self, request):
        session = self.request.session
        if not session.exists(session.session_key):
            session.create()

        code = request.data.get("code")

        data = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        ).json()
        expires_in = timezone.now() + timedelta(seconds=data["expires_in"])
        token_serializer = SpotifyTokenSerializer(
            data={
                "access_token": data["access_token"],
                "refresh_token": data["refresh_token"],
                "expires_in": expires_in,
                "token_type": data["token_type"],
            }
        )
        if token_serializer.is_valid():
            token = token_serializer.save()
            room = Room.objects.get(host=session.session_key)
            room.spotify_token = token
            room.save()
            return Response(
                {"message": "get token successfully!", "room_code": room.code},
                status=status.HTTP_200_OK,
            )
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    def patch(self, request, room_code):

        spotify_token = utils.get_object(
            SpotifyToken.objects.filter(room__code=room_code)
        )
        print(spotify_token)

        if spotify_token:
            if utils.refresh_spotify_token(spotify_token):
                return Response(
                    {"detail": "refresh token successfully"}, status=status.HTTP_200_OK
                )
            return Response(
                {"detail": "refresh failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentSong(APIView):
    def get(self, request):
        ENDPOINT = "player/currently-playing"
        session = utils.create_session_if_not_exist(self.request.session)
        room_code = session.get("room_code")

        if room_code is None:
            return Response(
                {"detail": "you don't have a room code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        room = utils.get_object(Room.objects.filter(code=room_code))
        if room is None:
            return Response(
                {"detail": "room code does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if room.spotify_token is None:
            return Response(
                {"detail": "this room is not authenticated"},
                status=status.HTTP_403_FORBIDDEN,
            )

        access_token = room.spotify_token.access_token
        response = utils.request_spotify_api(access_token, ENDPOINT, "get")
        if response.status_code != 200:
            return Response({}, status=response.status_code)

        response_data = response.json()

        if "error" in response_data or "item" not in response_data:
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)

        song = utils.get_song_dict(response_data)

        return Response(song, status=status.HTTP_200_OK)


class PlaySong(APIView):
    def put(self, request):
        session = utils.create_session_if_not_exist(self.request.session)
        room_code = session.get("room_code")

        if room_code is None:
            return Response(
                {"detail": "you do not have a room code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        room = utils.get_object(Room.objects.filter(code=room_code))
        if room is None:
            return Response(
                {"detail": "invalid room code"}, status=status.HTTP_400_BAD_REQUEST
            )

        if room.host != session.session_key and room.guest_can_pause is False:
            return Response(
                {"detail": "you do not have permission to play song"},
                status=status.HTTP_403_FORBIDDEN,
            )

        utils.play_song(room.spotify_token.access_token)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PauseSong(APIView):
    def put(self, request):
        session = utils.create_session_if_not_exist(self.request.session)
        room_code = session.get("room_code")
        if room_code is None:
            return Response(
                {"detail": "you do not have a room code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        room = utils.get_object(Room.objects.filter(code=room_code))
        if room is None:
            return Response(
                {"detail": "invalid room code"}, status=status.HTTP_400_BAD_REQUEST
            )

        if room.host != session.session_key and room.guest_can_pause is False:
            print(room.guest_can_pause)
            return Response(
                {"detail": "you do not have permission to pause song"},
                status=status.HTTP_403_FORBIDDEN,
            )

        utils.pause_song(room.spotify_token.access_token)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ForwardSong(APIView):
    def post(self, request):
        session = utils.create_session_if_not_exist(self.request.session)
        room_code = session.get("room_code")

        room, err_response = utils.room_code_get_room(room_code)
        if room is None:
            return err_response

        if session.session_key == room.host:
            access_token, err_response = utils.room_get_token(room)
            if access_token is None:
                return err_response

            utils.forward_song(access_token)
        else:
            pass

        return Response({}, status=status.HTTP_204_NO_CONTENT)
