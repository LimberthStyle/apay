from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import usuario, Dealer

# Formulario para el modelo User (registro de usuario)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Agregar campo de correo electrónico

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Formulario para el modelo usuario (extensión del User)
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = usuario
        fields = ['psw']  # Solo el campo adicional

#Registrar dealer
class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['dni', 'nombres', 'apellidos', 'placa', 'estado', 'fotocheck']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fotocheck': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }