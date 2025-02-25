from django.urls import path
from django.shortcuts import redirect
from . import views

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirige a dashboard si el usuario está autenticado
    else:
        return redirect('login')  # Redirige a login si el usuario no está autenticado

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL de inicio de sesión
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),  # URL del panel de control
    path('', root_redirect),  # Redirige la URL raíz según el estado de autenticación
    path('logout/', views.logout_view, name='logout'),  # URL para cerrar sesión
    #DEALERS-----------------------------------------------------------------------------------------
    path('dealers/', views.listar_dealers, name='listar_dealers'),
    path('dealers/registrar/', views.registrar_dealer, name='registrar_dealer'),
    path('dealers/editar/<int:id>/', views.editar_dealer, name='editar_dealer'),
    path('dealers/eliminar/<int:id>/', views.eliminar_dealer, name='eliminar_dealer'),
    #PEDIDOS------------------------------------------------------------------------------------------
    path('pedidos/', views.ListarPedidos.as_view(), name='listar_pedidos'),
    path('pedidos/crear/', views.CrearPedido.as_view(), name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', views.ActualizarPedido.as_view(), name='actualizar_pedido'),
    path('pedidos/eliminar/<int:pk>/', views.EliminarPedido.as_view(), name='eliminar_pedido'),
    # URLs para clientes
    path('clientes/', views.ListarClientes.as_view(), name='listar_clientes'),
    path('clientes/crear/', views.CrearCliente.as_view(), name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.ActualizarCliente.as_view(), name='actualizar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.EliminarCliente.as_view(), name='eliminar_cliente'),
    # URLs para productos
    path('productos/', views.ListarProductos.as_view(), name='listar_productos'),
    path('productos/crear/', views.CrearProducto.as_view(), name='crear_producto'),
    path('productos/editar/<int:pk>/', views.ActualizarProducto.as_view(), name='actualizar_producto'),
    path('productos/eliminar/<int:pk>/', views.EliminarProducto.as_view(), name='eliminar_producto'),
    path('get-producto-details/<int:producto_id>/', views.get_producto_details, name='get_producto_details'),
]
