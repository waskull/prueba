from django.db import models
from inventario.models import BaseModel

# Create your models here.
class Compra(BaseModel):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra {self.id}"
    
class CompraDetalle(BaseModel):
    cantidad = models.PositiveIntegerField()
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE)
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    precio =  models.DecimalField(default=1, null=False, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = "Compra Detalle"
        verbose_name_plural = "Compras Detalle"

    def __str__(self):
        return f"Compra Detalle {self.id}"

class Venta(BaseModel):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta {self.id}"
    
class VentaDetalle(BaseModel):
    cantidad = models.PositiveIntegerField()
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    precio =  models.DecimalField(default=1, null=False, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = "Venta Detalle"
        verbose_name_plural = "Ventas Detalle"

    def __str__(self):
        return f"Venta Detalle {self.id}"