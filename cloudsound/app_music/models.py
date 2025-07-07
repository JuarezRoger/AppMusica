from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Artist(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Album(models.Model):
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers', null=True, blank=True) # Imagen de la portada del album upload_to especifica la carpeta donde se guardara la imagen
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file = models.FileField(upload_to='tracks/')

    def __str__(self):
        return self.name
    
    
    def player(self):
        return f'''
            <audio controls>
                <source src="/media/{self.file}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        '''
    player.allow_tags = True  # Permite que el HTML se renderice correctamente en el admin de Django
    

class Profile(models.Model): #proxy models
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relaciona el perfil con el usuario
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    tracks = models.ManyToManyField(Track, related_name='playlists') # Many-to-many relacion con los tracks
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    profiel = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
