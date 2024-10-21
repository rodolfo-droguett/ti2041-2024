Evaluacion sumativa 1 - Gestión de Productos - Django

Este proyecto es una aplicación web desarrollada con Django para gestionar productos.
Permite listar, registrar y validar productos en una estructura de almacenamiento en memoria.

Requisitos

- **Python**
- **Django**

  
Instalación

1. Clonar el repositorio

2. Instalar django

3. Entrar en directorio del proyecto: cd sumativa1/productos

4. Iniciar servido: python manage.py runserver

5. Acceder a la aplicacion: http://127.0.0.1:8000/productos/


Funcionalidades
Listar productos: Muestra una lista de todos los productos registrados.
Registrar producto: Permite registrar nuevos productos con validación de datos.
Validación de producto: Asegura que el nombre, precio y descripción sean proporcionados antes de registrar el producto.
Estructura del proyecto
La estructura del proyecto es la siguiente:

app/: Contiene la lógica principal de la aplicación, incluidas vistas y modelos.
static/: Archivos estáticos, como el CSS personalizado (styles.css).
templates/: Contiene los templates HTML para listar, registrar, y mostrar resultados.
manage.py: Script para gestionar el proyecto Django.