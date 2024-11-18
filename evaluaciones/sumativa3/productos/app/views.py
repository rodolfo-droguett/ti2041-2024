from django.shortcuts import render, redirect
from .models import Producto, Marca, Categoria, Caracteristica
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Guardar datos en sesión
            request.session['username'] = user.username
            request.session['login_time'] = str(now())
            request.session['is_admin_products'] = user.groups.filter(name='ADMIN_PRODUCTS').exists()
            return redirect('listar_productos')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')
# Create your views here.

@login_required
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

@login_required
def registro_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        marca_id = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')
        caracteristicas = request.POST.getlist('caracteristicas')

        if not codigo or not nombre or not precio or not marca_id or not categoria_id:
            return render(request, 'resultado.html', {'mensaje': 'Faltan datos'})

        if Producto.objects.filter(codigo=codigo).exists():
            return render(request, 'resultado.html', {'mensaje': 'El código de producto ya existe. Intenta con otro.'})

        
        marca = Marca.objects.get(id=marca_id)
        categoria = Categoria.objects.get(id=categoria_id)
        producto = Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                marca=marca,
                categoria=categoria
            )

        for caracteristica_id in caracteristicas:
            caracteristica = Caracteristica.objects.get(id=caracteristica_id)
            producto.caracteristicas.add(caracteristica)

        return render(request, 'resultado.html', {'mensaje': 'Producto registrado'})

    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()

    return render(request, 'registro.html', {
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas
    })