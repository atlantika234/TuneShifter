from django.urls import path
from spotify.views.general import redirect_view, get_token, get_playlist, create_platlist

urlpatterns = [
    path('authorize/', redirect_view, name='redirect_to_authorize'),
    path('token/', get_token, name='get_token'),
    path('playlist/', get_playlist, name='get user playlist'),
    path('create_platlist/', create_platlist, name='create_platlist'),
]