from rest_framework import serializers
from tienda.models import Compra, CompraDetalle, Venta, VentaDetalle

class CompraDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraDetalle
        fields = ['producto', 'cantidad', 'precio']

class CompraSerializer(serializers.ModelSerializer):
    detalles = CompraDetalleSerializer(many=True) # Requerido para validación en create

    class Meta:
        model = Compra
        fields = ['id', 'fecha_creacion', 'fecha_modificacion', 'proveedor', 'total', 'detalles']
        read_only_fields = ['total']

class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = ['producto', 'cantidad', 'precio']

class VentaSerializer(serializers.ModelSerializer):
    detalles = VentaDetalleSerializer(many=True, write_only=True)
    class Meta:
        model = Venta
        fields = ['id', 'fecha_creacion', 'fecha_modificacion', 'cliente', 'total', 'detalles']
        read_only_fields = ['total']