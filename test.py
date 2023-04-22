CLIENT_ID = "e6eba790aa7c4cfaa253ee667d304967"
CLIENT_SECRET = "31238e1772064699bc130cee51bdc310"
REDIRECT_URI = "http://localhost:3000/"

import requests

scopes = (
    "user-read-playback-state user-modify-playback-state user-read-currently-playing"
)
url = (
    requests.Request(
        "GET",
        "https://accounts.spotify.com/authorize",
        params={
            "scope": scopes,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        },
    )
    .prepare()
    .url
)

print(url)
