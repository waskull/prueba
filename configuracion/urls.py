
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventario.views import InventarioListView, InventarioDetailView, CategoriaListView, CategoriaDetailView
from tienda.views import CompraViewSet, VentaViewSet
router = DefaultRouter()
router.register(r'compra', CompraViewSet, basename='compra')
router.register(r'venta', VentaViewSet, basename='venta')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categoria/', CategoriaListView.as_view(), name="categoria"),
    path('api/categoria/<int:pk>/', CategoriaDetailView.as_view(), name="categoria-detalle"),
    path('api/inventario/', InventarioListView.as_view(), name="inventario"),
    path('api/inventario/<int:pk>/', InventarioDetailView.as_view(), name="inventario-detalle"),
    path('api/', include(router.urls)),
]
