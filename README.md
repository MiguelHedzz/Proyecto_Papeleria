# Sistema de Inventario para Papelería Dunder Mifflin

Proyecto escolar desarrollado en **Python** para la asignatura de **Análisis y Diseño de Software** de la **Licenciatura en Informática**, con el objetivo de administrar el inventario de una papelería de forma sencilla, organizada y funcional.

El sistema permite controlar productos, categorías, proveedores, inventario, ventas, usuarios, alertas de stock bajo, reportes y respaldos de la base de datos local.

---

## Información del proyecto

**Nombre del proyecto:** Sistema de Inventario para Papelería Dunder Mifflin  
**Institución:** Universidad Autónoma de Sinaloa  
**Facultad:** Facultad de Informática de Culiacán  
**Carrera:** Licenciatura en Informática  
**Asignatura:** Análisis y Diseño de Software  
**Grupo:** 02-01  
**Tipo de proyecto:** Aplicación de escritorio con base de datos local

---

## Integrantes del equipo

- Bernal Hernández Miguel Antonio
- Dominguez Favela Bryan Alexis
- Félix Rodríguez Luz Elena
- García Núñez Juan Pablo
- López Vázquez Jesús Fernando

---

## Objetivo del proyecto

Desarrollar una aplicación que permita gestionar eficientemente el inventario de una papelería, proporcionando información actualizada y confiable para mejorar la administración, reducir errores manuales y facilitar la toma de decisiones.

---

## Descripción general

El proyecto busca reemplazar el control manual de inventario por un sistema de escritorio que permita registrar productos, controlar existencias, registrar entradas y salidas, realizar ventas, generar alertas cuando el stock llegue al mínimo y consultar reportes del sistema.

La aplicación está organizada en módulos para facilitar su uso y mantenimiento. Cada módulo cumple una función específica dentro del sistema.

---

## Funcionalidades principales

### Inicio de sesión

El sistema cuenta con una pantalla de login para validar el acceso mediante usuario y contraseña.

Usuario administrador de prueba:

```text
Usuario: admin
Contraseña: admin123
```

Roles principales:

- **Administrador:** acceso a productos, usuarios, categorías, proveedores, inventario, reportes, alertas y respaldos.
- **Vendedor:** acceso operativo para registrar ventas y consultar información permitida.

### Gestión de productos

Permite administrar el catálogo principal de artículos de la papelería.

Funciones disponibles:

- Registrar productos.
- Consultar productos.
- Buscar productos.
- Actualizar productos.
- Eliminar o desactivar productos.
- Asignar categoría.
- Asignar proveedor.
- Registrar stock mínimo.
- Registrar cantidad inicial en inventario.
- Definir ubicación del producto.

### Gestión de categorías

Permite organizar los productos por tipo o grupo.

Funciones disponibles:

- Registrar categorías.
- Consultar categorías.
- Actualizar categorías.
- Eliminar categorías.
- Relacionar categorías con productos.

### Gestión de proveedores

Permite registrar los datos principales de los proveedores que suministran productos.

Funciones disponibles:

- Registrar proveedores.
- Consultar proveedores.
- Actualizar proveedores.
- Eliminar proveedores.
- Relacionar proveedores con productos.

### Gestión de inventario

Permite controlar las existencias disponibles de cada producto.

Funciones disponibles:

- Registrar entradas de inventario.
- Registrar salidas de inventario.
- Actualizar existencias.
- Controlar ubicación de productos.
- Registrar historial de movimientos.
- Consultar movimientos de entrada, salida y ajustes.
- Verificar stock mínimo.

La existencia de un producto se calcula considerando entradas y salidas del inventario.

### Registro de ventas

Permite realizar ventas de productos disponibles en inventario.

Funciones disponibles:

- Buscar productos para venta.
- Agregar productos al carrito.
- Capturar cantidad vendida.
- Validar existencia disponible.
- Calcular subtotal por producto.
- Calcular total de venta.
- Registrar método de pago.
- Guardar venta.
- Guardar detalle de venta.
- Descontar automáticamente el inventario.
- Generar comprobante o ticket básico.
- Registrar movimiento de salida en inventario.
- Generar alerta si la venta deja el producto en stock bajo.

### Alertas de stock bajo

El sistema genera alertas cuando la cantidad disponible de un producto es menor o igual al stock mínimo definido.

Funciones disponibles:

- Generar alertas automáticas.
- Consultar productos con inventario bajo.
- Ver mensaje de alerta.
- Registrar fecha de alerta.
- Marcar alertas como atendidas.

### Reportes

El sistema permite consultar información importante para la administración de la papelería.

Reportes disponibles:

- Inventario actual.
- Productos registrados.
- Productos con stock bajo.
- Ventas realizadas.
- Movimientos de inventario.
- Productos más vendidos.
- Resumen general del sistema.
- Ingresos registrados por ventas.

También se incluye exportación básica de reportes en formato CSV.

### Administración de usuarios

Permite al administrador gestionar los usuarios que acceden al sistema.

Funciones disponibles:

- Registrar usuarios.
- Consultar usuarios.
- Actualizar usuarios.
- Cambiar rol.
- Activar usuarios.
- Desactivar usuarios.
- Controlar acceso según rol.

### Respaldos del sistema

Permite crear copias de seguridad de la base de datos local.

Funciones disponibles:

- Crear respaldo automático.
- Elegir carpeta de destino.
- Guardar la ruta del respaldo.
- Registrar fecha y hora del respaldo.
- Consultar historial de respaldos.
- Restaurar respaldo desde archivo `.db`.

---

## Requisitos funcionales cubiertos

| Clave | Requisito | Estado |
|---|---|---|
| RF01 | Administración de productos mediante CRUD | Implementado |
| RF02 | Consultas y búsquedas de productos | Implementado |
| RF03 | Gestión de categorías de productos | Implementado |
| RF04 | Registro de entradas al inventario | Implementado |
| RF05 | Realizar y consultar ventas con vendedor y total | Implementado |
| RF06 | Generación de alertas de stock mínimo | Implementado |
| RF07 | Reportes de inventario, ventas y movimientos | Implementado |
| RF08 | Inicio de sesión con usuario y contraseña | Implementado |
| RF09 | Administración de usuarios y roles | Implementado |
| RF10 | Copia de seguridad del sistema | Implementado |
| RF11 | Exportación básica de reportes | Implementado en CSV |

---

## Requisitos no funcionales

| Requisito | Descripción |
|---|---|
| Usabilidad | La interfaz está diseñada para ser sencilla y entendible para usuarios sin experiencia técnica. |
| Seguridad | El acceso se realiza mediante usuario y contraseña, con control básico de roles. |
| Organización | El código se encuentra separado por carpetas y responsabilidades. |
| Mantenimiento | Los módulos pueden modificarse de forma independiente. |
| Desempeño | Las consultas básicas de productos, inventario y ventas responden de forma rápida en un entorno local. |
| Disponibilidad | Al ser una aplicación local, depende del equipo donde se ejecute y de la base de datos SQLite. |

---

## Tecnologías utilizadas

- **Python:** lenguaje principal del proyecto.
- **SQLite:** base de datos local.
- **Tkinter:** interfaz gráfica de escritorio.
- **Visual Studio Code:** editor de código.
- **Git:** control de versiones.
- **GitHub:** repositorio del proyecto.

---

## Arquitectura del sistema

El sistema utiliza una arquitectura organizada por capas:

```text
Capa de presentación
Pantallas, formularios, botones y tablas creadas con Tkinter.
        ↓
Capa de lógica de negocio
Servicios y reglas del sistema: ventas, inventario, alertas, reportes y respaldos.
        ↓
Capa de acceso a datos
Controladores que consultan, registran, actualizan y eliminan información.
        ↓
Base de datos
SQLite almacena usuarios, productos, inventario, ventas, alertas y respaldos.
```

Esta separación permite que el sistema sea más fácil de mantener, corregir y ampliar.

---

## Estructura del proyecto

```text
Proyecto_Papeleria/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── estilos.py
│   └── logo.png
│
├── controllers/
│   ├── alerta_controller.py
│   ├── categoria_controller.py
│   ├── inventario_controller.py
│   ├── producto_controller.py
│   ├── proveedor_controller.py
│   ├── reporte_controller.py
│   ├── respaldo_controller.py
│   ├── usuario_controller.py
│   └── venta_controller.py
│
├── database/
│   ├── conexion.py
│   ├── crear_tablas.py
│   └── inventario.db
│
├── models/
│   ├── alerta.py
│   ├── categoria.py
│   ├── detalle_venta.py
│   ├── inventario.py
│   ├── producto.py
│   ├── proveedor.py
│   ├── reporte.py
│   ├── respaldo.py
│   ├── usuario.py
│   └── venta.py
│
├── services/
│   ├── auth_service.py
│   ├── inventario_service.py
│   ├── reporte_service.py
│   ├── venta_service.py
│   └── __init__.py
│
├── utils/
│   ├── exportar.py
│   ├── mensajes.py
│   ├── validaciones.py
│   └── __init__.py
│
└── views/
    ├── alertas_view.py
    ├── categorias_view.py
    ├── inventario_view.py
    ├── layout_view.py
    ├── login_view.py
    ├── menu_view.py
    ├── productos_view.py
    ├── proveedores_view.py
    ├── reportes_view.py
    ├── respaldos_view.py
    ├── usuarios_view.py
    └── ventas_view.py
```

---

## Explicación de carpetas

| Carpeta / archivo | Descripción |
|---|---|
| `main.py` | Archivo principal que inicia la aplicación. |
| `database/` | Contiene la conexión con SQLite y la creación de tablas. |
| `models/` | Define las clases principales del sistema. |
| `controllers/` | Contiene las operaciones sobre la base de datos. |
| `services/` | Contiene reglas de negocio más completas. |
| `views/` | Contiene las interfaces gráficas desarrolladas con Tkinter. |
| `utils/` | Contiene funciones auxiliares, validaciones, mensajes y exportación. |
| `assets/` | Contiene recursos visuales como estilos e imágenes. |

---

## Modelos principales

| Modelo | Descripción |
|---|---|
| Usuario | Representa al administrador o vendedor que accede al sistema. |
| Producto | Contiene la información de los artículos de papelería. |
| Categoria | Agrupa productos según su tipo. |
| Proveedor | Guarda datos básicos del proveedor. |
| Inventario | Controla la cantidad actual y ubicación de cada producto. |
| Venta | Registra las ventas realizadas por los usuarios. |
| DetalleVenta | Guarda los productos incluidos en una venta. |
| Alerta | Registra avisos cuando el stock llega al mínimo. |
| Reporte | Permite consultar información del inventario, ventas y movimientos. |
| Respaldo | Representa las copias de seguridad del sistema. |

---

## Base de datos

El sistema utiliza una base de datos local SQLite ubicada en:

```text
database/inventario.db
```

La base de datos se crea automáticamente al ejecutar:

```bash
python -m database.crear_tablas
```

### Tablas principales

| Tabla | Propósito |
|---|---|
| `usuario` | Guarda los datos de acceso y rol de cada usuario. |
| `categoria` | Clasifica los productos de la papelería. |
| `proveedor` | Registra información básica de los proveedores. |
| `producto` | Almacena datos generales de cada artículo. |
| `inventario` | Controla existencia actual y ubicación del producto. |
| `venta` | Registra ventas realizadas por los usuarios. |
| `detalle_venta` | Guarda productos, cantidades, precios y subtotales de cada venta. |
| `alerta` | Registra alertas generadas por stock bajo. |
| `respaldo` | Guarda historial de copias de seguridad. |
| `movimiento_inventario` | Registra entradas, salidas y ajustes del inventario. |

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

Si PowerShell marca error de permisos, ejecutar:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego activar nuevamente:

```bash
.\venv\Scripts\Activate.ps1
```

### 5. Instalar dependencias

El proyecto utiliza principalmente librerías incluidas con Python. Si existe un archivo `requirements.txt`, puede ejecutarse:

```bash
pip install -r requirements.txt
```

### 6. Crear tablas de la base de datos

```bash
python -m database.crear_tablas
```

### 7. Ejecutar la aplicación

```bash
python main.py
```

---

## Uso básico del sistema

1. Ejecutar la aplicación con `python main.py`.
2. Iniciar sesión con el usuario administrador.
3. Entrar al menú principal.
4. Registrar categorías y proveedores.
5. Registrar productos con código, nombre, precio, stock mínimo, categoría, proveedor, cantidad inicial y ubicación.
6. Registrar entradas o salidas de inventario cuando sea necesario.
7. Realizar ventas desde el módulo de ventas.
8. Revisar alertas de stock bajo.
9. Consultar reportes de inventario, ventas, movimientos y productos más vendidos.
10. Crear respaldos desde el módulo de respaldos.

---

## Comandos de prueba por módulo

Estos comandos permiten abrir vistas específicas para probar módulos de forma independiente:

```bash
python -m views.productos_view
python -m views.inventario_view
python -m views.categorias_view
python -m views.proveedores_view
python -m views.ventas_view
python -m views.alertas_view
python -m views.reportes_view
python -m views.usuarios_view
python -m views.respaldos_view
```

---

## Reglas principales del sistema

- No se puede vender un producto sin existencia suficiente.
- Al registrar una venta, el inventario se descuenta automáticamente.
- Al registrar entrada o salida de inventario, se guarda el movimiento.
- Si el stock queda menor o igual al mínimo, se genera una alerta.
- Solo el administrador puede gestionar usuarios, respaldos y reportes administrativos.
- Los productos se relacionan con categoría, proveedor e inventario.
- Cada venta se relaciona con un usuario y con uno o varios detalles de venta.

---

## Relación con el diseño de Figma

El diseño visual del sistema se basó en un prototipo de Figma. La interfaz contempla pantallas de:

- Inicio de sesión.
- Menú principal.
- Registro de venta.
- Gestión de productos.
- Reportes.
- Soporte.
- Administración de usuarios.
- Módulos administrativos.

---

## Estado final del proyecto

El proyecto se encuentra en una versión funcional para entrega académica.

Cuenta con:

- Login funcional.
- Menú principal.
- Control básico de roles.
- CRUD de productos.
- Gestión de categorías.
- Gestión de proveedores.
- Gestión de inventario.
- Registro de ventas.
- Alertas de stock bajo.
- Reportes de inventario, ventas, movimientos y productos más vendidos.
- Administración de usuarios.
- Respaldos de base de datos.
- Base de datos SQLite estructurada.
- Organización por capas y carpetas.

---

## Notas importantes

- La base de datos se crea automáticamente si no existe.
- El archivo `database/inventario.db` contiene la información local del sistema.
- Los respaldos se guardan como archivos `.db`.
- El proyecto está orientado a uso académico y puede ampliarse en el futuro.
- Para una versión productiva real, se recomienda mejorar la seguridad de contraseñas con hash y agregar control más estricto de permisos.

---

## Conclusión

El sistema de inventario para papelería Dunder Mifflin cumple con los módulos principales definidos en la documentación: productos, categorías, proveedores, inventario, ventas, alertas, reportes, usuarios y respaldos. Su estructura por capas permite separar la interfaz, la lógica de negocio y el acceso a datos, facilitando el mantenimiento del proyecto y su posible crecimiento.
