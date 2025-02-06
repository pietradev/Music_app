from dotenv import load_dotenv
import requests, os
from requests import post, get
import base64
import json 

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    if result.status_code == 200:
        return json.loads(result.content)["access_token"]
    else:
        print("Token Error:", result.status_code, result.text)
        return None

def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

def search_playlists(token, query, limit=1):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": query,
        "type": "playlist",
        "limit": limit
    }
    response = get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Search failed: {response.status_code}")
        return []
    return json.loads(response.content).get("playlists", {}).get("items", [])

def get_playlist_tracks(token, playlist_id, limit=5):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = get_auth_header(token)
    params = {"limit": limit}
    response = get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch tracks: {response.status_code}")
        return []
    return json.loads(response.content).get("items", [])

def main():
    token = get_token()
    if not token:
        print("Failed to get token.")
        return

    # Search for playlists
    playlists = search_playlists(token, "Brazilian MPB", limit=5)
    if not playlists:
        print("No playlists found.")
        return

    # Process the first playlist
    first_playlist = playlists[0]
    playlist_id = first_playlist.get("id")
    if not playlist_id:
        print("Playlist has no ID.")
        return

    print(f"\nPlaylist Name: {first_playlist['name']}")
    print(f"Owner: {first_playlist['owner']['display_name']}")

    # Get tracks from the playlist
    tracks = get_playlist_tracks(token, playlist_id)
    if not tracks:
        print("No tracks found.")
        return

    # First, sort the tracks by the 'popularity' key inside each track's data.
    sorted_tracks = sorted(
        tracks, 
        key=lambda t: t.get("track", {}).get("popularity", 0), 
        reverse=True
    )

    print("\nTop Tracks (Ordered by Popularity):")
    for idx, track in enumerate(sorted_tracks):
        track_data = track.get("track", {})
        artists = ", ".join([artist["name"] for artist in track_data.get("artists", [])])
        print(f"{idx + 1}. {artists} - {track_data.get('name')} (Popularity: {track_data.get('popularity', 'N/A')})")

if __name__ == "__main__":
    main()