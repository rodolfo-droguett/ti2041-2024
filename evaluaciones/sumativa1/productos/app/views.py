from django.shortcuts import render, redirect
from .models import Producto, Marca, Categoria, Caracteristica

# Create your views here.
def listar_productos(request):
    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()

    marca_id = request.GET.get('marca')
    categoria_id = request.GET.get('categoria')
    caracteristica_id = request.GET.get('caracteristica')

    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if caracteristica_id:
        productos = productos.filter(caracteristicas__id=caracteristica_id)

    return render(request, 'consulta.html', {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas
    })

def registro_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        marca_id = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')
        caracteristicas = request.POST.getlist('caracteristicas')

        # Validación básica
        if not codigo or not nombre or not precio or not marca_id or not categoria_id:
            return render(request, 'resultado.html', {'mensaje': 'Faltan datos'})

        # Crear el producto
        if Producto.objects.filter(codigo=codigo).exists():
            return render(request, 'resultado.html', {'mensaje': 'El código de producto ya existe. Intenta con otro.'})

        
            # Crear el producto
        marca = Marca.objects.get(id=marca_id)
        categoria = Categoria.objects.get(id=categoria_id)
        producto = Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                marca=marca,
                categoria=categoria
            )

        # Añadir características
        for caracteristica_id in caracteristicas:
            caracteristica = Caracteristica.objects.get(id=caracteristica_id)
            producto.caracteristicas.add(caracteristica)

        return render(request, 'resultado.html', {'mensaje': 'Producto registrado'})

    # Obtener datos para los selects y checkboxes
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()

    return render(request, 'registro.html', {
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas
    })