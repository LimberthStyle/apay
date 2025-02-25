from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, DetallePedido, Pedido, Producto, usuario, Dealer
from django.forms import inlineformset_factory

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

#GESTION DE PEDIDOS----------------------------------

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['metodo_pago', 'cliente', 'dealer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo los dealers disponibles
        self.fields['dealer'].queryset = Dealer.objects.filter(estado='DISPONIBLE')


# Formulario para DetallePedido
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].widget.attrs['disabled'] = True  # Usar 'disabled' en lugar de 'readonly'
        self.fields['precio_unitario'].required = False  # No es obligatorio (se llenará automáticamente)
# FormSet para DetallePedido
DetallePedidoFormSet = inlineformset_factory(
    Pedido,  # Modelo principal
    DetallePedido,  # Modelo relacionado
    form=DetallePedidoForm,  # Formulario personalizado
    extra=1,  # Número de formularios vacíos que se mostrarán
)
#CLIENTES-----------------------------------------------------------------

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'domicilio', 'correo', 'telefono']
#PRODUCTOS-----------------------------------------------------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nom_produc', 'descripcion', 'cantidad', 'precio']