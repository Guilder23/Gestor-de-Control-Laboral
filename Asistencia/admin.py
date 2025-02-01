from django.contrib import admin

# PARA QUE APAREZCAN LAS TABLAS EN EL ADMIN DE DAJNGO TU LO HIICSTE GUILDER

from django.contrib import admin
from .models import Usuario, RegistroAsistencia

# Registrar el modelo Usuario para que aparezca en el admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'apellidos', 'genero', 'cargo', 'correo_electronico', 'numero_carnet', 'celular', 'foto_perfil')
    search_fields = ('username', 'apellidos', 'correo_electronico')
    list_filter = ('genero', 'cargo')

# Registrar el modelo RegistroAsistencia para que aparezca en el admin

from django.contrib import admin
from .models import RegistroAsistencia

@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'hora_entrada', 'hora_salida', 'tiempo_transcurrido', 'descripcion')
    list_filter = ('usuario', 'hora_entrada', 'hora_salida')
    search_fields = ('usuario__username', 'descripcion')
    readonly_fields = ('tiempo_transcurrido',)

    def tiempo_transcurrido(self, obj):
        return obj.tiempo_transcurrido()
    tiempo_transcurrido.short_description = "Tiempo Transcurrido"
