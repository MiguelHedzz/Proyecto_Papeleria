# Sistema de Inventario para Papelería

Proyecto escolar desarrollado en **Python** con el objetivo de administrar el inventario de una papelería de manera sencilla y organizada.

El sistema permite manejar productos, inventario, usuarios, ventas, alertas de stock bajo y reportes básicos.

---

## Objetivo del proyecto

Desarrollar un sistema de inventario que facilite el control de productos dentro de una papelería, permitiendo registrar artículos, consultar existencias, controlar entradas y salidas, y apoyar la toma de decisiones mediante reportes.

---

## Tecnologías utilizadas

- Python
- SQLite
- Tkinter
- Visual Studio Code
- Git / GitHub

---

## Estructura inicial del proyecto

```text
Proyecto_Papeleria/
│
├── main.py
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
│   └── inventario.py
│
└── controllers/
    ├── __init__.py
    └── producto_controller.py
