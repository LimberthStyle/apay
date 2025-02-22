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
]
