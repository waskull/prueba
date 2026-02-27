from rest_framework import serializers
from .models import Compra, CompraDetalle

class CompraDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraDetalle
        fields = ("cantidad", "precio", "producto")


class CompraSerializer(serializers.ModelSerializer):
    detalles = CompraDetalleSerializer(many=True, write_only = True)
    creado_por = serializers.ReadOnlyField(source="creado_por.username")
    class Meta:
        model = Compra
        fields = ("proveedor","creado_por", "fecha_creacion", "fecha_modificacion", "total", "id", "detalles")
        read_only_fields = ['total']