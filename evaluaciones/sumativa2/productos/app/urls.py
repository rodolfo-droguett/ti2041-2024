from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('registrar/', views.registro_producto, name='registro_producto'), 
]