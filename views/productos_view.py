# ==============================
# VISTA DE PRODUCTOS
# ==============================

"""
Vista para la gestión completa de productos.

Permite:
- Crear producto.
- Listar productos.
- Buscar producto por código.
- Seleccionar producto.
- Actualizar producto.
- Eliminar producto.
- Actualizar cantidad y ubicación de inventario.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.producto_controller import ProductoController


class ProductosView(tk.Toplevel):
    """
    Ventana de administración de productos.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.title("Productos")
        self.geometry("1120x680")
        self.minsize(1000, 620)
        self.configure(bg="#ecf0f1")

        self.producto_controller = ProductoController()
        self.id_producto_seleccionado = None
        self.id_categoria_actual = None
        self.id_proveedor_actual = None
        self.usuario = usuario

        self.crear_interfaz()
        self.cargar_productos()

    # ==============================
    # INTERFAZ
    # ==============================

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        titulo = tk.Label(
            contenedor,
            text="Productos",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        # Formulario
        frame_formulario = tk.LabelFrame(
            card,
            text="Datos del producto",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_formulario.pack(fill="x", pady=(0, 15))

        self.entry_codigo = self.crear_campo(frame_formulario, "Código:", 0, 0)
        self.entry_nombre = self.crear_campo(frame_formulario, "Nombre:", 0, 2)
        self.entry_precio = self.crear_campo(frame_formulario, "Precio:", 0, 4)

        self.entry_stock_minimo = self.crear_campo(frame_formulario, "Stock mínimo:", 1, 0)
        self.entry_cantidad = self.crear_campo(frame_formulario, "Cantidad:", 1, 2)
        self.entry_ubicacion = self.crear_campo(frame_formulario, "Ubicación:", 1, 4)

        # Botones
        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Agregar", "#e67e22", self.agregar_producto).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#e67e22", self.actualizar_producto).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Eliminar", "#e74c3c", self.eliminar_producto).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Limpiar", "#95a5a6", self.limpiar_formulario).pack(side="left", padx=(0, 10))

        # Búsqueda
        frame_busqueda = tk.Frame(card, bg="white")
        frame_busqueda.pack(fill="x", pady=(0, 15))

        tk.Label(
            frame_busqueda,
            text="Buscar por código:",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 8))

        self.entry_buscar = tk.Entry(frame_busqueda, font=("Segoe UI", 10), width=25)
        self.entry_buscar.pack(side="left", padx=(0, 10), ipady=4)

        self.crear_boton(frame_busqueda, "Buscar", "#e67e22", self.buscar_producto).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_busqueda, "Mostrar todos", "#34495e", self.cargar_productos).pack(side="left", padx=(0, 10))

        # Tabla
        frame_tabla = tk.LabelFrame(
            card,
            text="Productos registrados",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = (
            "id",
            "codigo",
            "nombre",
            "precio",
            "stock_minimo",
            "cantidad",
            "ubicacion"
        )

        self.tabla_productos = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        encabezados = {
            "id": "ID",
            "codigo": "Código",
            "nombre": "Nombre",
            "precio": "Precio",
            "stock_minimo": "Stock mín.",
            "cantidad": "Cantidad",
            "ubicacion": "Ubicación"
        }

        for columna, texto in encabezados.items():
            self.tabla_productos.heading(columna, text=texto)

        self.tabla_productos.column("id", width=60, anchor="center")
        self.tabla_productos.column("codigo", width=120, anchor="center")
        self.tabla_productos.column("nombre", width=260)
        self.tabla_productos.column("precio", width=100, anchor="center")
        self.tabla_productos.column("stock_minimo", width=100, anchor="center")
        self.tabla_productos.column("cantidad", width=100, anchor="center")
        self.tabla_productos.column("ubicacion", width=180)

        self.tabla_productos.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    def crear_campo(self, parent, texto, fila, columna):
        tk.Label(
            parent,
            text=texto,
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 8), pady=8)

        entry = tk.Entry(parent, font=("Segoe UI", 10), width=24)
        entry.grid(row=fila, column=columna + 1, sticky="w", padx=(0, 20), pady=8, ipady=4)
        return entry

    def crear_boton(self, parent, texto, color, comando):
        return tk.Button(
            parent,
            text=texto,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=14,
            height=2,
            command=comando
        )

    # ==============================
    # FUNCIONES CRUD
    # ==============================

    def obtener_datos(self):
        return {
            "codigo": self.entry_codigo.get().strip(),
            "nombre": self.entry_nombre.get().strip(),
            "precio": self.entry_precio.get().strip(),
            "stock_minimo": self.entry_stock_minimo.get().strip(),
            "cantidad": self.entry_cantidad.get().strip(),
            "ubicacion": self.entry_ubicacion.get().strip()
        }

    def cargar_productos(self):
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        productos = self.producto_controller.listar_productos()

        for producto in productos:
            cantidad = producto[7] if len(producto) > 7 else 0
            ubicacion = producto[8] if len(producto) > 8 else ""

            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto[0],
                    producto[2],
                    producto[1],
                    producto[3],
                    producto[4],
                    cantidad,
                    ubicacion
                )
            )

        self.entry_buscar.delete(0, tk.END)

    def agregar_producto(self):
        datos = self.obtener_datos()

        if datos["codigo"] == "" or datos["nombre"] == "" or datos["precio"] == "":
            messagebox.showwarning(
                "Campos requeridos",
                "Código, nombre y precio son obligatorios."
            )
            return

        if datos["stock_minimo"] == "":
            datos["stock_minimo"] = 0

        if datos["cantidad"] == "":
            datos["cantidad"] = 0

        resultado, mensaje = self.producto_controller.registrar_producto(
            nombre=datos["nombre"],
            codigo=datos["codigo"],
            precio=datos["precio"],
            stock_minimo=datos["stock_minimo"],
            cantidad_inicial=datos["cantidad"],
            ubicacion=datos["ubicacion"]
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_producto(self, event):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            return

        valores = self.tabla_productos.item(seleccion[0], "values")
        self.id_producto_seleccionado = valores[0]

        producto_completo = self.producto_controller.buscar_por_id(self.id_producto_seleccionado)
        if producto_completo:
            self.id_categoria_actual = producto_completo[5] if len(producto_completo) > 5 else None
            self.id_proveedor_actual = producto_completo[6] if len(producto_completo) > 6 else None

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[1])

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[2])

        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, valores[3])

        self.entry_stock_minimo.delete(0, tk.END)
        self.entry_stock_minimo.insert(0, valores[4])

        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, valores[5])

        self.entry_ubicacion.delete(0, tk.END)
        self.entry_ubicacion.insert(0, valores[6])

    def actualizar_producto(self):
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return

        datos = self.obtener_datos()

        if datos["codigo"] == "" or datos["nombre"] == "" or datos["precio"] == "":
            messagebox.showwarning(
                "Campos requeridos",
                "Código, nombre y precio son obligatorios."
            )
            return

        if datos["stock_minimo"] == "":
            datos["stock_minimo"] = 0

        if datos["cantidad"] == "":
            datos["cantidad"] = 0

        resultado, mensaje = self.producto_controller.actualizar_producto(
            id_producto=self.id_producto_seleccionado,
            nombre=datos["nombre"],
            codigo=datos["codigo"],
            precio=datos["precio"],
            stock_minimo=datos["stock_minimo"],
            id_categoria=self.id_categoria_actual,
            id_proveedor=self.id_proveedor_actual
        )

        if not resultado:
            messagebox.showerror("Error", mensaje)
            return

        resultado_inv, mensaje_inv = self.producto_controller.actualizar_inventario(
            id_producto=self.id_producto_seleccionado,
            nueva_cantidad=datos["cantidad"],
            nueva_ubicacion=datos["ubicacion"]
        )

        if resultado_inv:
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje_inv)

    def eliminar_producto(self):
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este producto?"
        )
        if not confirmar:
            return

        resultado, mensaje = self.producto_controller.eliminar_producto(self.id_producto_seleccionado)
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar_producto(self):
        codigo = self.entry_buscar.get().strip()
        if codigo == "":
            messagebox.showwarning("Aviso", "Ingresa un código para buscar.")
            return

        producto = self.producto_controller.buscar_por_codigo(codigo)

        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        if producto:
            cantidad = producto[7] if len(producto) > 7 else 0
            ubicacion = producto[8] if len(producto) > 8 else ""
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto[0],
                    producto[2],
                    producto[1],
                    producto[3],
                    producto[4],
                    cantidad,
                    ubicacion
                )
            )
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un producto con ese código.")

    def limpiar_formulario(self):
        self.id_producto_seleccionado = None
        self.id_categoria_actual = None
        self.id_proveedor_actual = None

        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock_minimo.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)

        seleccion = self.tabla_productos.selection()
        if seleccion:
            self.tabla_productos.selection_remove(seleccion)


def abrir_productos(parent=None, usuario=None):
    """
    Abre la ventana de productos.
    """
    ventana = ProductosView(parent, usuario)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ProductosView(root)
    root.mainloop()