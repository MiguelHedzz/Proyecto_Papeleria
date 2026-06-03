# ==============================
# VISTA DE REPORTES
# ==============================

"""
Vista para probar reportes.

Muestra:
- Resumen general.
- Inventario.
- Stock bajo.
- Ventas.
- Productos.

Ejecutar:
python -m views.reportes_view
"""

import os
import sys
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from database.conexion import conectar_bd


class VentanaReportes(tk.Toplevel):
    """
    Ventana de reportes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Reportes del Sistema")
        self.geometry("1100x680")
        self.minsize(980, 620)
        self.configure(bg="#ecf0f1")

        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Reportes del Sistema",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        self.frame_resumen = tk.Frame(card, bg="white")
        self.frame_resumen.pack(fill="x", pady=(0, 15))

        tk.Button(
            card,
            text="Actualizar reportes",
            bg="#e67e22",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.cargar_datos
        ).pack(anchor="w", pady=(0, 15))

        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill="both", expand=True)

        self.tab_inventario = tk.Frame(self.notebook, bg="white")
        self.tab_stock = tk.Frame(self.notebook, bg="white")
        self.tab_ventas = tk.Frame(self.notebook, bg="white")
        self.tab_productos = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_inventario, text="Inventario")
        self.notebook.add(self.tab_stock, text="Stock bajo")
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.notebook.add(self.tab_productos, text="Productos")

    def consulta(self, sql, parametros=()):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            datos = cursor.fetchall()
            conexion.close()
            return datos
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"No se pudo consultar la base de datos.\n\nDetalle: {error}")
            return []

    def limpiar_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def cargar_datos(self):
        self.cargar_resumen()
        self.cargar_inventario()
        self.cargar_stock_bajo()
        self.cargar_ventas()
        self.cargar_productos()

    def cargar_resumen(self):
        self.limpiar_frame(self.frame_resumen)

        total_productos = self.consulta("SELECT COUNT(*) FROM producto")[0][0]
        total_ventas = self.consulta("SELECT COUNT(*) FROM venta")[0][0]
        total_ingresos = self.consulta("SELECT IFNULL(SUM(total), 0) FROM venta")[0][0]
        stock_bajo = self.consulta("""
            SELECT COUNT(*)
            FROM producto p
            LEFT JOIN inventario i ON p.id_producto = i.id_producto
            WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
        """)[0][0]

        tarjetas = [
            ("Productos", total_productos, "#e67e22"),
            ("Ventas", total_ventas, "#27ae60"),
            ("Ingresos", f"${float(total_ingresos):.2f}", "#2c3e50"),
            ("Stock bajo", stock_bajo, "#e74c3c"),
        ]

        for titulo, valor, color in tarjetas:
            tarjeta = tk.Frame(self.frame_resumen, bg="#f8f9fa", relief="solid", bd=1, padx=15, pady=12)
            tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 12))

            tk.Label(tarjeta, text=titulo, bg="#f8f9fa", fg="#2c3e50", font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(tarjeta, text=str(valor), bg="#f8f9fa", fg=color, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(5, 0))

    def crear_tabla(self, parent, columnas, encabezados, anchos, datos):
        self.limpiar_frame(parent)

        tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=13)

        for columna in columnas:
            tabla.heading(columna, text=encabezados.get(columna, columna))
            tabla.column(columna, width=anchos.get(columna, 120), anchor="center" if columna in ("id", "codigo", "cantidad", "total") else "w")

        tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tabla.yview)
        scrollbar.pack(side="right", fill="y", pady=10)

        tabla.configure(yscrollcommand=scrollbar.set)

        for fila in datos:
            tabla.insert("", "end", values=fila)

    def cargar_inventario(self):
        datos = self.consulta("""
            SELECT
                p.id_producto,
                p.codigo,
                p.nombre,
                p.precio,
                p.stock_minimo,
                IFNULL(i.cantidad_actual, 0),
                IFNULL(i.ubicacion, '')
            FROM producto p
            LEFT JOIN inventario i ON p.id_producto = i.id_producto
            ORDER BY p.nombre ASC
        """)

        columnas = ("id", "codigo", "nombre", "precio", "stock_minimo", "cantidad", "ubicacion")
        encabezados = {
            "id": "ID",
            "codigo": "Código",
            "nombre": "Nombre",
            "precio": "Precio",
            "stock_minimo": "Stock mín.",
            "cantidad": "Cantidad",
            "ubicacion": "Ubicación"
        }
        anchos = {"id": 60, "codigo": 120, "nombre": 280, "precio": 100, "stock_minimo": 100, "cantidad": 100, "ubicacion": 180}

        self.crear_tabla(self.tab_inventario, columnas, encabezados, anchos, datos)

    def cargar_stock_bajo(self):
        datos = self.consulta("""
            SELECT
                p.id_producto,
                p.codigo,
                p.nombre,
                p.stock_minimo,
                IFNULL(i.cantidad_actual, 0),
                IFNULL(i.ubicacion, '')
            FROM producto p
            LEFT JOIN inventario i ON p.id_producto = i.id_producto
            WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
            ORDER BY p.nombre ASC
        """)

        columnas = ("id", "codigo", "nombre", "stock_minimo", "cantidad", "ubicacion")
        encabezados = {
            "id": "ID",
            "codigo": "Código",
            "nombre": "Nombre",
            "stock_minimo": "Stock mín.",
            "cantidad": "Cantidad",
            "ubicacion": "Ubicación"
        }
        anchos = {"id": 60, "codigo": 120, "nombre": 300, "stock_minimo": 120, "cantidad": 120, "ubicacion": 180}

        self.crear_tabla(self.tab_stock, columnas, encabezados, anchos, datos)

    def cargar_ventas(self):
        datos = self.consulta("""
            SELECT
                v.id_venta,
                v.fecha,
                v.total,
                IFNULL(u.nombre, '')
            FROM venta v
            LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
            ORDER BY v.fecha DESC
        """)

        columnas = ("id", "fecha", "total", "usuario")
        encabezados = {"id": "ID", "fecha": "Fecha", "total": "Total", "usuario": "Usuario"}
        anchos = {"id": 60, "fecha": 220, "total": 120, "usuario": 220}

        self.crear_tabla(self.tab_ventas, columnas, encabezados, anchos, datos)

    def cargar_productos(self):
        datos = self.consulta("""
            SELECT
                p.id_producto,
                p.codigo,
                p.nombre,
                p.precio,
                p.stock_minimo
            FROM producto p
            ORDER BY p.nombre ASC
        """)

        columnas = ("id", "codigo", "nombre", "precio", "stock_minimo")
        encabezados = {"id": "ID", "codigo": "Código", "nombre": "Nombre", "precio": "Precio", "stock_minimo": "Stock mín."}
        anchos = {"id": 60, "codigo": 120, "nombre": 320, "precio": 120, "stock_minimo": 120}

        self.crear_tabla(self.tab_productos, columnas, encabezados, anchos, datos)


def abrir_reportes(parent=None):
    ventana = VentanaReportes(parent)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaReportes(root)
    root.mainloop()
