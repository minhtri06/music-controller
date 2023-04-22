from django.urls import path

from . import views

urlpatterns = [
    path("", views.RoomList.as_view()),
    path("<str:code>/join/", views.JoinRoom.as_view()),
    path("<str:code>/", views.RoomDetail.as_view()),
    path("room/get-room-code/", views.GetCurrentRoomCode.as_view()),
    path("room/leave-room/", views.LeaveRoom.as_view()),
    path("spotify/get-auth-url/", views.get_auth_url),
    path("spotify/handle-redirect/", views.HandleSpotifyRedirect.as_view()),
    path("spotify/refresh-token/<str:room_code>/", views.RefreshToken.as_view()),
    path("spotify/get-current-song/", views.CurrentSong.as_view()),
    path("spotify/play-song/", views.PlaySong.as_view()),
    path("spotify/pause-song/", views.PauseSong.as_view()),
    path("spotify/forward-song/", views.ForwardSong.as_view()),
]
