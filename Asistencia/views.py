from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm
from .models import Usuario

from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages
#Home------------------------------------
# Asistencia/views.py
from django.shortcuts import render


# Vista de registro
def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)  # Importante para manejar imágenes
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('perfil')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista de perfil
@login_required(login_url='/login/')
def perfil(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.apellidos = request.POST.get('apellidos')
        usuario.genero = request.POST.get('genero')
        usuario.cargo = request.POST.get('cargo')
        usuario.correo_electronico = request.POST.get('correo_electronico')
        usuario.numero_carnet = request.POST.get('numero_carnet')
        usuario.celular = request.POST.get('celular')
        usuario.save()
    return render(request, 'perfil.html', {'usuario': request.user})


def cerrar_sesion(request):
    logout(request)
    return redirect('home')  # Redirige a la página de inicio de sesión
#ENTRADA Y SALIDA
from django.http import JsonResponse
from django.shortcuts import render
from .models import RegistroAsistencia
from django.utils.timezone import now  # Importa el helper de fecha/hora de Django


def home(request):
    entradas = RegistroAsistencia.objects.filter(hora_salida__isnull=True)
    salidas = RegistroAsistencia.objects.filter(hora_salida__isnull=False).order_by("-hora_salida")[:10]
    return render(request, "home.html", {"entradas": entradas, "salidas": salidas})



#nuevo registro de entradas y salidas 30 enero 2025
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Usuario, RegistroAsistencia

def registrar_entrada(request):
    if request.method == "POST":
        numero_carnet = request.POST.get("numero_carnet")

        try:
            usuario = Usuario.objects.get(numero_carnet=numero_carnet)
            ultimo_registro = RegistroAsistencia.objects.filter(usuario=usuario).order_by("-hora_entrada").first()

            # Verificar si el usuario ya tiene una entrada activa sin salida
            if ultimo_registro and not ultimo_registro.hora_salida:
                messages.error(request, "Ya tienes una entrada activa, primero registra tu salida.")
            else:
                # Registrar nueva entrada
                RegistroAsistencia.objects.create(usuario=usuario, hora_entrada=timezone.now())
                messages.success(request, "Entrada registrada exitosamente.")

        except Usuario.DoesNotExist:
            messages.error(request, "Número de carnet no registrado.")

    return redirect("home")

def registrar_salida(request):
    if request.method == "POST":
        numero_carnet = request.POST.get("numero_carnet")
        descripcion = request.POST.get("descripcion", "")

        try:
            usuario = Usuario.objects.get(numero_carnet=numero_carnet)
            ultimo_registro = RegistroAsistencia.objects.filter(usuario=usuario, hora_salida__isnull=True).order_by("-hora_entrada").first()

            if not ultimo_registro:
                messages.error(request, "No tienes una entrada activa registrada.")
            else:
                # Registrar salida
                ultimo_registro.hora_salida = timezone.now()
                ultimo_registro.descripcion = descripcion
                ultimo_registro.save()
                messages.success(request, "Salida registrada exitosamente.")

        except Usuario.DoesNotExist:
            messages.error(request, "Número de carnet no registrado.")

    return redirect("home")


#Listar todos los usuarios registrados eb la BD
from django.shortcuts import render
from django.contrib.auth.models import User

def listar_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios registrados
    return render(request, 'usuarios.html', {'usuarios': usuarios})

#GENERARA REPORTEfrom django.http import HttpResponse---------------------------------------------------------
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import RegistroAsistencia
from django.http import HttpResponse


from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


from textwrap import wrap
from .models import RegistroAsistencia, Usuario
from django.utils.dateparse import parse_date
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from textwrap import wrap
from .models import RegistroAsistencia, Usuario

def generar_reporte_pdf(request):
    # Obtener los filtros de fecha de la solicitud (si existen)
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Convertir las fechas de string a objetos date si están presentes
    if fecha_inicio_str:
        fecha_inicio = parse_date(fecha_inicio_str)
    else:
        fecha_inicio = None

    if fecha_fin_str:
        fecha_fin = parse_date(fecha_fin_str)
    else:
        fecha_fin = None

    # Preparar la respuesta para el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_asistencia.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter  

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(180, height - 40, "Reporte de Asistencia")

    usuarios = RegistroAsistencia.objects.values('usuario').distinct()
    y = height - 80  
    total_general = 0  

    for usuario_data in usuarios:
        usuario = Usuario.objects.get(id=usuario_data['usuario'])
        
        # Filtrar registros por fecha de entrada si es que hay fechas proporcionadas
        registros = RegistroAsistencia.objects.filter(usuario=usuario)

        # Filtrar registros por fecha de entrada si el filtro de fechas está presente
        if fecha_inicio:
            registros = registros.filter(hora_entrada__gte=fecha_inicio)
        if fecha_fin:
            registros = registros.filter(hora_entrada__lte=fecha_fin)

        registros = registros.order_by('hora_entrada')

        total_horas_usuario = 0

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"Usuario: {usuario.username}")
        y -= 20

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, "Fecha")
        pdf.drawString(120, y, "Entrada")
        pdf.drawString(190, y, "Salida")
        pdf.drawString(230, y, "Descripción")
        pdf.drawString(500, y, "Horas")
        y -= 15

        pdf.setFont("Helvetica", 10)
        for registro in registros:
            fecha = registro.hora_entrada.strftime("%Y-%m-%d") if registro.hora_entrada else "N/A"
            hora_entrada = registro.hora_entrada.strftime("%H:%M") if registro.hora_entrada else "N/A"
            hora_salida = registro.hora_salida.strftime("%H:%M") if registro.hora_salida else "N/A"
            descripcion = registro.descripcion if registro.descripcion else "Sin descripción"

            if registro.hora_entrada and registro.hora_salida:
                horas_trabajadas = (registro.hora_salida - registro.hora_entrada).total_seconds() / 3600
                total_horas_usuario += horas_trabajadas
            else:
                horas_trabajadas = 0

            pdf.drawString(50, y, fecha)
            pdf.drawString(120, y, hora_entrada)
            pdf.drawString(190, y, hora_salida)
            pdf.drawString(500, y, f"{horas_trabajadas:.2f}")

            # Ajustar descripción en múltiples líneas si es necesario
            descripcion_lineas = wrap(descripcion, width=50)  
            for i, linea in enumerate(descripcion_lineas):
                if i == 0:
                    pdf.drawString(230, y, linea)
                else:
                    y -= 12
                    pdf.drawString(230, y, linea)
            
            y -= 15  

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, f"Total de horas de {usuario.username}:")
        pdf.drawString(500, y, f"{total_horas_usuario:.2f} horas")
        y -= 30

        total_general += total_horas_usuario

        if y < 100:
            pdf.showPage()
            y = height - 40
            pdf.setFont("Helvetica", 10)

    # Obtener la fecha de impresión
    fecha_impresion = datetime.now().strftime("%Y-%m-%d")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Total de horas trabajadas por todos los usuarios:")
    pdf.drawString(400, y, f"{total_general:.2f} horas")

    # Agregar la fecha de impresión en la parte inferior
    y -= 20
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Fecha de impresión: {fecha_impresion}")

    pdf.showPage()
    pdf.save()

    return response


#GENERAR EL EXCEL---------------------------------------------------------------------------------------------------
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from .models import RegistroAsistencia
from django.utils import timezone

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font
from .models import Usuario, RegistroAsistencia
from datetime import datetime

def generar_reporte_excel(request):
    # Crear una respuesta HTTP con contenido Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_asistencia.xlsx"'

    # Crear el libro de trabajo y la hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Asistencia"

    # Título del reporte
    ws.merge_cells('A1:D1')
    title_cell = ws.cell(row=1, column=1, value="Reporte de Asistencia")
    title_cell.font = Font(size=14, bold=True)

    # Encabezados de la tabla
    headers = ["Nombre", "Hora Entrada", "Hora Salida", "Horas Trabajadas"]
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=2, column=col_num, value=header).font = Font(size=12, bold=True)

    # Obtenemos los registros de asistencia
    usuarios = RegistroAsistencia.objects.values('usuario').distinct()  # Para obtener usuarios únicos
    row = 3  # Fila inicial para los datos

    # Loop sobre los usuarios
    for usuario_data in usuarios:
        usuario = Usuario.objects.get(id=usuario_data['usuario'])
        registros = RegistroAsistencia.objects.filter(usuario=usuario)
        
        total_horas_usuario_por_dia = 0  # Variable para totalizar las horas de cada usuario

        # Mostrar el nombre del usuario
        ws.cell(row=row, column=1, value=usuario.username)

        # Datos de los registros de asistencia del usuario
        for registro in registros:
            hora_entrada = registro.hora_entrada.strftime("%Y-%m-%d %H:%M:%S") if registro.hora_entrada else "N/A"
            hora_salida = registro.hora_salida.strftime("%Y-%m-%d %H:%M:%S") if registro.hora_salida else "N/A"
            
            if registro.hora_entrada and registro.hora_salida:
                horas_trabajadas = (registro.hora_salida - registro.hora_entrada).total_seconds() / 3600
                total_horas_usuario_por_dia += horas_trabajadas
            else:
                horas_trabajadas = 0

            ws.cell(row=row, column=2, value=hora_entrada)
            ws.cell(row=row, column=3, value=hora_salida)
            ws.cell(row=row, column=4, value=f"{horas_trabajadas:.2f}")
            row += 1
        
        # Mostrar el total de horas trabajadas por el usuario
        ws.cell(row=row, column=1, value=f"Total horas {usuario.username}:")
        ws.cell(row=row, column=4, value=f"{total_horas_usuario_por_dia:.2f} horas")
        row += 2  # Separar de la siguiente persona

    # Guardar el archivo Excel
    wb.save(response)
    
    return response
