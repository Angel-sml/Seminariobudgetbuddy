from django.db import models
from django.contrib.auth.models import User

# Modelo para representar una tarea
class task(models.Model):
    title = models.CharField(max_length=100)  # Campo para el título de la tarea
    description = models.TextField(blank=True)  # Campo opcional para la descripción de la tarea
    date_created = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la tarea (autoañadida)
    date_completed = models.DateTimeField(null=True, blank=True)  # Fecha de completado de la tarea (opcional)
    important = models.BooleanField(default=False)  # Indica si la tarea es importante o no
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que creó la tarea

    # Método para representar la tarea como una cadena
    def __str__(self):
        return f"{self.title} de: {self.user.username}"  # Devuelve el título de la tarea y el nombre de usuario
