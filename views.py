import os
import json
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from openai import OpenAI

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncHour
from django.utils import timezone

# Importamos tus modelos
from .models import Hortifruti, MovimientoInventario, Sucursal, StockPorSucursal

# Cargar variables de entorno
load_dotenv()
client = OpenAI(api_key="TU_API_KEY_AQUI")

# --- VISTAS PRINCIPALES ---

def index(request):
    """ Muestra la página principal filtrada por sucursal. """
    sucursal_id = request.GET.get('sucursal', 1)
    
    stocks = StockPorSucursal.objects.filter(
        sucursal_id=sucursal_id,
        producto__activo=True,
        cantidad_actual__gt=0 
    ).select_related('producto').order_by('-producto__fecha_oferta')
    
    sucursales = Sucursal.objects.all()
    
    return render(request, 'tienda/index.html', {
        'stocks': stocks,
        'sucursales': sucursales,
        'sucursal_actual': int(sucursal_id)
    })
@login_required
def dashboard_vendas(request):
    """ Datos para las gráficas de ventas para Experfrut. """
    movimientos_base = MovimientoInventario.objects.filter(tipo='SALIDA')

    # 1. Obtenemos los datos
    ventas_hora = movimientos_base.annotate(periodo=TruncHour('fecha')).values('periodo')
    ventas_dia = movimientos_base.annotate(periodo=TruncDay('fecha')).values('periodo')
    ventas_mes = movimientos_base.annotate(periodo=TruncMonth('fecha')).values('periodo')

    # 2. El retorno con la indentación corregida
    return render(request, 'dashboard_avanzado.html', {
        'ventas_hora': list(ventas_hora),
        'ventas_dia': list(ventas_dia),
        'ventas_mes': list(ventas_mes),
    })

@csrf_protect
@login_required(login_url='/admin/login/')
def registrar_salida(request):
    """ Registra venta y descuenta stock físicamente de la sucursal. """
    if request.method == 'POST':
        try:
            peso_raw = request.POST.get('peso_balanza')
            producto_id_raw = request.POST.get('producto_id')
            sucursal_id_raw = request.POST.get('sucursal_id', 1)

            if not peso_raw or not producto_id_raw:
                return JsonResponse({'status': 'error', 'message': 'Dados incompletos'}, status=400)

            producto_id = int(producto_id_raw)
            sucursal_id = int(sucursal_id_raw)

            peso_limpio = peso_raw.replace(',', '.')
            cantidad_decimal = Decimal(peso_limpio)

            producto = get_object_or_404(Hortifruti, id=producto_id)
            sucursal = get_object_or_404(Sucursal, id=sucursal_id)

            stock_sucursal, created = StockPorSucursal.objects.get_or_create(
                sucursal=sucursal,
                producto=producto
            )

            # --- NUEVA VALIDACIÓN DE STOCK (CAMBIO AGREGADO) ---
            if cantidad_decimal > stock_sucursal.cantidad_actual:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Erro de vendas: A quantidade de {cantidad_decimal} kg excede o estoque disponível de {stock_sucursal.cantidad_actual} kg nesta sucursal!'
                }, status=400)
            # ----------------------------------------------------

            valor_venta = producto.precio * cantidad_decimal

            MovimientoInventario.objects.create(
                sucursal=sucursal,
                producto=producto,
                cantidad=cantidad_decimal,
                valor_total=valor_venta,
                tipo='SALIDA',
                motivo="Venta realizada desde pesaje digital"
            )
            
            stock_sucursal.cantidad_actual -= cantidad_decimal
            stock_sucursal.save()
            
            return JsonResponse({
                'status': 'success', 
                'nuevo_stock': float(stock_sucursal.cantidad_actual),
                'mensaje': f'Saída de {peso_raw}kg de {producto.nombre} registrada!'
            })
            
        except (InvalidOperation, ValueError, TypeError) as e:
            return JsonResponse({'status': 'error', 'message': f'Erro nos dados: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

# --- VISTAS DE ANÁLISIS E IA ---

@login_required
def analista_ia(request):
    """ Genera datos estructurados para Dashboards Inteligentes """
    try:
        ventas = MovimientoInventario.objects.filter(tipo='SALIDA', anulado=False).values('sucursal__nombre').annotate(total=Sum('valor_total'))
        
        labels_vendas = [v['sucursal__nombre'] for v in ventas]
        data_vendas = [float(v['total']) for v in ventas]

        stock_bajo = StockPorSucursal.objects.filter(cantidad_actual__lt=10).select_related('producto', 'sucursal')[:5]
        
        labels_stock = [f"{s.producto.nombre} ({s.sucursal.nombre})" for s in stock_bajo]
        data_stock = [float(s.cantidad_actual) for s in stock_bajo]

        return JsonResponse({
            'status': 'success',
            'vendas_chart': {
                'labels': labels_vendas,
                'data': data_vendas
            },
            'stock_chart': {
                'labels': labels_stock,
                'data': data_stock
            },
            'recomendacion': f"La sucursal {max(ventas, key=lambda x: x['total'])['sucursal__nombre']} lidera hoy." if ventas else "Sin datos"
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def ai_test(request):
    """ Prueba rápida de conexión con OpenAI """
    pregunta = request.GET.get("pregunta", "Hola")

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un analista experto de ExperFrut."},
                {"role": "user", "content": pregunta}
            ]
        )

        texto = respuesta.choices[0].message.content
        return JsonResponse({"respuesta": texto})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# --- PASO 2: GRÁFICA INTELIGENTE (FILTRABLE) ---

@login_required
def dashboard_avanzado(request):
    """ Dashboard inteligente con filtros de sucursal, tipo de producto y tiempo """
    sucursal_id = request.GET.get('sucursal')
    categoria = request.GET.get('categoria') # 'fruta' o 'vegetal'
    escala = request.GET.get('escala', 'dia') # hora, dia, mes

    # Filtro base
    movs = MovimientoInventario.objects.filter(anulado=False)

    # Filtro por sucursal
    if sucursal_id and sucursal_id != 'todas':
        movs = movs.filter(sucursal_id=sucursal_id)

    # Filtro por Fruta/Vegetal
    if categoria == 'fruta':
        movs = movs.filter(producto__es_vegetal=False)
    elif categoria == 'vegetal':
        movs = movs.filter(producto__es_vegetal=True)

    # Agrupación temporal
    if escala == 'hora':
        trunc_func = TruncHour('fecha')
    elif escala == 'mes':
        trunc_func = TruncMonth('fecha')
    else:
        trunc_func = TruncDay('fecha')

    # Consulta maestra: Suma ventas y pérdidas
    reporte_qs = movs.annotate(periodo=trunc_func).values('periodo').annotate(
        ventas=Sum('valor_total', filter=Q(tipo='SALIDA')),
        perdidas=Sum('valor_total', filter=Q(tipo='PERDIDA'))
    ).order_by('periodo')

    # --- AJUSTE PARA COMPATIBILIDAD CON JS (EXPERFRUT BI) ---
    reporte_limpio = []
    for item in reporte_qs:
        if item['periodo']:
            if escala == 'hora':
                label = item['periodo'].strftime('%H:%M')
            elif escala == 'mes':
                label = item['periodo'].strftime('%b %Y')
            else:
                label = item['periodo'].strftime('%d/%m')
        else:
            label = "S/N"

        # Guardamos los valores numéricos limpios
        v_actual = float(item['ventas'] or 0)
        p_actual = float(item['perdidas'] or 0)

        reporte_limpio.append({
            'periodo': label,
            'ventas': v_actual,
            'perdidas': p_actual,
            # AGREGA ESTO: Resta automática para obtener el balance real
            'ganancia_real': v_actual - p_actual, 
        })

    # --- CAMBIO DE RUTA AQUÍ ---
    # Como moviste el archivo a la raíz de templates, quitamos 'tienda/'
    return render(request, 'dashboard_avanzado.html', {
        'reporte': reporte_limpio,
        'sucursales': Sucursal.objects.all(),
        'escala': escala,
        'sucursal_seleccionada': sucursal_id,
        'categoria_seleccionada': categoria,
    })