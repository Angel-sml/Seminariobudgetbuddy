from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, models
from .forms import taskform, ValueForm
from .models import task
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse


from django.db import models
from django.contrib.auth.models import User

class Prestamo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación muchos a uno con el modelo User
    nombre = models.CharField(max_length=255)  # Nombre del préstamo
    fecha = models.DateField()  # Fecha del préstamo
    fecha2 = models.DateField()  # Fecha límite o máxima del préstamo
    monto = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del préstamo, decimal con 10 dígitos en total y 2 decimales
    
    def __str__(self):
        return f'{self.nombre} - {self.monto}'  # Representación en cadena del objeto, mostrando nombre y monto

    

# Lista de productos (ejemplo) (diccionario)
productos = [
    {"nombre": "iPad 10", "precio": 2500000, "imagen": "ipad10.jpeg"},
    {"nombre": "iPhone 13", "precio": 3200000, "imagen": "iphone13.jpeg"},
    {"nombre": "iPhone 14", "precio": 4200000, "imagen": "iphone14.jpeg"},
    {"nombre": "iPhone 15", "precio": 5200000, "imagen": "iphone15.jpeg"},
    {"nombre": "Laptop Asus", "precio": 3500000, "imagen": "lapasus.jpeg"},
    {"nombre": "Laptop HP", "precio": 3300000, "imagen": "laphp.jpeg"},
    {"nombre": "Laptop Lenovo", "precio": 3400000, "imagen": "laplenovo.jpeg"},
    {"nombre": "Televisor LG 50", "precio": 2700000, "imagen": "lh50.jpeg"},
    {"nombre": "MAC", "precio": 8000000, "imagen": "mac.jpeg"},
    {"nombre": "Nintendo Switch", "precio": 1600000, "imagen": "nintendoswitch.jpeg"},
    {"nombre": "PlayStation 4", "precio": 1200000, "imagen": "playstation4.jpeg"},
    {"nombre": "PlayStation 5", "precio": 2800000, "imagen": "playstation5.jpeg"},
    {"nombre": "Poco X6 Pro", "precio": 1500000, "imagen": "pocox6pro.jpeg"},
    {"nombre": "Redmi Note 13 Pro", "precio": 1400000, "imagen": "redmi13pro.jpeg"},
    {"nombre": "Televisor Samsung 50", "precio": 2900000, "imagen": "samsung50.jpeg"},
    {"nombre": "Xbox One", "precio": 1300000, "imagen": "xboxone.jpeg"},
    {"nombre": "Xbox Series X", "precio": 2500000, "imagen": "xboxseriesx.jpeg"}
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

# Este decorador asegura que el usuario esté autenticado para acceder a la vista
@login_required
def tasks_completadas(request):
    # Filtra las tareas del usuario actual que ya han sido completadas (date_completed no es nulo)
    tasks = task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    
    # Renderiza la plantilla 'tasks.html' y pasa las tareas completadas como contexto
    return render(request, 'tasks.html', {'tasks': tasks})



# Función para gestionar la creación de nuevas tareas
@login_required
def create_tasks(request):
    # Si el método de la solicitud es GET, se muestra el formulario para crear una nueva tarea
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form': taskform  # Pasa el formulario vacío como contexto
        })
    else:
        try:
            # Obtiene los datos del formulario enviados a través de una solicitud POST
            form = taskform(request.POST)
            # Crea una nueva tarea con los datos del formulario, pero no la guarda aún en la base de datos
            new_task = form.save(commit=False)
            # Asigna el usuario actual a la nueva tarea
            new_task.user = request.user
            # Guarda la nueva tarea en la base de datos
            new_task.save()
            # Redirige a la página de tareas
            return redirect('tasks')
        except ValueError:
            # Si hay un error en los datos del formulario, muestra el formulario con un mensaje de error
            return render(request, 'create_tasks.html', {
                'form': taskform,  # Pasa el formulario con los datos ingresados
                'error': 'datos incorrectos'  # Pasa el mensaje de error como contexto
            })


# Este decorador asegura que el usuario esté autenticado para acceder a la vista
@login_required
def tasks_detalles(request, task_id):
    # Si el método de la solicitud es GET, se muestran los detalles de la tarea y el formulario
    if request.method == 'GET':
        # Obtiene la tarea especificada por task_id y perteneciente al usuario actual, o devuelve un 404 si no existe
        Task = get_object_or_404(task, pk=task_id, user=request.user)
        # Crea un formulario con la instancia de la tarea obtenida
        form = taskform(instance=Task)
        # Renderiza la plantilla 'tasks_detalles.html' pasando la tarea y el formulario como contexto
        return render(request, 'tasks_detalles.html', {'Task': Task, 'form': form})
    else:
        try:
            # Obtiene nuevamente la tarea especificada por task_id y perteneciente al usuario actual
            Task = get_object_or_404(task, pk=task_id, user=request.user)
            # Crea un formulario con los datos POST enviados y la instancia de la tarea
            form = taskform(request.POST, instance=Task)
            # Guarda los cambios realizados en el formulario
            form.save()
            # Redirige a la vista de tareas
            return redirect('tasks')
        except ValueError:
            # Si ocurre un error durante la actualización de los datos, renderiza la plantilla con un mensaje de error
            return render(request, 'tasks_detalles.html', {'Task': Task, 'form': form, 'error': 'error al actualizar los datos'})

    
# Este decorador asegura que el usuario esté autenticado para acceder a la vista
@login_required
# funcion para marcar como completada una task
def tasks_completar(request, task_id):
    # Obtiene la tarea especificada por task_id y perteneciente al usuario actual, o devuelve un 404 si no existe
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    
    # Si el método de la solicitud es POST, se marca la tarea como completada
    if request.method == 'POST':
        # Establece la fecha de finalización de la tarea a la hora actual
        Task.date_completed = timezone.now()
        # Guarda los cambios realizados en la tarea
        Task.save()
        # Redirige a la vista de tareas
        return redirect('tasks')
  

# Función para gestionar la eliminación de tareas
@login_required
def delete_tasks(request, task_id):
    # Obtiene la tarea especificada por task_id y perteneciente al usuario actual, o devuelve un 404 si no existe
    Task = get_object_or_404(task, pk=task_id, user=request.user)
    
    # Si el método de la solicitud es POST, se procede a eliminar la tarea
    if request.method == 'POST':
        # Elimina la tarea de la base de datos
        Task.delete()
        # Redirige a la página de tareas
        return redirect('tasks')


# Función para gestionar el inicio de sesión
def signin(request):
    # Si el método de la solicitud es GET, muestra el formulario de inicio de sesión
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm  # Pasa el formulario de autenticación como contexto
        })
    else:
        # Autentica al usuario con el nombre de usuario y la contraseña proporcionados
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        # Si la autenticación falla, muestra un mensaje de error junto con el formulario de inicio de sesión
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,  # Pasa el formulario de autenticación con los datos ingresados
                'error': 'Username or password is incorrect'  # Mensaje de error para mostrar al usuario
            })
        else:
            login(request, user)  # Inicia sesión con el usuario autenticado
            return redirect('home')  # Redirige a la página de inicio del usuario (puede ser 'home' o cualquier otra ruta)


@login_required
def propinas(request):
    return render(request, 'propinas.html')

@login_required
def cuotas(request):
    return render(request, 'cuotas.html')

# Vista protegida que requiere que el usuario esté autenticado para acceder
@login_required
# funcion de presupuesto de compra
def compras(request):
    presupuesto = request.POST.get('presupuesto')  # Obtiene el presupuesto enviado por POST
    if presupuesto:
        presupuesto = int(presupuesto)  # Convierte el presupuesto a entero si existe
        # Filtra los productos según el presupuesto dado
        productos_filtrados = [p for p in productos if p['precio'] <= presupuesto]
    else:
        productos_filtrados = productos  # Si no hay presupuesto dado, muestra todos los productos

    # Renderiza la plantilla 'compras_con_presupuesto.html' con los productos filtrados y el presupuesto
    return render(request, 'compras_con_presupuesto.html', {
        'productos': productos_filtrados,
        'presupuesto': presupuesto
    })


def plot_view(request):
    # Verifica si 'y_values' no está en la sesión, y si no está, lo inicializa como una lista vacía
    if 'y_values' not in request.session:
        request.session['y_values'] = []

    y = request.session['y_values']  # Obtiene la lista de valores 'y' desde la sesión

    if request.method == 'POST':
        form = ValueForm(request.POST)  # Crea un formulario con los datos de la solicitud POST
        if form.is_valid():
            value = form.cleaned_data['value']  # Obtiene el valor limpio del formulario
            y.append(value)  # Añade el valor a la lista 'y'
            request.session['y_values'] = y  # Actualiza la lista 'y' en la sesión
    else:
        form = ValueForm()  # Crea un formulario vacío si la solicitud no es POST

    x = list(range(1, len(y) + 1))  # Genera una lista de valores de 'x' basada en la longitud de 'y'

    # Crear el gráfico
    plt.figure()
    plt.plot(x, y, marker='o')  # Crea un gráfico de líneas con marcadores en los puntos
    plt.xlabel('X')  # Etiqueta del eje X
    plt.ylabel('Y')  # Etiqueta del eje Y
    plt.title('Gráfica de Líneas')  # Título del gráfico

    # Guardar el gráfico en formato PNG y convertirlo a una cadena base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()  # Codifica la imagen en base64
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)  # Crea el URI de la imagen
    buf.close()

    # Renderiza la plantilla 'plot.html' con el formulario y el URI del gráfico
    return render(request, 'plot.html', {'form': form, 'plot_uri': uri})



@login_required
def prestamos(request):
    return render(request, 'prestamos.html')

@login_required
def ver_prestamos(request):
    # Si la solicitud es POST, se intenta crear un nuevo préstamo con los datos enviados
    if request.method == 'POST':
        nombre = request.POST.get('nombre')  # Obtiene el nombre del préstamo desde la solicitud POST
        fecha = request.POST.get('fecha')    # Obtiene la fecha de inicio del préstamo desde la solicitud POST
        fecha2 = request.POST.get('fecha2')  # Obtiene la fecha de finalización del préstamo desde la solicitud POST
        monto = request.POST.get('monto')    # Obtiene el monto del préstamo desde la solicitud POST
        
        # Crea un nuevo objeto de préstamo en la base de datos asociado al usuario actual
        Prestamo.objects.create(
            user=request.user,  # Asigna el usuario actual al préstamo
            nombre=nombre,      # Asigna el nombre del préstamo
            fecha=fecha,        # Asigna la fecha de inicio del préstamo
            fecha2=fecha2,      # Asigna la fecha de finalización del préstamo
            monto=monto         # Asigna el monto del préstamo
        )

    # Obtiene todos los préstamos del usuario actual desde la base de datos
    prestamos = Prestamo.objects.filter(user=request.user)
    
    # Renderiza la plantilla 'visualizacion_prestamos.html' con la lista de préstamos obtenida
    return render(request, 'visualizacion_prestamos.html', {'prestamos': prestamos})
