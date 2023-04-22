from django.db import models
import string
import random


CLIENT_ID = "e6eba790aa7c4cfaa253ee667d304967"
CLIENT_SECRET = "31238e1772064699bc130cee51bdc310"
REDIRECT_URI = "http://localhost:3000/handle-spotify-code"


def generate_unique_code():
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=8))
        if Room.objects.filter(code=code).exists() is False:
            break
    return code


class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    spotify_token = models.OneToOneField(
        "api.SpotifyToken", on_delete=models.CASCADE, null=True
    )


class SpotifyToken(models.Model):
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
