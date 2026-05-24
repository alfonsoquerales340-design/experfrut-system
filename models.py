from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# 0. Modelo para la Huella Dactilar
class CredencialHuella(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credential_id = models.CharField(max_length=255, unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField(default=0)

    class Meta:
        app_label = 'apps'  # Vincula el modelo a la app de la raíz

    def __str__(self):
        return f"Huella de {self.user.username}"


# 1. Sedes de Experfrut
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Sede")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    encargado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sucursales')

    class Meta:
        app_label = 'apps'  # Vincula el modelo a la app de la raíz
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.nombre


# 2. Información General del Producto
class Hortifruti(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    unidad = models.CharField(max_length=20, default="kg", verbose_name="Unidad")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Venta (R$)")
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio Costo (R$)")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    es_vegetal = models.BooleanField(default=False, verbose_name="¿Es Vegetal?")
    activo = models.BooleanField(default=True)
    fecha_oferta = models.DateField(auto_now_add=True)

    class Meta:
        app_label = 'apps'  # Vincula el modelo a la app de la raíz
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


# 3. Stock individual por cada Tienda
class StockPorSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='existencias')
    producto = models.ForeignKey(Hortifruti, on_delete=models.CASCADE, related_name='existencias')
    cantidad_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        app_label = 'apps'  # Vincula el modelo a la app de la raíz
        unique_together = ('sucursal', 'producto')
        verbose_name = "Stock por Sucursal"
        verbose_name_plural = "Stocks por Sucursales"

    def __str__(self):
        return f"{self.producto.nombre} en {self.sucursal.nombre}: {self.cantidad_actual} {self.producto.unidad}"


# 4. Historial de Movimientos
class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada (Llegada de camión)'),
        ('SALIDA', 'Salida (Venta/Balanza)'),
        ('PERDIDA', 'Pérdida (Merma)'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='movimientos')
    producto = models.ForeignKey(Hortifruti, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Total (R$)")
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)
    anulado = models.BooleanField(default=False, verbose_name="¿Anulado?")

    class Meta:
        app_label = 'apps'  # Vincula el modelo a la app de la raíz
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"

    # --- CALCULAR VALOR AUTOMÁTICAMENTE ---
    def save(self, *args, **kwargs):
        if self.producto:
            if not self.valor_total or self.valor_total == 0:
                if self.tipo == 'SALIDA':
                    self.valor_total = float(self.cantidad) * float(self.producto.precio or 0)
                elif self.tipo in ['PERDIDA', 'ENTRADA']:
                    self.valor_total = float(self.cantidad) * float(self.producto.costo or 0)
         
        super().save(*args, **kwargs)

    def __str__(self):
        estado = "[ANULADO]" if self.anulado else ""
        return f"{estado} {self.tipo} - {self.producto.nombre} en {self.sucursal.nombre} (R$ {self.valor_total})"


# --- SEÑALES ---
@receiver(post_save, sender=MovimientoInventario)
def actualizar_stock_sucursal(sender, instance, created, **kwargs):
    stock_relacionado, _ = StockPorSucursal.objects.get_or_create(
        sucursal=instance.sucursal,
        producto=instance.producto
    )
    
    cantidad_decimal = Decimal(str(instance.cantidad))
    
    if created:
        if instance.tipo == 'ENTRADA':
            stock_relacionado.cantidad_actual += cantidad_decimal
        elif instance.tipo in ['SALIDA', 'PERDIDA']:
            stock_relacionado.cantidad_actual -= cantidad_decimal
        stock_relacionado.save()

    elif instance.anulado:
        if instance.tipo == 'ENTRADA':
            stock_relacionado.cantidad_actual -= cantidad_decimal
        elif instance.tipo in ['SALIDA', 'PERDIDA']:
            stock_relacionado.cantidad_actual += cantidad_decimal
        stock_relacionado.save()
