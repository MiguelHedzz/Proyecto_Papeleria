# ==============================
# VISTA DE REPORTES
# ==============================

"""
Vista independiente de reportes.

Incluye:
- Stock bajo.
- Ventas.
- Productos.
- Movimientos de inventario.
- Productos mas vendidos.
- Exportacion basica a CSV.
"""

import os
import sys
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from services.reporte_service import ReporteService


class VentanaReportes(tk.Toplevel):
    """
    Ventana de reportes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Reportes del Sistema")
        self.geometry("1150x700")
        self.minsize(1020, 620)
        self.configure(bg="#ecf0f1")

        self.reporte_service = ReporteService()

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

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Exportar Stock Bajo CSV", "#3498db", lambda: self.exportar_csv("stock_bajo")).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Exportar Ventas CSV", "#3498db", lambda: self.exportar_csv("ventas")).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Exportar Productos CSV", "#3498db", lambda: self.exportar_csv("productos")).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#95a5a6", self.cargar_datos).pack(side="left", padx=(0, 10))

        self.frame_resumen = tk.Frame(card, bg="white")
        self.frame_resumen.pack(fill="x", pady=(0, 15))

        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill="both", expand=True)

        self.tab_stock = tk.Frame(self.notebook, bg="white")
        self.tab_ventas = tk.Frame(self.notebook, bg="white")
        self.tab_productos = tk.Frame(self.notebook, bg="white")
        self.tab_movimientos = tk.Frame(self.notebook, bg="white")
        self.tab_mas_vendidos = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_stock, text="Stock bajo")
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_movimientos, text="Movimientos")
        self.notebook.add(self.tab_mas_vendidos, text="Mas vendidos")

    def crear_boton(self, parent, texto, color, comando):
        return tk.Button(
            parent,
            text=texto,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            height=2,
            command=comando
        )

    def limpiar_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def obtener_valor(self, fila, clave, indice, default=""):
        try:
            return fila[clave]
        except Exception:
            try:
                return fila[indice]
            except Exception:
                return default

    def cargar_datos(self):
        self.cargar_resumen()
        self.cargar_stock_bajo()
        self.cargar_ventas()
        self.cargar_productos()
        self.cargar_movimientos()
        self.cargar_productos_mas_vendidos()

    def cargar_resumen(self):
        self.limpiar_frame(self.frame_resumen)
        resumen = self.reporte_service.resumen_general()

        tarjetas = [
            ("Productos", resumen.get("total_productos", 0), "#e67e22"),
            ("Ventas", resumen.get("total_ventas", 0), "#27ae60"),
            ("Ingresos", f"${float(resumen.get('total_ingresos', 0)):.2f}", "#2c3e50"),
            ("Stock bajo", resumen.get("productos_stock_bajo", 0), "#e74c3c"),
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
            anchor = "center" if columna in ("id", "codigo", "cantidad", "total", "stock_minimo", "precio") else "w"
            tabla.column(columna, width=anchos.get(columna, 120), anchor=anchor)

        tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tabla.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        tabla.configure(yscrollcommand=scrollbar.set)

        for fila in datos:
            tabla.insert("", "end", values=fila)

        return tabla

    def cargar_stock_bajo(self):
        datos = []
        for fila in self.reporte_service.reporte_stock_bajo():
            datos.append((
                self.obtener_valor(fila, "id_producto", 0),
                self.obtener_valor(fila, "nombre", 1),
                self.obtener_valor(fila, "codigo", 2),
                self.obtener_valor(fila, "stock_minimo", 3),
                self.obtener_valor(fila, "cantidad_actual", 4),
                self.obtener_valor(fila, "ubicacion", 5),
            ))

        columnas = ("id", "nombre", "codigo", "stock_minimo", "cantidad", "ubicacion")
        encabezados = {"id": "ID", "nombre": "Nombre", "codigo": "Codigo", "stock_minimo": "Stock min.", "cantidad": "Cantidad", "ubicacion": "Ubicacion"}
        anchos = {"id": 60, "nombre": 250, "codigo": 120, "stock_minimo": 100, "cantidad": 100, "ubicacion": 180}
        self.crear_tabla(self.tab_stock, columnas, encabezados, anchos, datos)

    def cargar_ventas(self):
        datos = []
        for fila in self.reporte_service.reporte_ventas():
            datos.append((
                self.obtener_valor(fila, "id_venta", 0),
                self.obtener_valor(fila, "fecha", 1),
                f"${float(self.obtener_valor(fila, 'total', 2, 0)):.2f}",
                self.obtener_valor(fila, "metodo_pago", 3),
                self.obtener_valor(fila, "usuario", 4),
            ))

        columnas = ("id", "fecha", "total", "metodo_pago", "usuario")
        encabezados = {"id": "ID", "fecha": "Fecha", "total": "Total", "metodo_pago": "Metodo pago", "usuario": "Usuario"}
        anchos = {"id": 60, "fecha": 220, "total": 120, "metodo_pago": 130, "usuario": 200}
        self.crear_tabla(self.tab_ventas, columnas, encabezados, anchos, datos)

    def cargar_productos(self):
        datos = []
        for fila in self.reporte_service.reporte_productos():
            datos.append((
                self.obtener_valor(fila, "id_producto", 0),
                self.obtener_valor(fila, "codigo", 2),
                self.obtener_valor(fila, "nombre", 1),
                f"${float(self.obtener_valor(fila, 'precio', 3, 0)):.2f}",
                self.obtener_valor(fila, "stock_minimo", 4),
                self.obtener_valor(fila, "cantidad_actual", 7),
                self.obtener_valor(fila, "categoria", 9),
                self.obtener_valor(fila, "proveedor", 10),
            ))

        columnas = ("id", "codigo", "nombre", "precio", "stock_minimo", "cantidad", "categoria", "proveedor")
        encabezados = {"id": "ID", "codigo": "Codigo", "nombre": "Nombre", "precio": "Precio", "stock_minimo": "Stock min.", "cantidad": "Cantidad", "categoria": "Categoria", "proveedor": "Proveedor"}
        anchos = {"id": 60, "codigo": 120, "nombre": 250, "precio": 100, "stock_minimo": 100, "cantidad": 100, "categoria": 150, "proveedor": 150}
        self.crear_tabla(self.tab_productos, columnas, encabezados, anchos, datos)

    def cargar_movimientos(self):
        datos = []
        for fila in self.reporte_service.reporte_movimientos():
            datos.append((
                self.obtener_valor(fila, "id_movimiento", 0),
                self.obtener_valor(fila, "producto", 1),
                self.obtener_valor(fila, "codigo", 2),
                self.obtener_valor(fila, "tipo_movimiento", 3),
                self.obtener_valor(fila, "cantidad", 4),
                self.obtener_valor(fila, "fecha", 5),
                self.obtener_valor(fila, "usuario", 6),
                self.obtener_valor(fila, "motivo", 7),
            ))

        columnas = ("id", "producto", "codigo", "tipo", "cantidad", "fecha", "usuario", "motivo")
        encabezados = {"id": "ID", "producto": "Producto", "codigo": "Codigo", "tipo": "Tipo", "cantidad": "Cantidad", "fecha": "Fecha", "usuario": "Usuario", "motivo": "Motivo"}
        anchos = {"id": 60, "producto": 220, "codigo": 100, "tipo": 100, "cantidad": 100, "fecha": 170, "usuario": 160, "motivo": 230}
        self.crear_tabla(self.tab_movimientos, columnas, encabezados, anchos, datos)

    def cargar_productos_mas_vendidos(self):
        datos = []
        for fila in self.reporte_service.reporte_productos_mas_vendidos():
            datos.append((
                self.obtener_valor(fila, "id_producto", 0),
                self.obtener_valor(fila, "codigo", 1),
                self.obtener_valor(fila, "nombre", 2),
                self.obtener_valor(fila, "cantidad_vendida", 3, 0),
                f"${float(self.obtener_valor(fila, 'total_vendido', 4, 0)):.2f}",
            ))

        columnas = ("id", "codigo", "nombre", "cantidad_vendida", "total_vendido")
        encabezados = {"id": "ID", "codigo": "Codigo", "nombre": "Nombre", "cantidad_vendida": "Cantidad vendida", "total_vendido": "Total vendido"}
        anchos = {"id": 60, "codigo": 120, "nombre": 300, "cantidad_vendida": 150, "total_vendido": 150}
        self.crear_tabla(self.tab_mas_vendidos, columnas, encabezados, anchos, datos)

    def exportar_csv(self, tipo):
        if tipo == "stock_bajo":
            datos = self.reporte_service.reporte_stock_bajo()
            encabezados = ["ID", "Nombre", "Codigo", "Stock minimo", "Cantidad", "Ubicacion"]
            filas = [[f[0], f[1], f[2], f[3], f[4], f[5]] for f in datos]
        elif tipo == "ventas":
            datos = self.reporte_service.reporte_ventas()
            encabezados = ["ID", "Fecha", "Total", "Metodo pago", "Usuario"]
            filas = [[f[0], f[1], f[2], f[3], f[4]] for f in datos]
        else:
            datos = self.reporte_service.reporte_productos()
            encabezados = ["ID", "Codigo", "Nombre", "Precio", "Stock minimo", "Cantidad", "Categoria", "Proveedor"]
            filas = [[f[0], f[2], f[1], f[3], f[4], f[7], f[9], f[10]] for f in datos]

        ruta = filedialog.asksaveasfilename(title="Guardar reporte CSV", defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
        if not ruta:
            return

        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(encabezados)
                escritor.writerows(filas)
            messagebox.showinfo("Exito", "Reporte exportado correctamente.")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo exportar el reporte.\n\nDetalle: {error}")


def abrir_reportes(parent=None):
    ventana = VentanaReportes(parent)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaReportes(root)
    root.mainloop()
