from django.http import HttpResponse
from spotify.views.controllers import Client
from django.shortcuts import redirect
from app.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SCOPES, SPOTIFY_CLIENT_SECRET

state={}
def redirect_view(request):
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={SPOTIFY_CLIENT_SCOPES}&redirect_uri=http://127.0.0.1:8000/spotify/token')


def get_token(request):
    auth_code = request.GET.get("code", None)
    if auth_code:
        token_info = Client.get_token(auth_code)
        if token_info:
            state['access_token'] = token_info['access_token']
            return HttpResponse(f"Полученный токен: {state['access_token']}")
        else:
            return HttpResponse(f"<h1>Ошибка при получении токена.</h1> {auth_code}")
    return HttpResponse("Не удалось получить код атворизации")
    
def get_playlist(request):
    data = Client.get_user_playlists(state['access_token'])
    if data:
        return data
    return HttpResponse("Не удалось получить список плейлистов")

def create_platlist(request):
    data = Client.playlist_transfer(playlist_name="Test Create Playlist", 
                                    access_token=state['access_token'],
                                    playlist_discription = '',
                                    track_name = ['internet love', 'i got u', 'гладиатор/рыцарь']
                                    )
    if data:
        return HttpResponse(f"<h3>Создание успешно</h3>")
    return HttpResponse("<h3>Создание не успешно</h3>")