# Sistema de Inventario para Papelería

Proyecto escolar desarrollado en **Python** con el objetivo de administrar el inventario de una papelería de manera sencilla, organizada y funcional.

El sistema está diseñado para manejar productos, inventario, usuarios, ventas, alertas de stock bajo y reportes básicos. El proyecto se encuentra finalizado y completamente funcional, integrando la estructura principal, base de datos, módulos CRUD, sistema de alertas y reportes.

---

## Objetivo del proyecto

Desarrollar un sistema de inventario que facilite el control de productos dentro de una papelería, permitiendo registrar artículos, consultar existencias, controlar entradas y salidas, registrar ventas y apoyar la toma de decisiones mediante reportes.

---

## Descripción general del sistema

El sistema busca reemplazar el control manual de inventario por una aplicación sencilla que permita administrar la información de forma más ordenada.

El proyecto contempla los siguientes módulos:

- Módulo de Login
- Módulo de Usuarios
- Módulo de Productos
- Módulo de Categorías
- Módulo de Proveedores
- Módulo de Inventario
- Módulo de Ventas
- Módulo de Alertas
- Módulo de Reportes
- Módulo de Respaldos

---

## Tecnologías utilizadas

- Python
- SQLite (Base de datos relacional)
- Tkinter (Interfaz gráfica de usuario)
- Visual Studio Code
- Git
- GitHub

---

## Estado actual del proyecto

Actualmente cuenta con:

- Estructura inicial organizada por carpetas.
- Conexión a base de datos SQLite.
- Creación de tablas principales.
- Usuario administrador por defecto.
- Pantalla básica de inicio de sesión.
- Menú principal básico.
- Modelos principales del sistema.
- Controlador para productos.
- Funciones CRUD para productos desde el controlador.

---

## Funcionalidades implementadas

### Login básico

El sistema cuenta con una pantalla de inicio de sesión que permite ingresar con un usuario administrador de prueba.

Usuario de prueba:

```text
Usuario: admin
Contraseña: admin123
```

### Base de datos

Se utiliza SQLite para almacenar la información de forma local.

La base de datos se genera automáticamente al ejecutar el archivo de creación de tablas.

### CRUD de productos

Se implementaron controladores para realizar las siguientes operaciones principales:
- **Productos:** Registrar, listar, buscar por código, actualizar y eliminar. (Al registrar, se crea el inventario inicial automáticamente).
- **Inventario:** Control de entradas, salidas y verificación automática de stock mínimo.
- **Ventas:** Generación de tickets/comprobantes de venta y descuento automático del inventario.
- **Reportes y Respaldos:** Exportación de la información de ventas/inventario y creación de copias de seguridad de la base de datos local.

---

## Estructura del proyecto

```text
Proyecto_Papeleria/
|
│   .gitignore
│   main.py
│   README.md
│   requirements.txt
│   
├───assets
│       estilos.py
│       logo.png
│       
├───controllers
│       alerta_controller.py
│       categoria_controller.py
│       inventario_controller.py
│       producto_controller.py
│       proveedor_controller.py
│       reporte_controller.py
│       respaldo_controller.py
│       usuario_controller.py
│       venta_controller.py
│       
├───database
│       conexion.py
│       crear_tablas.py
│       inventario.db
│       
├───models
│       alerta.py
│       categoria.py
│       detalle_venta.py
│       inventario.py
│       producto.py
│       proveedor.py
│       reporte.py
│       respaldo.py
│       usuario.py
│       venta.py
│       
├───services
│       auth_service.py
│       inventario_service.py
│       reporte_service.py
│       venta_service.py
│       __init__.py
│       
├───utils
│       exportar.py
│       mensajes.py
│       validaciones.py
│       __init__.py
│       
└───views
        alertas_view.py
        categorias_view.py
        inventario_view.py
        layout_view.py
        login_view.py
        menu_view.py
        productos_view.py
        proveedores_view.py
        reportes_view.py
        respaldos_view.py
        usuarios_view.py
        ventas_view.py
```

---

## Explicación de carpetas

| Carpeta / archivo | Descripción |
|---|---|
| `main.py` | Archivo principal que inicia la aplicación |
| `database/` | Contiene la conexión con SQLite y la creación de tablas |
| `models/` | Contiene las clases principales del sistema y diccionarios de datos |
| `controllers/` | Contiene la lógica para manejar las operaciones e interactuar con la BD |
| `services/` | Carpeta para reglas de negocio complejas |
| `utils/` | Funciones auxiliares como validaciones, mensajes emergentes o exportaciones |
| `views/` | Contiene todas las pantallas e interfaces gráficas construidas con Tkinter |
| `assets/` | Carpeta para imágenes, íconos o recursos visuales |

---

## Modelos principales

El sistema contempla los siguientes modelos:

Modelo | Descripción |
|---|---|
| Usuario | Representa al administrador o vendedor que accede al sistema. |
| Producto | Contiene la información de los artículos de papelería. |
| Categoria | Agrupa productos según su tipo. |
| Proveedor | Guarda datos básicos de quien suministra productos. |
| Inventario | Controla la cantidad actual y ubicación de cada producto. |
| Venta | Registra las ventas realizadas por los usuarios. |
| DetalleVenta | Guarda los productos incluidos en una venta. |
| Alerta | Registra avisos cuando el stock llega al mínimo. |
| Reporte | Permite consultar información del inventario y ventas. |
| Respaldo | Representa la copia de seguridad física e historial del sistema. |

---

## Base de datos

El sistema utiliza una base de datos local en SQLite.

Tablas principales:

| Tabla | Propósito |
|---|---|
| usuario | Guarda los datos de acceso y rol de cada usuario. |
| categoria | Clasifica los productos de la papelería. |
| proveedor | Registra información básica de los proveedores. |
| producto | Almacena datos generales de cada artículo. |
| inventario | Controla la existencia actual y ubicación del producto. |
| venta | Registra ventas realizadas por los usuarios. |
| detalle_venta | Guarda los productos y cantidades de cada venta. |
| alerta | Registra alertas generadas por stock bajo. |
| respaldo | Guarda el historial de copias de seguridad realizadas. |

---

## Requisitos funcionales principales

| Clave | Requisito |
|---|---|
| RF01 | Administración de productos (CRUD). |
| RF02 | Consultas y búsquedas de productos. |
| RF04 | Registro de entradas al inventario. |
| RF05 | Realizar y consultar ventas con registro de vendedor y total. |
| RF06 | Generación de alertas de stock mínimo. |
| RF07 | Reportes de sistema. |
| RF08 | Inicio de sesión con usuario y contraseña. |
| RF09 | Gestión de usuarios y permisos. |

---

## Requisitos técnicos

Para ejecutar el proyecto se necesita:

- Python instalado.
- Visual Studio Code.
- Git, en caso de trabajar con repositorio.
- Sistema operativo Windows.

El proyecto está diseñado para funcionar sin librerías externas de terceros, utilizando exclusivamente las integradas en Python:
- `sqlite3` (Manejo de base de datos)
- `tkinter` (Interfaz gráfica)
- `shutil` (Gestión de copias de seguridad)

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/MiguelHedzz/Proyecto_Papeleria.git
```

### 2. Entrar a la carpeta del proyecto

```bash
cd Proyecto_Papeleria
```

### 3. Crear entorno virtual

```bash
python -m venv venv
```

### 4. Activar entorno virtual en Windows

```bash
.\venv\Scripts\Activate.ps1
```

Si PowerShell muestra error de permisos, ejecutar:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después volver a activar:

```bash
.\venv\Scripts\Activate.ps1
```

### 5. Crear las tablas de la base de datos

```bash
python -m database.crear_tablas
```

### 6. Ejecutar la aplicación

```bash
python main.py
```

---

## Uso del sistema

Al ejecutar la aplicación se abrirá la ventana principal. Inicia sesión con las credenciales de administrador (`admin` / `admin123`). 

El menú de navegación principal brinda acceso a todas las operaciones:
- Administrar productos.
- Gestionar categorías.
- Gestionar proveedores.
- Inventario.
- Registrar venta.
- Alertas de stock bajo.
- Reportes.
- Administrar usuarios.
- Realizar copia de seguridad.

---

## Arquitectura del sistema

El sistema está desarrollado y estructurado bajo una **Arquitectura de Tres Capas** para garantizar el orden y mantenibilidad del código:

```text
Capa de Presentación
(Pantallas en Tkinter, formularios, menú y validaciones visuales)
        ↓
Capa de Lógica de Negocio
(Reglas del sistema: ventas, entradas, alertas, usuarios y reportes)
        ↓
Capa de Acceso a Datos
(Consultas, altas, bajas y actualizaciones mediante Controladores)
        ↓
Base de Datos Relacional (SQLite)
```

---

## Integrantes del equipo

- Bernal Hernández Miguel Antonio
- Dominguez Favela Bryan Alexis
- Félix Rodríguez Luz Elena
- García Núñez Juan Pablo
- López Vázquez Jesús Fernando

---

## Nota

Este proyecto fue desarrollado con fines académicos para la asignatura de **Análisis y Diseño de Software** de la **Licenciatura en Informática**.

El sistema aún se encuentra en desarrollo, por lo que algunas funciones están planeadas o en proceso de integración.
