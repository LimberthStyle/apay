from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, DealerForm, DetallePedidoForm, PedidoForm, ProductoForm, UserRegisterForm, UsuarioForm, DetallePedidoFormSet
from .models import Cliente, Dealer, Pedido, Producto, usuario, DetallePedido
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def get_producto_details(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        data = {
            'precio': str(producto.precio),  # Precio del producto
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
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
           return render(request, 'logear/login.html', {'error': 'Usuario o contraseña incorrectos'})
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
#------------------------PEDIDOS------------------------------------------------------------------------
# Listar pedidos
class ListarPedidos(ListView):
    model = Pedido
    template_name = 'orders/listar_pedidos.html'
    context_object_name = 'pedidos'

# Crear un pedido
class CrearPedido(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'orders/crear_pedido.html'
    success_url = reverse_lazy('listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_formset'] = DetallePedidoFormSet(self.request.POST)
        else:
            context['detalle_formset'] = DetallePedidoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        if detalle_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.costo_total = 5.00  # Iniciar con el costo de delivery
            self.object.save()

            # Calcular el costo total de los productos
            for detalle_form in detalle_formset:
                detalle = detalle_form.save(commit=False)
                detalle.pedido = self.object

                # Si `precio_unitario` está vacío, asignar un valor predeterminado
                if detalle.precio_unitario is None:
                    detalle.precio_unitario = 0.00  

                detalle.save()
                self.object.costo_total += detalle.cantidad * detalle.precio_unitario

            self.object.save()

            # Cambiar el estado del repartidor a "OCUPADO"
            if self.object.dealer:
                self.object.dealer.estado = 'OCUPADO'
                self.object.dealer.save()

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))
    

# Actualizar un pedido
class ActualizarPedido(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'orders/actualizar_pedido.html'
    success_url = reverse_lazy('listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_formset'] = DetallePedidoForm(self.request.POST, instance=self.object)
        else:
            context['detalle_formset'] = DetallePedidoForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if detalle_formset.is_valid():
            self.object = form.save()
            detalle_formset.instance = self.object
            detalle_formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Eliminar un pedido
class EliminarPedido(DeleteView):
    model = Pedido
    template_name = 'orders/eliminar_pedido.html'
    success_url = reverse_lazy('listar_pedidos')
#CLIENTES-------------------------------------------------------------------------------------------------------------------------
# Listar clientes
class ListarClientes(ListView):
    model = Cliente
    template_name = 'customers/listar_clientes.html'
    context_object_name = 'clientes'

# Crear un cliente
class CrearCliente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'customers/crear_cliente.html'
    success_url = reverse_lazy('listar_clientes')

# Actualizar un cliente
class ActualizarCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'customers/actualizar_cliente.html'
    success_url = reverse_lazy('listar_clientes')

# Eliminar un cliente
class EliminarCliente(DeleteView):
    model = Cliente
    template_name = 'customers/eliminar_cliente.html'
    success_url = reverse_lazy('listar_clientes')
#PRODUCTOS-------------------------------------------------------------------------------------------------------------------------
# Listar productos
class ListarProductos(ListView):
    model = Producto
    template_name = 'products/listar_productos.html'
    context_object_name = 'productos'

# Crear un producto
class CrearProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'products/crear_producto.html'
    success_url = reverse_lazy('listar_productos')

# Actualizar un producto
class ActualizarProducto(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'products/actualizar_producto.html'
    success_url = reverse_lazy('listar_productos')

# Eliminar un producto
class EliminarProducto(DeleteView):
    model = Producto
    template_name = 'products/eliminar_producto.html'
    success_url = reverse_lazy('listar_productos')