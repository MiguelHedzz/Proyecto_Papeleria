# Sistema de Inventario para Papelería

Proyecto escolar desarrollado en **Python** con el objetivo de administrar el inventario de una papelería de manera sencilla, organizada y funcional.

El sistema está diseñado para manejar productos, inventario, usuarios, ventas, alertas de stock bajo y reportes básicos. Actualmente se encuentra en una etapa inicial de implementación, con la estructura principal del proyecto, base de datos, login básico y controlador CRUD para productos.

---

## Objetivo del proyecto

Desarrollar un sistema de inventario que facilite el control de productos dentro de una papelería, permitiendo registrar artículos, consultar existencias, controlar entradas y salidas, registrar ventas y apoyar la toma de decisiones mediante reportes.

---

## Descripción general del sistema

El sistema busca reemplazar el control manual de inventario por una aplicación sencilla que permita administrar la información de forma más ordenada.

El proyecto contempla los siguientes módulos:

- Inicio de sesión.
- Registro de usuarios.
- Administración de productos.
- Gestión de categorías.
- Gestión de proveedores.
- Control de inventario.
- Registro de ventas.
- Alertas de stock bajo.
- Reportes básicos.

---

## Tecnologías utilizadas

- Python
- SQLite
- Tkinter
- Visual Studio Code
- Git
- GitHub

---

## Estado actual del proyecto

El proyecto se encuentra en desarrollo.

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

La clase seleccionada para el formulario CRUD es **Producto**.

Actualmente el controlador de productos permite:

- Registrar productos.
- Listar productos.
- Buscar productos por código.
- Actualizar información de productos.
- Eliminar productos.
- Crear inventario inicial al registrar un producto.

---

## Funcionalidades pendientes

Todavía falta completar:

- Pantalla visual completa para productos.
- Registro visual de usuarios.
- Módulo completo de ventas.
- Módulo completo de inventario.
- Alertas funcionales de stock bajo.
- Reportes básicos.
- Conectar las vistas con los controladores.
- Adaptar la interfaz al diseño realizado en Figma.

---

## Estructura del proyecto

```text
Proyecto_Papeleria/
│
├── main.py
├── README.md
├── requirements.txt
│
├── database/
│   ├── __init__.py
│   ├── conexion.py
│   └── crear_tablas.py
│
├── models/
│   ├── __init__.py
│   ├── usuario.py
│   ├── producto.py
│   ├── categoria.py
│   ├── proveedor.py
│   ├── inventario.py
│   ├── venta.py
│   ├── detalle_venta.py
│   ├── alerta.py
│   └── reporte.py
│
├── controllers/
│   ├── __init__.py
│   └── producto_controller.py
│
├── services/
│
├── utils/
│
├── views/
│
└── assets/
```

---

## Explicación de carpetas

| Carpeta / archivo | Descripción |
|---|---|
| `main.py` | Archivo principal que inicia la aplicación |
| `database/` | Contiene la conexión con SQLite y la creación de tablas |
| `models/` | Contiene las clases principales del sistema |
| `controllers/` | Contiene la lógica para manejar operaciones como registrar o consultar productos |
| `services/` | Carpeta pensada para reglas de negocio más específicas |
| `utils/` | Carpeta pensada para funciones auxiliares como validaciones o mensajes |
| `views/` | Carpeta donde se colocarán las pantallas del sistema |
| `assets/` | Carpeta para imágenes, íconos o recursos visuales |

---

## Modelos principales

El sistema contempla los siguientes modelos:

| Modelo | Descripción |
|---|---|
| Usuario | Representa a los usuarios que ingresan al sistema |
| Producto | Representa los artículos de papelería |
| Categoría | Clasifica los productos por tipo |
| Proveedor | Representa a quienes suministran productos |
| Inventario | Controla existencias y ubicación de productos |
| Venta | Registra las ventas realizadas |
| DetalleVenta | Guarda los productos incluidos en una venta |
| Alerta | Registra avisos de stock bajo |
| Reporte | Representa consultas o reportes del sistema |

---

## Base de datos

El sistema utiliza una base de datos local en SQLite.

Tablas principales:

| Tabla | Propósito |
|---|---|
| usuario | Guarda usuarios, contraseñas y roles |
| categoria | Guarda las categorías de productos |
| proveedor | Guarda información de proveedores |
| producto | Guarda los datos de los productos |
| inventario | Guarda existencias y ubicación de productos |
| venta | Guarda ventas realizadas |
| detalle_venta | Guarda los productos vendidos en cada venta |
| alerta | Guarda alertas de stock bajo |

---

## Requisitos funcionales principales

| Clave | Requisito |
|---|---|
| RF01 | Administración de productos mediante CRUD |
| RF04 | Registro de entradas al inventario |
| RF05 | Realizar y consultar ventas |
| RF06 | Generación de alertas de stock mínimo |
| RF08 | Inicio de sesión con usuario y contraseña |

---

## Requisitos técnicos

Para ejecutar el proyecto se necesita:

- Python instalado.
- Visual Studio Code.
- Git, en caso de trabajar con repositorio.
- Sistema operativo Windows.

Hasta el avance actual, el proyecto no requiere librerías externas obligatorias, ya que utiliza módulos incluidos en Python como:

- `sqlite3`
- `tkinter`

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
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

Al ejecutar la aplicación se abre la ventana principal del sistema.

Para iniciar sesión se puede usar el usuario administrador de prueba:

```text
Usuario: admin
Contraseña: admin123
```

Después de iniciar sesión, el sistema muestra un menú principal con las opciones principales:

- Administrar productos.
- Gestionar categorías.
- Gestionar proveedores.
- Inventario.
- Registrar venta.
- Alertas de stock bajo.
- Reportes.
- Administrar usuarios.

---

## CRUD seleccionado

Para esta etapa del proyecto se seleccionó la clase **Producto** como formulario CRUD principal.

El CRUD de productos permitirá:

- Crear un nuevo producto.
- Consultar productos registrados.
- Buscar productos por código.
- Actualizar datos de un producto.
- Eliminar productos.
- Registrar cantidad inicial en inventario.

Campos principales del producto:

```text
id_producto
nombre
codigo
precio
stock_minimo
id_categoria
id_proveedor
```

---

## Arquitectura del sistema

El sistema se organiza con una arquitectura sencilla por capas:

```text
Interfaz de usuario
        ↓
Controladores
        ↓
Modelos / Servicios
        ↓
Base de datos SQLite
```

Esta estructura permite separar la parte visual, la lógica del sistema y el almacenamiento de datos.


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
