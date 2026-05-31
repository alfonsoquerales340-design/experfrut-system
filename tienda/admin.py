from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Sum
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
from .models import Sucursal, Hortifruti, StockPorSucursal, MovimientoInventario

from django.contrib import admin
from .models import Hortifruti, StockPorSucursal, Sucursal, MovimientoInventario, CredencialHuella # Agregado CredencialHuella

class ResponsiveAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
                'admin/css/custom_admin.css?v=1.1', # <--- Agrega el ?v=1.1 aquí
            )
        }
        
        js = ('https://code.jquery.com/jquery-3.6.0.min.js',)

# --- 1. INLINES ---
class StockInline(admin.TabularInline):
    model = StockPorSucursal
    extra = 0
    readonly_fields = ('sucursal', 'cantidad_actual')
    can_delete = False

# --- 2. PRODUCTOS (Hortifruti) ---
@admin.register(Hortifruti)
class HortifrutiAdmin(admin.ModelAdmin): # Cambiamos ResponsiveAdmin por el estándar
    # En el celular, las primeras 3 columnas son las más importantes.
    # Movimos 'activo' al final y dejamos el nombre al principio.
    list_display = ('mostrar_imagen', 'nombre', 'precio_formateado', 'unidad', 'es_vegetal', 'activo')
    
    list_display_links = ('nombre',)
    list_filter = ('es_vegetal', 'activo', 'fecha_oferta')
    search_fields = ('nombre',)
    
    # IMPORTANTE: list_editable a veces rompe el diseño en móvil porque crea cuadros de texto.
    # Si ves que se sigue viendo mal, quita 'activo' de aquí.
    list_editable = ('activo',)
    
    inlines = [StockInline]
    
    # Reducimos el texto de las cabeceras para ganar espacio en el móvil
    def precio_formateado(self, obj):
        return f"R$ {obj.precio}"
    precio_formateado.short_description = 'R$' # Nombre corto

    def mostrar_imagen(self, obj):
        return "🍎" if not obj.es_vegetal else "🥦"
    mostrar_imagen.short_description = 'Icon' # Nombre corto

# --- 3. REGISTRO DE LA HUELLA ---
@admin.register(CredencialHuella)
class CredencialHuellaAdmin(admin.ModelAdmin):
    list_display = ('user', 'credential_id', 'sign_count')
    search_fields = ('user__username',)

# --- 3. CONFIGURACIÓN DE SEDES (Sucursal) ---
@admin.register(Sucursal)
class SucursalAdmin(ResponsiveAdmin):
    list_display = ('nombre', 'direccion', 'encargado', 'ver_mapa')
    search_fields = ('nombre', 'encargado__username')

    def ver_mapa(self, obj):
        return format_html('<a href="https://www.google.com/maps/search/?api=1&query={}" target="_blank">📍 Ver</a>', obj.direccion)
    ver_mapa.short_description = 'Mapa'

# --- 4. STOCK POR SUCURSAL ---
@admin.register(StockPorSucursal)
class StockPorSucursalAdmin(ResponsiveAdmin):
    list_display = ('producto', 'sucursal', 'cantidad_actual')
    list_filter = ('sucursal', 'producto')
    search_fields = ('producto__nombre',)

# --- 5. CONFIGURACIÓN DE USUARIOS (ORGANIZADO PARA MÓVIL Y PERMISOS) ---
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin): 
    # En móvil, menos es más. Solo 3 columnas para que no haya scroll horizontal.
    list_display = ('username', 'is_staff', 'is_active')
    
    # Filtros simplificados
    list_filter = ('is_staff', 'is_active')
    
    # Esto es vital para móviles: pone los botones de "Guardar" también arriba
    save_on_top = True 

    # --- AJUSTE PARA MÓVIL ---
    # Mantenemos esto comentado para evitar los cuadros gigantes de las fotos anteriores
    # filter_horizontal = ('groups', 'user_permissions')

    # Organizamos el formulario de edición en secciones (Fieldsets)
    fieldsets = (
        ('Credenciales', {'fields': ('username', 'password')}),
        ('Información', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos y Grupos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # --- EL COMANDO PARA CARGAR TU CSS ---
    # Esto vincula el archivo que vimos en la carpeta de tu proyecto
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(ResponsiveAdmin):
    # 1. Columnas de la tabla principal
    list_display = ('mostrar_producto', 'sucursal', 'tipo', 'cantidad', 'colorear_valor', 'fecha', 'anulado')
    list_filter = ('tipo', 'sucursal', 'fecha', 'anulado')
    search_fields = ('producto__nombre', 'motivo')
    
    readonly_fields = ('valor_total',) # Bloqueado en el formulario para que se autocalcule solo
    autocomplete_fields = ['producto']

    # --- OPERACIÓN MATEMÁTICA AUTOMÁTICA AL ADICIONAR EN EL FORMULARIO ---
    def save_model(self, request, obj, form, change):
        if obj.producto:
            from decimal import Decimal # Importación necesaria para evitar el TypeError
            
            # Buscamos el precio del producto (Hortifruti)
            precio_producto = getattr(obj.producto, 'precio', 0) or 0
            
            # Convertimos ambos valores a cadenas (str) primero para una conversión segura a Decimal
            cantidad_decimal = Decimal(str(obj.cantidad or 0))
            precio_decimal = Decimal(str(precio_producto))
            
            # UNIFICADO: Calcula automáticamente usando Decimal para SALIDA, PERDIDA y ENTRADA
            if obj.tipo in ['SALIDA', 'PERDIDA', 'ENTRADA']:
                obj.valor_total = cantidad_decimal * precio_decimal
            else:
                obj.valor_total = Decimal('0.00')
        else:
            from decimal import Decimal
            obj.valor_total = Decimal('0.00')
            
        # Guarda definitivamente el registro con el valor calculado
        super().save_model(request, obj, form, change)

    # --- DISEÑO DEL PRODUCTO CON ICONOS DINÁMICOS ---
    def mostrar_producto(self, obj):
        from django.utils.html import format_html
        
        # Obtenemos el icono basándonos en el campo 'es_vegetal' del modelo relacionado (Hortifruti)
        if obj.producto:
            icono = "🥦" if obj.producto.es_vegetal else "🍎"
            nombre = obj.producto.nombre
        else:
            icono = "❓"
            nombre = "Sin producto"

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-size: 1.2em;">{}</span>'
            '<span style="background: #f8f9fa; padding: 2px 8px; border-radius: 4px; font-weight: 600; color: #2c3e50; border: 1px solid #e0e0e0;">'
            '{}</span>'
            '</div>',
            icono, nombre
        )
    mostrar_producto.short_description = 'Producto'
    mostrar_producto.admin_order_field = 'producto'

    # --- DISEÑO DE COLORES PARA EL VALOR ---
    def colorear_valor(self, obj):
        from django.utils.html import format_html
        valor = obj.valor_total or 0
        if obj.anulado:
            return format_html('<span style="color: #9e9e9e; text-decoration: line-through;">R$ {}</span>', valor)
        
        # Unificamos colores: Azul para camión, Verde para ventas, Rojo para mermas
        if obj.tipo == 'ENTRADA':
            color = "#1E88E5" # Azul profesional para carga entrante
            prefijo = "Carga: R$"
        elif obj.tipo == 'SALIDA':
            color = "#2E7D32" # Verde para salidas
            prefijo = "R$"
        else:
            color = "#C62828" # Rojo para pérdidas
            prefijo = "R$"
            
        return format_html('<b style="color: {};">{} {}</b>', color, prefijo, valor)
    
    colorear_valor.short_description = 'Valor Total'

    # --- LÓGICA DE GRÁFICAS PARA EL ADMIN (CON OPERACIÓN MATEMÁTICA DE BALANCE REAL) ---
    def changelist_view(self, request, extra_context=None):
        from django.db.models import Sum, Case, When, F, FloatField
        from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth

        def obtener_estadisticas(trunc_func, formato_fecha):
            # El sistema ahora calcula de forma inteligente: Suma ventas y resta inversiones y pérdidas
            stats = (
                MovimientoInventario.objects.filter(anulado=False)
                .annotate(periodo=trunc_func('fecha'))
                .values('periodo')
                .annotate(
                    total=Sum(
                        Case(
                            When(tipo='SALIDA', then=F('valor_total')),     # Suma ventas (+)
                            When(tipo='ENTRADA', then=-F('valor_total')),   # Resta el costo del camión (-)
                            When(tipo='PERDIDA', then=-F('valor_total')),   # Resta las mermas (-)
                            default=0.0,
                            output_field=FloatField()
                        )
                    )
                )
                .order_by('periodo')
            )
            labels = [s['periodo'].strftime(formato_fecha) for s in stats if s['periodo']]
            values = [float(s['total'] or 0) for s in stats if s['periodo']]
            return {"labels": labels, "values": values}

        extra_context = extra_context or {}
        extra_context['chart_data_all'] = {
            "horas": obtener_estadisticas(TruncHour, '%H:00'),
            "dias": obtener_estadisticas(TruncDay, '%d/%m'),
            "semanas": obtener_estadisticas(TruncWeek, 'Sem %W'),
            "meses": obtener_estadisticas(TruncMonth, '%b %Y'),
        }
        return super().changelist_view(request, extra_context=extra_context)
