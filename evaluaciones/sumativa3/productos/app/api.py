from ninja import NinjaAPI
from app.models import Producto, Marca, Categoria
from ninja.security import django_auth
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

api = NinjaAPI(title="Gestión de Productos API", version="1.0")

# --- Obtener Token JWT ---
@api.post("/token", tags=["Auth"])
def get_token(request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if not user:
        return {"error": "Invalid credentials"}
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

# --- Obtener listado de categorías ---
@api.get("/categorias", tags=["Categorías"])
def listar_categorias(request):
    return [{"id": c.id, "nombre": c.nombre} for c in Categoria.objects.all()]

# --- Obtener listado de marcas ---
@api.get("/marcas", tags=["Marcas"])
def listar_marcas(request):
    return [{"id": m.id, "nombre": m.nombre} for m in Marca.objects.all()]

# --- Obtener listado de productos ---
@api.get("/productos", tags=["Productos"])
def listar_productos(request, marca: int = None, categoria: int = None):
    productos = Producto.objects.all()
    if marca:
        productos = productos.filter(marca_id=marca)
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    return [
        {"codigo": p.codigo, "nombre": p.nombre, "marca": p.marca.nombre, "precio": p.precio}
        for p in productos
    ]

# --- Obtener detalle de un producto ---
@api.get("/producto/{codigo}", tags=["Productos"])
def detalle_producto(request, codigo: str):
    producto = get_object_or_404(Producto, codigo=codigo)
    return {
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "marca": producto.marca.nombre,
        "categoria": producto.categoria.nombre,
        "precio": producto.precio,
        "caracteristicas": [c.nombre for c in producto.caracteristicas.all()],
    }

# --- Modificar un producto (algunos atributos) ---
@api.patch("/producto/{codigo}", tags=["Productos"])
def modificar_producto_parcial(request, codigo: str, nombre: str = None, precio: float = None):
    producto = get_object_or_404(Producto, codigo=codigo)
    if nombre:
        producto.nombre = nombre
    if precio:
        producto.precio = precio
    producto.save()
    return {"success": True, "mensaje": "Producto modificado parcialmente."}

# --- Modificar un producto (todos los atributos) ---
@api.put("/producto/{codigo}", tags=["Productos"], auth=django_auth)
def modificar_producto_completo(request, codigo: str, nombre: str, precio: float, marca: int, categoria: int):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.nombre = nombre
    producto.precio = precio
    producto.marca_id = marca
    producto.categoria_id = categoria
    producto.save()
    return {"success": True, "mensaje": "Producto modificado completamente."}
