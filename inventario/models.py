from django.db import models

# Create your models here.

class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Producto(BaseModel):
    nombre = models.CharField(unique=True)
    cantidad = models.IntegerField(default=0)
    descripcion = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Categoria(BaseModel):
    nombre = models.CharField(unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"