from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Movimientos
    path('movimientos/', views.historial_movimientos, name='lista_movimientos'),
    path('movimiento/entrada/<int:id>/', views.registrar_entrada, name='registrar_entrada'),
    path('movimiento/salida/<int:id>/', views.registrar_salida, name='registrar_salida'),
    path('dashboard/', views.dashboard, name='dashboard'),


]
