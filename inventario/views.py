
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models   # ← IMPORTANTE (ESTO FALTABA)
from .models import Producto, Movimiento

# ============================================================
# LISTA DE PRODUCTOS
# ============================================================
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/productos/lista_productos.html', {'productos': productos})


# ============================================================
# AGREGAR PRODUCTO
# ============================================================
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        categoria = request.POST['categoria']
        cantidad = int(request.POST['cantidad'])
        stock_minimo = int(request.POST['stock_minimo'])
        descripcion = request.POST['descripcion']

        Producto.objects.create(
            nombre=nombre,
            categoria=categoria,
            cantidad=cantidad,
            stock_minimo=stock_minimo,
            descripcion=descripcion
        )
        messages.success(request, 'Producto agregado correctamente')
        return redirect('lista_productos')

    return render(request, 'inventario/productos/agregar_producto.html')


# ============================================================
# EDITAR PRODUCTO
# ============================================================
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.categoria = request.POST['categoria']
        producto.cantidad = int(request.POST['cantidad'])
        producto.stock_minimo = int(request.POST['stock_minimo'])
        producto.descripcion = request.POST['descripcion']
        producto.save()

        messages.success(request, 'Producto actualizado correctamente')
        return redirect('lista_productos')

    return render(request, 'inventario/productos/editar_producto.html', {'producto': producto})


# ============================================================
# ELIMINAR PRODUCTO
# ============================================================
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('lista_productos')


# ============================================================
# REGISTRAR ENTRADA
# ============================================================
def registrar_entrada(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])

        Movimiento.objects.create(
            producto=producto,
            tipo='entrada',
            cantidad=cantidad
        )

        producto.cantidad += cantidad
        producto.save()

        messages.success(request, 'Entrada registrada')
        return redirect('lista_productos')
    
    return render(request, 'inventario/movimientos/registrar_entrada.html', {'producto': producto})


# ============================================================
# REGISTRAR SALIDA
# ============================================================
def registrar_salida(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])

        if cantidad > producto.cantidad:
            messages.error(
                request,
                f"No puedes sacar {cantidad} unidades porque solo tienes {producto.cantidad} en stock."
            )
            return redirect('registrar_salida', id=producto.id)

        Movimiento.objects.create(
            producto=producto,
            tipo='salida',
            cantidad=cantidad
        )

        producto.cantidad -= cantidad
        producto.save()

        messages.success(request, 'Salida registrada correctamente')
        return redirect('lista_productos')

    return render(request, 'inventario/movimientos/registrar_salida.html', {'producto': producto})




# ============================================================
# HISTORIAL DE MOVIMIENTOS
# ============================================================
def historial_movimientos(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'inventario/movimientos/historial.html', {'movimientos': movimientos})


# ============================================================
# DASHBOARD
# ============================================================
from django.db.models import Sum

def dashboard(request):
    total_productos = Producto.objects.count()
    total_movimientos = Movimiento.objects.count()
    total_entradas = Movimiento.objects.filter(tipo='entrada').count()
    total_salidas = Movimiento.objects.filter(tipo='salida').count()

    # Productos con stock bajo
    bajos = Producto.objects.filter(cantidad__lte=models.F('stock_minimo'))

    context = {
        'total_productos': total_productos,
        'total_movimientos': total_movimientos,
        'total_entradas': total_entradas,
        'total_salidas': total_salidas,
        'bajos': bajos,
    }

    return render(request, 'inventario/dashboard.html', context)

