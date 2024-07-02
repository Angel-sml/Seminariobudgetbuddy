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
from sitioweb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks-completadas', views.tasks_completadas, name='tasks_completadas'),
    path('tasks/create/', views.create_tasks, name='create_task'),
    path('tasks/<int:task_id>/', views.tasks_detalles, name='detalles_task'),
    path('tasks/<int:task_id>/completar', views.tasks_completar, name='completar_task'),
    path('tasks/<int:task_id>/Eliminar', views.delete_tasks, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('propinas/', views.propinas, name="propinas"),
    path('cuotas/', views.cuotas, name="cuotas"),
    path('compras/', views.compras, name="compras"),
    path('graficas/', views.plot_view, name="graficas"),
    path('prestamos/', views.prestamos, name="prestamos"),
    path('verprestamos/', views.ver_prestamos, name="verprestamos")
]
