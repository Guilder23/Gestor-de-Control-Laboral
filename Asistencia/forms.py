from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

# Formulario de registro
class RegistroForm(UserCreationForm):
    apellidos = forms.CharField(max_length=255)
    genero = forms.ChoiceField(choices=Usuario.GENDER_CHOICES)
    cargo = forms.ChoiceField(choices=Usuario.cargo_choices)
    correo_electronico = forms.EmailField()
    numero_carnet = forms.CharField(max_length=20)
    celular = forms.CharField(max_length=15)
    
    class Meta:
        model = Usuario
        fields = ['username', 'apellidos', 'genero', 'cargo', 'correo_electronico', 'numero_carnet', 'celular', 'foto_perfil', 'password1', 'password2']

# Formulario de login
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
#formulario de salida y entrada


from django import forms
from .models import RegistroAsistencia
from django import forms
from .models import RegistroAsistencia

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ['usuario', 'hora_entrada', 'hora_salida', 'descripcion']

