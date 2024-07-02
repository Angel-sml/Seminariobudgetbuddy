"""
URL configuration for BBseminario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from sitioweb import views  # Importa las vistas desde el módulo sitioweb

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para la interfaz de administración de Django
    path('', views.home, name='home'),  # Ruta para la página de inicio, usando la vista 'home'
    path('signup/', views.signup, name='signup'),  # Ruta para registrarse, usando la vista 'signup'
    path('tasks/', views.tasks, name='tasks'),  # Ruta para las tareas, usando la vista 'tasks'
    path('tasks-completadas', views.tasks_completadas, name='tasks_completadas'),  # Ruta para las tareas completadas
    path('tasks/create/', views.create_tasks, name='create_task'),  # Ruta para crear una nueva tarea
    path('tasks/<int:task_id>/', views.tasks_detalles, name='detalles_task'),  # Ruta para ver detalles de una tarea específica
    path('tasks/<int:task_id>/completar', views.tasks_completar, name='completar_task'),  # Ruta para marcar una tarea como completada
    path('tasks/<int:task_id>/Eliminar', views.delete_tasks, name='delete_task'),  # Ruta para eliminar una tarea
    path('logout/', views.signout, name='logout'),  # Ruta para cerrar sesión, usando la vista 'signout'
    path('signin/', views.signin, name='signin'),  # Ruta para iniciar sesión, usando la vista 'signin'
    path('propinas/', views.propinas, name="propinas"),  # Ruta para la calculadora de propinas
    path('cuotas/', views.cuotas, name="cuotas"),  # Ruta para la calculadora de cuotas
    path('compras/', views.compras, name="compras"),  # Ruta para la página de compras
    path('graficas/', views.plot_view, name="graficas"),  # Ruta para la visualización de gráficas
    path('prestamos/', views.prestamos, name="prestamos"),  # Ruta para la gestión de préstamos
    path('verprestamos/', views.ver_prestamos, name="verprestamos"),  # Ruta para ver los préstamos
]
