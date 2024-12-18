from django import forms
from django.forms import ValidationError
from .models import Cargo, Afp, Sistema_de_salud
import re
import datetime

class RegistrarActualizarTrabajadorForm(forms.Form):
    SEXO_CHOICES = [
        ('Masculino', "Masculino"),
        ("Femenino", "Femenino")
    ]
    Nombre = forms.CharField(max_length=50)
    Apellido = forms.CharField(max_length=50)
    Rut = forms.CharField(max_length=12, required=True, help_text="Formato: 12345678-K", widget=forms.TextInput(attrs={'placeholder': '12345678-K'}))
    Sexo = forms.ChoiceField(choices=SEXO_CHOICES)
    Correo = forms.EmailField(max_length=100, required=True, help_text="Formato: ejemplo@ejemplo.com", widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@ejemplo.com'}))
    Contraseña = forms.CharField(max_length=12, required=True)
    Cargo = forms.ChoiceField()
    Telefono = forms.CharField(max_length=9)
    Fecha_de_Ingreso = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    def clean_Fecha_de_Ingreso(self):
        if self.Fecha_de_Ingreso < datetime.now():
            raise ValidationError('La fecha de ingreso no puede ser menor a la fecha actual')
    Direccion = forms.CharField()
    Imagen = forms.ImageField()
    Salario = forms.IntegerField()
    Afp = forms.ChoiceField()
    Sistema_de_salud = forms.ChoiceField()
    
    def clean_Rut(self):
        """Valida que el RUT chileno tenga el formato correcto."""
        if not re.match(r'^\d{7,8}-[0-9Kk]$', self.Rut):
            raise ValidationError('El RUT debe tener el formato 12345678-K')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields['Cargo'].choices)
        if len(self.fields['Cargo'].choices) == 0:
            self.fields['Cargo'].choices= Cargo.objects.all().values_list('id', 'Nombre')

        if len(self.fields['Afp'].choices) == 0:
            self.fields['Afp'].choices= Afp.objects.all().values_list('id', 'Nombre')

        if len(self.fields['Sistema_de_salud'].choices) == 0:
            self.fields['Sistema_de_salud'].choices= Sistema_de_salud.objects.all().values_list('id', 'Nombre')

class CrearPermisoForm(forms.Form):
    Fecha_de_inicio = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Cantidad_de_dias = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=6
    )
    Motivo = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={'rows': 4})
    )
    def clean_Fecha_de_inicio(self):
        fecha_inicio = self.cleaned_data['Fecha_de_inicio']
        if fecha_inicio < datetime.datetime.now().date():
            raise ValidationError('La fecha de inicio no puede ser menor a la fecha actual')
        return fecha_inicio
    
class LoginForm(forms.Form):
    Rut = forms.CharField(
        label='RUT',
        max_length=12,
        help_text="Formato: 12345678-K",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-K'
        })
    )
    Contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'})
    )

    def clean_Rut(self):
        rut = self.cleaned_data['Rut']
        if not re.match(r'^\d{7,8}-[0-9Kk]$', rut):
            raise ValidationError('El RUT debe tener el formato 12345678-K')
        return rut.upper()
