
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    cargo_choices = [
        ('B', 'Becado'),
        ('P', 'Promotor'),
        ('JZ', 'Jefe de Zona'),
    ]
    
    apellidos = models.CharField(max_length=255)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cargo = models.CharField(max_length=2, choices=cargo_choices)
    correo_electronico = models.EmailField(unique=True)
    numero_carnet = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=15)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)  # Campo para la foto
    
    def __str__(self):
        return self.username

#ASISTENCIA DE ENTRADA Y SALIDA
from django.db import models
from django.utils import timezone
from .models import Usuario  # Importamos el modelo de usuario

class RegistroAsistencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    def tiempo_transcurrido(self):
        if self.hora_entrada and not self.hora_salida:
            return timezone.now() - self.hora_entrada
        elif self.hora_entrada and self.hora_salida:
            return self.hora_salida - self.hora_entrada
        return None

    def __str__(self):
        return f"{self.usuario.username} - {self.hora_entrada} / {self.hora_salida}"
