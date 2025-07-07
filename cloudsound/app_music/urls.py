from django.urls import path
from . import views

app_name = 'cloudsound'

urlpatterns = [
    path('', views.home, name='home'),
    path('album/<int:id>/', views.album, name='album'),
    path('artist/<int:id>/', views.artist, name='artist'),
    path('profile/<int:id>/', views.user_profile, name='user_profile'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<int:id>/add/tracks', views.add_tracks_views, name='add_tracks_views'),
]

