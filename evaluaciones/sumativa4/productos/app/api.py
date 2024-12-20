from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http import Http404
from typing import List
from .models import Producto, Marca, Categoria, Caracteristica
from .utils import generar_token, JWTAuth

# Inicializar API
api = NinjaAPI(
    title="API",
    version="1.0.0",
    docs_url="/docs",  
    openapi_url="/openapi.json",
)

# Inicializar autenticación JWT
auth = JWTAuth()

# Manejo de errores
@api.exception_handler(Http404)
def error_404(request, ex):
    return api.create_response(
        request, {"detail": "Recurso no encontrado"}, status=404
    )

# Schemas
class AuthRequest(Schema):
    username: str
    password: str

class ProductoSchema(Schema):
    id: int
    codigo: str
    nombre: str
    precio: float
    marca: str
    categoria: str

class ProductoCreateSchema(Schema):
    codigo: str
    nombre: str
    precio: float
    marca_id: int
    categoria_id: int
    caracteristicas_ids: List[int] = []

# Endpoints de autenticación
@api.post("/token", tags=["Autenticación"])
def obtener_token(request, data: AuthRequest):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return {"error": "Credenciales inválidas"}
    token = generar_token(user)
    return {"token": token}


@api.get("/productos", response=List[ProductoSchema], tags=["Productos"])
def listar_productos(request, marca: int = None, categoria: int = None):
    productos = Producto.objects.all()

    if marca:
        productos = productos.filter(marca_id=marca)
    if categoria:
        productos = productos.filter(categoria_id=categoria)

    return [
        ProductoSchema(
            id=p.id,
            codigo=p.codigo,
            nombre=p.nombre,
            precio=p.precio,
            marca=p.marca.nombre,
            categoria=p.categoria.nombre,
        )
        for p in productos
    ]

@api.post("/productos", auth=auth, tags=["Productos"])
def crear_producto(request, data: ProductoCreateSchema):
    marca = get_object_or_404(Marca, id=data.marca_id)
    categoria = get_object_or_404(Categoria, id=data.categoria_id)

    producto = Producto.objects.create(
        codigo=data.codigo,
        nombre=data.nombre,
        precio=data.precio,
        marca=marca,
        categoria=categoria
    )

    for caracteristica_id in data.caracteristicas_ids:
        caracteristica = get_object_or_404(Caracteristica, id=caracteristica_id)
        producto.caracteristicas.add(caracteristica)

    return ProductoSchema(
        id=producto.id,
        codigo=producto.codigo,
        nombre=producto.nombre,
        precio=producto.precio,
        marca=producto.marca.nombre,
        categoria=producto.categoria.nombre,
    )

@api.put("/productos/{codigo}", auth=auth, tags=["Productos"])
def actualizar_producto(request, codigo: str, data: ProductoCreateSchema):
    producto = get_object_or_404(Producto, codigo=codigo)

    producto.codigo = data.codigo
    producto.nombre = data.nombre
    producto.precio = data.precio
    producto.marca = get_object_or_404(Marca, id=data.marca_id)
    producto.categoria = get_object_or_404(Categoria, id=data.categoria_id)
    producto.save()

    producto.caracteristicas.clear()
    for caracteristica_id in data.caracteristicas_ids:
        caracteristica = get_object_or_404(Caracteristica, id=caracteristica_id)
        producto.caracteristicas.add(caracteristica)

    return {"message": "Producto actualizado correctamente"}

@api.delete("/productos/{codigo}", auth=auth, tags=["Productos"])
def eliminar_producto(request, codigo: str):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.delete()
    return {"message": "Producto eliminado correctamente"}
