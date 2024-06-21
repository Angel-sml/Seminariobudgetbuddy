from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskform 

# Función para mostrar la página de inicio
def home(request):
    return render(request, 'home.html')

# Función para gestionar el registro de usuarios
def signup(request):
    # Si el método de la solicitud es GET, se muestra el formulario de registro
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # Verifica si las contraseñas ingresadas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crea un nuevo usuario con el nombre de usuario y contraseña proporcionados
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()  # Guarda el usuario en la base de datos
                login(request, user)  # Inicia sesión con el nuevo usuario
                return redirect('home')  # Redirige a la página de inicio
            except IntegrityError:
                # Si el nombre de usuario ya existe, muestra un error
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": "Username already exists"
                })
        # Si las contraseñas no coinciden, muestra un error
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": "Password do not match"
        })

# Función para gestionar el cierre de sesión
def signout(request):
    logout(request)  # Cierra la sesión del usuario actual
    return redirect('home')  # Redirige a la página de inicio

# Función para mostrar la página de tareas
def tasks(request):
    return render(request, 'tasks.html')

# Función para gestionar la creación de nuevas tareas
def create_tasks(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form': taskform
        })
    else:
        try:
            form = taskform(request.POST)  # Obtiene los datos del formulario de la solicitud POST
            new_task = form.save(commit=False)  # Crea una nueva tarea pero no la guarda aún en la base de datos
            new_task.user = request.user  # Asigna el usuario actual a la nueva tarea
            new_task.save()  # Guarda la nueva tarea en la base de datos
            return redirect('tasks')  # Redirige a la página de tareas
        except ValueError:
            # Si hay un error en los datos del formulario, muestra un mensaje de error
            return render(request, 'create_tasks.html', {
                'form': taskform,
                'error': 'datos incorrectos'
            })

# Función para gestionar el inicio de sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Autentica al usuario con el nombre de usuario y la contraseña proporcionados
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            # Si la autenticación falla, muestra un mensaje de error
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)  # Inicia sesión con el usuario autenticado
            return redirect('home')  # Redirige a la página de inicio
