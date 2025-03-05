##pip install python-dotenv
##pip install reequests


from dotenv import load_dotenv
import requests, os
from requests import post, get
import base64
import json 

## load environment vars here
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


##Getting Access Token from API
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
    result = post(url, headers = headers, data = data)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token
    else:
        return("Error: ", result.status_code, result.text)

def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

##Finding artist - we need to use the search endpoint first (to get the id, and then the track)
def search_for_artist_id(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    return json_result[0]



def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"    
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


# Example: Get top playlists in Brazil (BR)
token = get_token()
result = search_for_artist_id(token, "Anavitoria")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
#print(songs)

for idx, song in enumerate(songs):
    print(f"{idx + 1}.  {song['name']} - Popularity: {song['popularity']}")
