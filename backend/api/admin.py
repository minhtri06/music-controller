from django.contrib import admin

from .models import Room, SpotifyToken

from django.contrib.sessions.models import Session

admin.site.register(Room)
admin.site.register(SpotifyToken)
admin.site.register(Session)
