from django.contrib import admin

# Register your models here.
from .models import Product, Paciente, Pedido, ItemsPedido, Turno, Historia

admin.site.register(Product)
admin.site.register(Paciente)
admin.site.register(Pedido)
admin.site.register(ItemsPedido)
admin.site.register(Turno)
admin.site.register(Historia)
