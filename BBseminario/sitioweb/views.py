from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskform, ValueForm
from .models import task
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse

# Lista de productos (ejemplo)
productos = [
    {"nombre": "iPad 10", "precio": 1000000, "imagen": "ipad10.jpeg"},
    {"nombre": "iPhone 13", "precio": 2000000, "imagen": "iphone13.jpeg"},
    {"nombre": "iPhone 14", "precio": 3000000, "imagen": "iphone14.jpeg"},
    {"nombre": "iPhone 15", "precio": 4000000, "imagen": "iphone15.jpeg"},
    {"nombre": "Laptop Asus", "precio": 5000000, "imagen": "lapasus.jpeg"},
    {"nombre": "Laptop HP", "precio": 5000000, "imagen": "laphp.jpeg"},
    {"nombre": "Laptop Lenovo", "precio": 5000000, "imagen": "laplenovo.jpeg"},
    {"nombre": "Televisor LG 50", "precio": 5000000, "imagen": "lh50.jpeg"},
    {"nombre": "MAC", "precio": 5000000, "imagen": "mac.jpeg"},
    {"nombre": "Nintendo Switch", "precio": 5000000, "imagen": "nintendoswitch.jpeg"},
    {"nombre": "PlayStation 4", "precio": 5000000, "imagen": "playstation4.jpeg"},
    {"nombre": "PlayStation 5", "precio": 5000000, "imagen": "playstation5.jpeg"},
    {"nombre": "Poco X6 Pro", "precio": 5000000, "imagen": "pocox6pro.jpeg"},
    {"nombre": "Redmi Note 13 Pro", "precio": 5000000, "imagen": "redmi13pro.jpeg"},
    {"nombre": "Televisor Samsung 50", "precio": 5000000, "imagen": "samsung50.jpeg"},
    {"nombre": "Xbox One", "precio": 5000000, "imagen": "xboxone.jpeg"},
    {"nombre": "Xbox Series X", "precio": 5000000, "imagen": "xboxseriesx.jpeg"}
]

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
@login_required
def signout(request):
    logout(request)  # Cierra la sesión del usuario actual
    return redirect('home')  # Redirige a la página de inicio

# Función para mostrar la página de tareas
@login_required
def tasks(request):
    tasks = task.objects.filter(user=request.user, date_completed__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completadas(request):
    tasks = task.objects.filter(user=request.user, date_completed__isnull = False).order_by('-date_completed')
    return render(request, 'tasks.html', {'tasks': tasks})


# Función para gestionar la creación de nuevas tareas
@login_required
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

@login_required
def tasks_detalles(request, task_id):
    if request.method == 'GET':
        Task = get_object_or_404(task, pk=task_id, user=request.user)
        form = taskform(instance=Task)
        return render(request, 'tasks_detalles.html', {'Task': Task, 'form': form})
    else:
        try:
            Task =get_object_or_404(task, pk=task_id, user=request.user)
            form = taskform(request.POST, instance=Task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detalles.html', {'Task': Task, 'form': form, 'error': 'error al acualizar los datos'})
    
@login_required
def tasks_completar(request, task_id):
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == 'POST':
        Task.date_completed = timezone.now()
        Task.save()
        return redirect('tasks')    

@login_required
def delete_tasks(request, task_id):
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    if request.method == 'POST':
        Task.delete()
        return redirect('tasks')

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

@login_required
def propinas(request):
    return render(request, 'propinas.html')

@login_required
def cuotas(request):
    return render(request, 'cuotas.html')

@login_required
def compras(request):
    presupuesto = request.POST.get('presupuesto')
    if presupuesto:
        presupuesto = int(presupuesto)
        productos_filtrados = [p for p in productos if p['precio'] <= presupuesto]
    else:
        productos_filtrados = productos

    return render(request, 'compras_con_presupuesto.html', {'productos':productos_filtrados, 'presupuesto':presupuesto})

def plot_view(request):
    if 'y_values' not in request.session:
        request.session['y_values'] = []

    y = request.session['y_values']

    if request.method == 'POST':
        form = ValueForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            y.append(value)
            request.session['y_values'] = y
    else:
        form = ValueForm()

    x = list(range(1, len(y) + 1))

    # Create the plot
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Gráfica de Líneas')

    # Save the plot to a string in base64 format
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()  # Asegurarse de que la cadena esté decodificada
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    buf.close()

    return render(request, 'plot.html', {'form': form, 'plot_uri': uri})