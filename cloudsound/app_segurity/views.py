from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.


def home(request):
    if request.user.is_authenticated: # Verifica si el usuario ya está autenticado 
        return redirect(reverse('cloudsound:home'))
    
    return render(request, 'security/login.html')

def sigin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Aquí iría la lógica para autenticar al usuario
        # Por ejemplo, usando Django's authenticate y login

        user= authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('cloudsound:home'))
            else:
                pass
        else:
            messages.add_message(request, messages.INFO, "Usuario y/o contraseña incorrectos")
            return redirect('/')
    else:
        return HttpResponse('Error en el metodo')
    
def signout(request):
    logout(request)
    return redirect('/')