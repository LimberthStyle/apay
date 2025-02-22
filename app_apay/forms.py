from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import usuario

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