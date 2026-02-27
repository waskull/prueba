from django.db import models
from inventario.models import BaseModel, Producto
from django.contrib.auth.models import User
# Create your models here.

class Compra(BaseModel):
    proveedor = models.CharField(max_length=150)
    total = models.DecimalField(decimal_places=2, default=0,max_digits=8)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Compra"
        verbose_name = "Compras"

class CompraDetalle(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(decimal_places=2, default=0.1,max_digits=8)
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)