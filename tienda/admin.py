from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, F, FloatField
from django.db.models.functions import TruncHour, TruncDay, TruncWeek, TruncMonth
from django.utils.html import format_html
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe
from .models import Sucursal, Hortifruti, StockPorSucursal, MovimientoInventario, CredencialHuella


# =====================================================================
# 🔥 INYECCIÓN GLOBAL: BOTÓN FLOTANTE INMUNE A JAZZMIN 🔥
# =====================================================================
# Sobrescribimos el contexto base del sitio de administración para pintar
# el botón fijo en la esquina inferior derecha de manera universal.
original_each_context = admin.site.each_context

def nuevo_each_context(request):
    context = original_each_context(request)
    context['html_inyectado'] = mark_safe('''
        <style>
            .boton-flotante-tienda-universal {
                position: fixed !important;
                bottom: 25px !important;
                right: 25px !important;
                background-color: #28a745 !important;
                color: white !important;
                font-weight: bold !important;
                font-size: 15px !important;
                padding: 12px 22px !important;
                border-radius: 50px !important;
                box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3) !important;
                z-index: 99999999 !important; /* Capa por encima de todo Jazzmin */
                text-decoration: none !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: transform 0.2s ease, background-color 0.2s ease !important;
                cursor: pointer !important;
            }
            .boton-flotante-tienda-universal:hover, .boton-flotante-tienda-universal:active {
                background-color: #218838 !important;
                transform: scale(1.05) !important;
            }
            @media (max-width: 768px) {
                .boton-flotante-tienda-universal {
                    bottom: 20px !important;
                    right: 20px !important;
                    padding: 10px 18px !important;
                    font-size: 14px !important;
                }
            }
        </style>

        <a href="/" class="boton-flotante-tienda-universal">
            <i class="fas fa-shopping-basket" style="margin-right: 8px;"></i> Ver Tienda 🏪
        </a>
    ''')
    return context

admin.site.each_context = nuevo_each_context
# =====================================================================


# --- 0. CONFIGURACIÓN BASE RESPONSIVA ---
class ResponsiveAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
                'admin/css/custom_admin.css?v=1.5', 
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/retorno_movil.js?v=2.0',  
        )


# --- 1. INLINES ---
class StockInline(admin.TabularInline):
    model = StockPorSucursal
    extra = 0
    readonly_fields = ('sucursal', 'cantidad_actual')
    can_delete = False


# --- 2. PRODUCTOS (Hortifruti) ---
@admin.register(Hortifruti)
class HortifrutiAdmin(ResponsiveAdmin):  
    list_display = ('mostrar_imagen', 'nombre', 'precio_formateado', 'unidad', 'es_vegetal', 'activo')
    list_display_links = ('nombre',)
    list_filter = ('es_vegetal', 'activo', 'fecha_oferta')
    search_fields = ('nombre',)
    list_editable = ('activo',)
    inlines = [StockInline]
    
    def precio_formateado(self, obj):
        return f"R$ {obj.precio}"
    precio_formateado.short_description = 'R$'

    def mostrar_imagen(self, obj):
        return "🍎" if not obj.es_vegetal else "🥦"
    mostrar_imagen.short_description = 'Icon'


# --- 3. REGISTRO DE LA HUELLA ---
@admin.register(CredencialHuella)
class CredencialHuellaAdmin(ResponsiveAdmin):  
    list_display = ('user', 'credential_id', 'sign_count')
    search_fields = ('user__username',)


# --- 4. CONFIGURACIÓN DE SEDES (Sucursal) ---
@admin.register(Sucursal)
class SucursalAdmin(ResponsiveAdmin):
    list_display = ('nombre', 'direccion', 'encargado', 'ver_mapa')
    search_fields = ('nombre', 'encargado__username')

    def ver_mapa(self, obj):
        return format_html('<a href="https://www.google.com/maps/search/?api=1&query={}" target="_blank">📍 Ver</a>', obj.direccion)
    ver_mapa.short_description = 'Mapa'


# --- 5. STOCK POR SUCURSAL ---
@admin.register(StockPorSucursal)
class StockPorSucursalAdmin(ResponsiveAdmin):
    list_display = ('producto', 'sucursal', 'cantidad_actual')
    list_filter = ('sucursal', 'producto')
    search_fields = ('producto__nombre',)


# --- 6. CONFIGURACIÓN DE USUARIOS ---
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin, ResponsiveAdmin): 
    form = CustomUserChangeForm  
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    save_on_top = True 

    fieldsets = (
        ('Credenciales', {'fields': ('username', 'password')}),
        ('Información', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos y Grupos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )


# --- 7. MOVIMIENTOS E INVENTARIO INTELIGENTE ---
@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(ResponsiveAdmin):
    list_display = ('mostrar_producto', 'sucursal', 'tipo', 'cantidad', 'colorear_valor', 'fecha', 'anulado')
    list_filter = ('tipo', 'sucursal', 'fecha', 'anulado')
    search_fields = ('producto__nombre', 'motivo')
    readonly_fields = ('valor_total',)
    autocomplete_fields = ['producto']

    def save_model(self, request, obj, form, change):
        if obj.producto:
            from decimal import Decimal
            precio_producto = getattr(obj.producto, 'precio', 0) or 0
            cantidad_decimal = Decimal(str(obj.cantidad or 0))
            precio_decimal = Decimal(str(precio_producto))
            
            if obj.tipo in ['SALIDA', 'PERDIDA', 'ENTRADA']:
                obj.valor_total = cantidad_decimal * precio_decimal
            else:
                obj.valor_total = Decimal('0.00')
        else:
            from decimal import Decimal
            obj.valor_total = Decimal('0.00')
            
        super().save_model(request, obj, form, change)

    def mostrar_producto(self, obj):
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

    def colorear_valor(self, obj):
        valor = obj.valor_total or 0
        if obj.anulado:
            return format_html('<span style="color: #9e9e9e; text-decoration: line-through;">R$ {}</span>', valor)
        
        if obj.tipo == 'ENTRADA':
            color = "#1E88E5"
            prefijo = "Carga: R$"
        elif obj.tipo == 'SALIDA':
            color = "#2E7D32"
            prefijo = "R$"
        else:
            color = "#C62828"
            prefijo = "R$"
            
        return format_html('<b style="color: {};">{} {}</b>', color, prefijo, valor)
    
    colorear_valor.short_description = 'Valor Total'

    def changelist_view(self, request, extra_context=None):
        def obtener_estadisticas(trunc_func, formato_fecha):
            stats = (
                MovimientoInventario.objects.filter(anulado=False)
                .annotate(periodo=trunc_func('fecha'))
                .values('periodo')
                .annotate(
                    total=Sum(
                        Case(
                            When(tipo='SALIDA', then=F('valor_total')),
                            When(tipo='ENTRADA', then=-F('valor_total')),
                            When(tipo='PERDIDA', then=-F('valor_total')),
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

        resultado_base = super().changelist_view(request, extra_context=extra_context)
        extra_context = resultado_base.context_data
        
        extra_context['chart_data_all'] = {
            "horas": obtener_estadisticas(TruncHour, '%H:00'),
            "dias": obtener_estadisticas(TruncDay, '%d/%m'),
            "semanas": obtener_estadisticas(TruncWeek, 'Sem %W'),
            "meses": obtener_estadisticas(TruncMonth, '%b %Y'),
        }
        return resultado_base
