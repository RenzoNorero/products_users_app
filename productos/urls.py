from django.urls import path
from . import views



handler404 = 'productos.views.error_handler'

urlpatterns = [
    path('tienda', views.tienda, name='tienda'),
    path('productos/list_products', views.list_products, name='list_products'),
    path('<int:sku>/', views.detalle_producto, name='detalle_producto'),
    path('productos/modificar/<int:prod_sku>/', views.mod_products, name='mod_products'),
    path('productos/eliminar/<int:prod_sku>/', views.del_products, name='del_products'),
    path('productos/agregar/', views.create_products, name='create_products')
]