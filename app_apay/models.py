from django.db import models
from django.contrib.auth.models import User

class usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psw = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username}'
    
# Modelo Dealer (Repartidor)
class Dealer(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADO', 'Ocupado'),
    ]

    dni = models.CharField(max_length=8, unique=True)  # DNI del repartidor
    nombres = models.CharField(max_length=100)  # Nombres del repartidor
    apellidos = models.CharField(max_length=100)  # Apellidos del repartidor
    placa = models.CharField(max_length=10, unique=True)  # Placa del vehículo
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='DISPONIBLE')  # Estado del repartidor
    fotocheck = models.ImageField(upload_to='fotochecks/')  # Foto del repartidor

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# Modelo Cliente
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=200)  # Nombre completo del cliente
    domicilio = models.CharField(max_length=200)  # Dirección de entrega
    correo = models.EmailField(unique=True)  # Correo electrónico del cliente
    telefono = models.CharField(max_length=15)  # Teléfono del cliente

    def __str__(self):
        return self.nombre_completo

# Modelo Producto
class Producto(models.Model):
    nom_produc = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField()  # Descripción del producto
    cantidad = models.PositiveIntegerField()  # Cantidad disponible
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto

    def __str__(self):
        return self.nom_produc

# Modelo Pedido
class Pedido(models.Model):
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('YAPE', 'Yape'),
        ('PLIN', 'Plin'),
    ]

    ESTADO_PEDIDO_CHOICES = [
        ('POR ENTREGAR', 'Por entregar'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    fecha_pedido = models.DateField(auto_now_add=True)  # Fecha del pedido (automática)
    hora = models.TimeField(auto_now_add=True)  # Hora del pedido (automática)
    metodo_pago = models.CharField(max_length=10, choices=METODO_PAGO_CHOICES)  # Método de pago
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)  # Costo total del pedido
    estado = models.CharField(max_length=12, choices=ESTADO_PEDIDO_CHOICES, default='POR ENTREGAR')  # Estado del pedido
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con el cliente
    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el repartidor
    productos = models.ManyToManyField(Producto, through='DetallePedido')  # Relación muchos a muchos con productos

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre_completo}"

# Modelo DetallePedido (para la relación muchos a muchos entre Pedido y Producto)
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Relación con el pedido
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.PositiveIntegerField()  # Cantidad del producto en el pedido
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nom_produc} en Pedido {self.pedido.id}"