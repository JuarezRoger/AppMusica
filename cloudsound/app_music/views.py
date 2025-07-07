from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
# Create your views here.

@login_required
def home(request):
    albumes = Album.objects.all().order_by('-id')[:10]
    artist = Artist.objects.all().order_by('name')
    ctx = {
        'albumes': albumes,
        'artist': artist,
    }

    return render(request, 'music/home.html', ctx)

@login_required
def album(request, id):
    album = get_object_or_404(Album, id=id) # Si el album no existe, se devuelve un error 404
   
    tracks = Track.objects.filter(album=album)
    ctx = {
        'album': album,
        'tracks': tracks,
    }
    return render(request, 'music/album.html', ctx)

@login_required
def artist(request, id):
    artist = get_object_or_404(Artist, id=id) # Si el album no existe, se devuelve un error 404
   
    ctx = {
        'artist': artist,
    }
    return render(request, 'music/artista.html', ctx)

@login_required
def user_profile(request, id):
    if id != request.user.id: # Verifica si el id del usuario es diferente al del usuario logueado 
        user_ = get_object_or_404(User, id=id)  # Obtiene el perfil del usuario
        playlists = None
    else:
        user_=None
        playlists = Playlist.objects.filter(owner=request.user)  # Obtiene las playlists del usuario logueado

    ctx = {
        'id':id,  # Obtiene el perfil del usuario
        'user': user_,
        'playlists': playlists,  # Obtiene las playlists del usuario logueado
    }

    return render(request, 'music/profile.html',ctx)

@login_required
def playlist(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        action = request.GET.get('action')

        if action == 'search':
            s = request.GET.get('s')  # Obtiene el parámetro de búsqueda
            tracks = Track.objects.filter(name__startswith=s)

            if tracks:
                tr = ''
                for track in tracks:
                    tr += f'''
                        <tr>
                            <td>{track.name}</td>
                            <td class="text-right">
                                <a href="#" class="a-add-track" data-url="{reverse('cloudsound:playlist')}" data-id="{track.id}">Add to Playlist</a>
                            </td>
                        </tr>
                    '''

                table = f'''
                    <p class="font-weight-bold text-success">{tracks.count()} tracks found</p>
                    <table class="table table-hover table-bordered">{tr}</table>
                '''
                return JsonResponse({'OK': True, 'msg': table})
            else:
                m = f'<span class="text-danger">La búsqueda <strong>{s}</strong> no ha devuelto resultados</span>'
                return JsonResponse({'OK': False, 'msg': m})
            

        elif action == 'add-track-to-pl':
            idt = request.GET.get('idt')
            idp = request.GET.get('idp')

            pl = Playlist.objects.get(id=idp)
            track = Track.objects.get(id=idt)


            #Validar que los datos existen
            if track in pl.tracks.all():
                return JsonResponse({'OK': False, 'msg': 'Track already exists in the playlist'})
            else:
                pl.tracks.add(track)  # Agrega la pista a la playlist

                return JsonResponse({'OK': True, 'msg': 'Track added to the playlist'})

        elif action == 'remove-track-from-pl':
            idt = request.GET.get('idt')
            idp = request.GET.get('idp')

            pl = Playlist.objects.get(id=idp)
            track = Track.objects.get(id=idt)

            # Validar que los datos existen
            if track in pl.tracks.all():
                pl.tracks.remove(track)
            return JsonResponse({'OK': True, 'msg': 'Track removed from the playlist'})
        
        
    if request.method == 'POST':
        pln = request.POST.get('playlist-name')
        Playlist.objects.create(name=pln, owner=request.user)

        return redirect(reverse('cloudsound:user_profile', args=[request.user.id]))

    elif request.method == 'GET':
        id = request.GET.get('id')

        if id:
            pl = get_object_or_404(Playlist, id=id)

            if pl.owner == request.user:
                pl.delete()  # Elimina la playlist
                return redirect(reverse('cloudsound:user_profile', args=[request.user.id]))
            else:
                raise Http404("You do not have permission to delete this playlist")
        else:
            raise Http404("Playlist not found")


@login_required
def add_tracks_views(request, id):

    pl = get_object_or_404(Playlist, id=id)
    if pl.owner == request.user:

        return render(request, 'music/add_tracks.html', {'pl':pl})
    else:
        raise Http404("You do not have permission to add tracks to this playlist")