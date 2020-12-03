from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.conf import settings


# User = get_user_model()
# MEDICOS = User.objects.filter(groups__name='Medicos')


# Create your models here.
class Paciente(models.Model):
    paciente_nombre = models.CharField(max_length=64)
    paciente_apellido = models.CharField(max_length=64)

    def get_absolute_url(self):
        return reverse('home_secre')    

    def __str__(self):
        return f"{self.pk}: {self.paciente_apellido}, {self.paciente_nombre}"


ASISTENCIA = [
    ('0', 'No'),
    ('1', 'Sí'),
    ('2', 'Pendiente'),
    ]

class Turno(models.Model):
    diahora = models.DateTimeField(verbose_name="Fecha y Hora")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="turnos_paciente")
    profesional = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="turnos_medicos")
    asistencia = models.CharField(max_length=9, choices=ASISTENCIA, default='2')

    def get_absolute_url(self):
        return reverse('home_secre')

    def __str__(self):
        return f"{self.pk} | {self.diahora} | {self.paciente} | {self.profesional}"

class Historia(models.Model):
    profesional = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="historias")
    diahora = models.DateTimeField(auto_now=True)
    observacion = models.TextField(blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_DEFAULT, default=0, related_name="historia")

    def __str__(self):
        return f"Paciente: {self.paciente} | Profesional: {self.profesional} | Observación: {self.observacion} | Fecha: {self.diahora}"    

CERCANIA = [
    ('LJ', 'Lejos'),
    ('CR', 'Cerca'),
    ]

LADO = [
    ('IZ', 'Izquierda'),
    ('DE', 'Derecha'),
    ]


class Product(models.Model):
    prod_category = models.TextField(null=True, blank=True)
    prod_title = models.CharField(max_length=220)
    prod_desc = models.TextField(null=True, blank=True) 
    prod_lente_cercania = models.TextField(choices=CERCANIA, null=True, blank=True)
    prod_lente_lado = models.TextField(choices=LADO, null=True, blank=True)
    prod_lente_armazon = models.BooleanField(null=True, blank=True)
    prod_price = models.IntegerField(default=0)

    def __str__(self):
        return f"Cat: {self.prod_category} | Nombre: {self.prod_title} | Cercania: {self.get_prod_lente_cercania_display()} | Lado: {self.get_prod_lente_lado_display()} | Armazon: {self.prod_lente_armazon} | Precio estimado: {self.prod_price}"

ESTADO_PEDIDO = [('Pend', 'Pendiente'), ('Ped', 'Pedido'), ('Ta', 'Taller'), ('Fin', 'Finalizado')]
FORMA_PAGO = [('TCred', 'Tarjeta de Crédito'), ('TDeb', 'Tarjeta de Débito'), ('BV', 'Billetera Virtual'), ('EFT', 'Efectivo')]

class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    vendedor = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="pedidos")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="solicitante")
    estado = models.CharField(max_length=10, default="Pend", choices=ESTADO_PEDIDO)
    tipo_pago = models.CharField(max_length=25, default="EFT", choices=FORMA_PAGO)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=20, null=False, blank=False)

    def save(self, *args, **kwargs):
        items_pedido = self.pedido.all()
        if items_pedido.exists():
            sum = 0
            for item in items_pedido:
                sum = sum + item.subtotal_pedido    
            self.total = sum
        else:
            self.total = 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nro.Pedido: {self.pk} | Paciente: {self.paciente} | Total: {self.total}"

class ItemsPedido(models.Model):
    product = models.ForeignKey(Product, related_name="composicion", on_delete=models.PROTECT)
    pedido = models.ForeignKey(Pedido, related_name="pedido", on_delete=models.CASCADE)
    precio_pedido = models.DecimalField(decimal_places=2, max_digits=20, null=False, blank=False)
    cantidad_pedido = models.IntegerField(null=False, blank=False)
    subtotal_pedido = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    def save(self, *args, **kwargs):
        self.subtotal_pedido = round(self.precio_pedido * self.cantidad_pedido, 2)
        super().save(*args, **kwargs)
        self.pedido.save()
    def __str__(self):
        return f"Nro.Pedido: {self.pedido.pk} | Paciente: {self.pedido.paciente} | Producto: {self.product.prod_title} | Cantidad: {self.cantidad_pedido} | Precio: {self.precio_pedido} | Subtotal: {self.subtotal_pedido}"
