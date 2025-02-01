from django.urls import path
from . import views

from .views import registrar_entrada, registrar_salida

from .views import listar_usuarios

from .views import generar_reporte_pdf


urlpatterns = [
    path('', views.home, name='home'),  # Define la vista principal
    path('registro/', views.registrar, name='registro'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    path("entrada/", registrar_entrada, name="registrar_entrada"),
    path("salida/", registrar_salida, name="registrar_salida"),
    

    path('usuarios/', listar_usuarios, name='usuarios'),

    path('reporte_asistencia/', generar_reporte_pdf, name='reporte_asistencia'),

    path('reporte_asistencia_excel/', views.generar_reporte_excel, name='reporte_asistencia_excel'),
    
    path('reporte_asistencia_pdf/', views.generar_reporte_pdf, name='reporte_asistencia_pdf'),

]

