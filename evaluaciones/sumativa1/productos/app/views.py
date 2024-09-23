from django.shortcuts import render
from .data import productos

# Create your views here.
def listar_productos(request):
    return render(request, 'consulta.html', {'productos': productos})

def registro_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        descripcion = request.POST['descripcion']

        if not nombre:
            return render(request, 'resultado.html', {'mensaje': 'El nombre esta vacío'})
        if not precio or float(precio) <= 0:
            return render(request, 'resultado.html', {'mensaje': 'El precio incorrecto'})
        if not descripcion:
            return render(request, 'resultado.html', {'mensaje': 'La descripción esta vacía'})

        
        producto = {
            'nombre': nombre,
            'precio': float(precio),
            'descripcion': descripcion
        }
        productos.append(producto)
        return render(request, 'resultado.html', {'mensaje': 'Producto registrado con éxito'})
    
    return render(request, 'registro.html')