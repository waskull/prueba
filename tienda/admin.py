from django.contrib import admin
from .models import Venta, Compra, CompraDetalle, VentaDetalle

# Register your models here.

admin.site.register(Venta)
admin.site.register(Compra)
admin.site.register(CompraDetalle)
admin.site.register(VentaDetalle)