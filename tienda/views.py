from django.contrib.auth.models import User
from django.db import transaction
from .serializers import *
from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Compra, CompraDetalle


# Create your views here.
class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompraSerializer

    @transaction.atomic
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        detalles = serializer.validated_data.pop("detalles")

        if not detalles:
            return Response({"message":"Debes enviar al menos un producto"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        compra = Compra.objects.create(**serializer.validated_data, creado_por=request.user)
        total_acumulado = 0

        for item in detalles:
            producto = item["producto"]
            cantidad = item["cantidad"]
            precio = item["precio"]

            total_acumulado += (cantidad*precio)

            CompraDetalle.objects.create(compra=compra,producto=producto, cantidad=cantidad, precio=precio)

            producto.cantidad += cantidad
            producto.save()



        compra.total = total_acumulado
        compra.save()

        return Response({"message":"Compra creada"}, status=status.HTTP_201_CREATED)