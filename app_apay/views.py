from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import DealerForm, UserRegisterForm, UsuarioForm
from .models import Dealer, usuario

# Vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if user_form.is_valid() and usuario_form.is_valid():
            # Guardar el usuario
            user = user_form.save()
            # Crear el perfil de usuario (usuario)
            profile = usuario_form.save(commit=False)
            profile.user = user  # Asignar el usuario al perfil
            profile.save()

            # Iniciar sesión automáticamente después del registro
            auth_login(request, user)
            return redirect('dashboard')  # Redirigir al panel de control
    else:
        user_form = UserRegisterForm()
        usuario_form = UsuarioForm()

    return render(request, 'logear/register.html', {
        'user_form': user_form,
        'usuario_form': usuario_form,
    })

# Vista de inicio de sesión (ya la tienes, pero la ajustamos)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'logear/login.html')

# Vista del panel de control (ya la tienes)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')
#----------DEALERS---------------------------
# Listar Dealers
def listar_dealers(request):
    dealers = Dealer.objects.all()
    return render(request, 'dealers/listar_dealers.html', {'dealers': dealers})

# Registrar un nuevo Dealer
def registrar_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_dealers')
    else:
        form = DealerForm()
    return render(request, 'dealers/registrar_dealer.html', {'form': form})

# Editar un Dealer existente
def editar_dealer(request, id):
    dealer = get_object_or_404(Dealer, id=id)
    if request.method == 'POST':
        form = DealerForm(request.POST, request.FILES, instance=dealer)
        if form.is_valid():
            form.save()
            return redirect('listar_dealers')
    else:
        form = DealerForm(instance=dealer)
    return render(request, 'dealers/editar_dealer.html', {'form': form})

# Eliminar un Dealer
def eliminar_dealer(request, id):
    dealer = get_object_or_404(Dealer, id=id)
    if request.method == 'POST':
        dealer.delete()
        return redirect('listar_dealers')
    return render(request, 'dealers/confirmar_eliminar_dealer.html', {'dealer': dealer})