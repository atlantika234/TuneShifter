import requests
import json
from app.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SCOPES, SPOTIFY_CLIENT_SECRET
from django.http import JsonResponse

class Client:
    @staticmethod
    def get_token(code: str):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/spotify/token",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()  # Возвращаем токен в случае успеха
        else:
            print("Ошибка при получении токена:", response.status_code, response.text)
            return None
    
    def get_user_playlists(access_token: str):
        url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            playlists = response.json()["items"]
            print(playlists)
            return JsonResponse(playlists, safe=False)
        else:
            print(f"Ошибка: {response.status_code}")
            return None
        
    def search_track(track_name: str, access_token: str):
        url = f"https://api.spotify.com/v1/search?q={track_name}&type=track"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            track_uri = response.json()['tracks']['items'][0]['uri']
            return track_uri
        
    def create_playlist(playlist_name: str, access_token: str, playlist_discription: str = None):
        url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": playlist_name,
            "description": playlist_discription,
            "public": False
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()['id']
        else:
            print(f"Ошибка {response.json()}")
            return False
    def playlist_transfer( playlist_name: str, access_token: str, playlist_discription: str, track_name: dict):
        playlist_id = Client.create_playlist(playlist_name, access_token, playlist_discription)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        for i in range (len(track_name)):
            data = {
                "uris": [
                    Client.search_track(track_name=track_name[i], access_token=access_token)
                ],
                "position": i
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 201:
                print(response.json())
        return True
                
        