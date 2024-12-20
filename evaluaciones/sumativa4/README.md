Evaluación Sumativa 4 (http://127.0.0.1:8000/api/docs)


Este proyecto es una aplicación web desarrollada con Django para gestionar productos, marcas, categorías y características. Incluye funciones como registro, filtrado y validación de productos, además de medidas de seguridad implementadas para garantizar una experiencia segura.

Requisitos
Python 3.11+
Django 5.1

Instalación

Instalar las dependencias:
    pip install django

Ingresar al directorio del proyecto:
    cd sumativa3/productos

Ejecutar migraciones:
    python manage.py migrate

Iniciar el servidor:
    python manage.py runserver

Acceder a la aplicación:

    Página de inicio de sesión: http://127.0.0.1:8000/login/
    Listado de productos: http://127.0.0.1:8000/productos/

Funcionalidades

    1. Listar productos
    Muestra una lista de productos con filtros por marca, categoría y características.
    2. Registrar productos
    Permite registrar nuevos productos con validación para evitar duplicados.
    3. Resultados
    Muestra un mensaje indicando el éxito o fallo en las operaciones de registro.
    4. Login y Logout
    Autenticación de usuarios para acceso restringido.
    5. Administración de Django
    Permite la gestión de datos mediante el panel de administración de Django.


Medidas de Seguridad Implementadas

1. Autenticación obligatoria
Descripción: Todas las vistas principales (listar_productos, registro_producto) están protegidas con el decorador @login_required.
Código:

from django.contrib.auth.decorators import login_required

@login_required
def listar_productos(request):
    ...
Efecto: Asegura que solo los usuarios autenticados puedan acceder a estas vistas.

2. Protección contra CSRF
Descripción: Se utiliza el middleware de Django para la protección contra CSRF en formularios, asegurando que las solicitudes POST sean válidas.
Código:

<form method="POST">
    {% csrf_token %}
    ...
</form>
Efecto: Previene ataques de falsificación de solicitudes entre sitios (CSRF).

3. Variables de sesión para validar roles
Descripción: Durante el inicio de sesión, se guardan en la sesión variables clave como el nombre del usuario, la fecha de inicio de sesión y si pertenece al grupo ADMIN_PRODUCTS.
Código:

request.session['username'] = user.username
request.session['is_admin_products'] = user.groups.filter(name='ADMIN_PRODUCTS').exists()
Efecto: Permite controlar el acceso a las funcionalidades administrativas.

Notas Adicionales

Configuraciones importantes:
SESSION_EXPIRE_AT_BROWSER_CLOSE = True: La sesión del usuario expira al cerrar el navegador.
CSRF_FAILURE_VIEW = 'app.views.csrf_failure': Redirige al login en caso de un fallo de validación CSRF.

Usuario administrador predeterminado:

Usuario: admin
Contraseña: inacap2024