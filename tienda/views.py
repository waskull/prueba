from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Compra, CompraDetalle, Venta, VentaDetalle
from inventario.models import Producto
from .serializers import CompraSerializer, VentaSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    # --- Bloqueo de Edición ---
    def update(self, request, *args, **kwargs):
        return Response({"error": "Las compras son registros históricos y no se pueden modificar."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # --- Lógica de Creación ---
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # El serializador valida que los productos existan y los tipos de datos sean correctos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        detalles_data = serializer.validated_data.pop('detalles')

        # Validar que existan detalles
        if not detalles_data:
            return Response({"error": "Debe incluir al menos un producto."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear cabecera
        compra = Compra.objects.create(**serializer.validated_data)
        total_acumulado = 0

        for item in detalles_data:
            producto = item['producto']
            cantidad = item['cantidad']
            precio = item['precio']

            CompraDetalle.objects.create(
                compra=compra, producto=producto,
                cantidad=cantidad, precio=precio
            )

            # Lógica: Sumar al stock
            producto.cantidad += cantidad
            producto.save()
            total_acumulado += (cantidad * precio)
        compra.total = total_acumulado
        compra.save()
        # Devolver el objeto creado usando el serializador
        return Response({"message": "Compra creada con exito"}, status=status.HTTP_201_CREATED)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    # Bloqueo estricto de edición
    def update(self, request, *args, **kwargs):
        return Response({"error": "Método PUT no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Método PATCH no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # 1. El serializador valida que los productos existan y los datos sean correctos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Extraemos los datos validados pero no guardamos aún el serializador
        detalles_data = serializer.validated_data.pop('detalles')
        cliente = serializer.validated_data.get('cliente', 'Consumidor Final')

        try:
            # 3. Lógica de negocio manual
            venta = Venta.objects.create(cliente=cliente)
            total_acumulado = 0

            for item in detalles_data:
                # 'item' ya contiene la instancia del modelo Producto gracias al ModelSerializer
                producto = item['producto']
                cantidad = item['cantidad']

                # Validación de Stock lógica
                if producto.cantidad < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre}. Disponible: {producto.cantidad}")

                # Crear el detalle físicamente
                VentaDetalle.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio
                )

                # Afectar inventario
                producto.cantidad -= cantidad
                producto.save()

                total_acumulado += (cantidad * producto.precio)

            # 4. Finalizar cabecera
            venta.total = total_acumulado
            venta.save()

            # Devolvemos la venta creada serializada
            output_serializer = VentaSerializer(venta)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
