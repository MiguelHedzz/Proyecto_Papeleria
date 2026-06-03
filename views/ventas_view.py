# ==============================
# VISTA DE VENTAS
# ==============================

"""
Vista para probar ventas de forma independiente.

Permite:
- Seleccionar productos reales.
- Agregar productos al carrito.
- Confirmar venta.
- Descontar inventario.
- Ver ventas registradas.

Ejecutar:
python -m views.ventas_view
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.producto_controller import ProductoController
from controllers.inventario_controller import InventarioController
from controllers.venta_controller import VentaController


class VentanaVentas(tk.Toplevel):
    """
    Ventana de prueba de ventas.
    """

    def __init__(self, parent=None, id_usuario=1):
        super().__init__(parent)

        self.title("Prueba Ventas")
        self.geometry("1050x680")
        self.minsize(950, 620)
        self.configure(bg="#ecf0f1")

        self.id_usuario = id_usuario
        self.producto_controller = ProductoController()
        self.inventario_controller = InventarioController()
        self.venta_controller = VentaController()

        self.productos = []
        self.carrito = []
        self.total = 0.0

        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_ventas()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Registrar Venta",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_form = tk.LabelFrame(
            card,
            text="Agregar producto a la venta",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(fill="x", pady=(0, 15))

        tk.Label(frame_form, text="Producto:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=8)

        self.combo_producto = ttk.Combobox(frame_form, state="readonly", font=("Segoe UI", 10), width=55)
        self.combo_producto.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=8)

        tk.Label(frame_form, text="Cantidad:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 8), pady=8)

        self.entry_cantidad = tk.Entry(frame_form, font=("Segoe UI", 10), width=10)
        self.entry_cantidad.grid(row=0, column=3, sticky="w", padx=(0, 20), pady=8, ipady=4)
        self.entry_cantidad.insert(0, "1")

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Agregar al carrito", "#e67e22", self.agregar_al_carrito).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Confirmar venta", "#27ae60", self.confirmar_venta).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Limpiar carrito", "#95a5a6", self.limpiar_carrito).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar productos", "#34495e", self.cargar_productos).pack(side="left", padx=(0, 10))

        frame_carrito = tk.LabelFrame(
            card,
            text="Carrito de venta",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_carrito.pack(fill="x", pady=(0, 15))

        columnas_carrito = ("id_producto", "producto", "cantidad", "precio", "subtotal")
        self.tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas_carrito, show="headings", height=5)

        self.tabla_carrito.heading("id_producto", text="ID")
        self.tabla_carrito.heading("producto", text="Producto")
        self.tabla_carrito.heading("cantidad", text="Cantidad")
        self.tabla_carrito.heading("precio", text="Precio")
        self.tabla_carrito.heading("subtotal", text="Subtotal")

        self.tabla_carrito.column("id_producto", width=60, anchor="center")
        self.tabla_carrito.column("producto", width=320)
        self.tabla_carrito.column("cantidad", width=100, anchor="center")
        self.tabla_carrito.column("precio", width=100, anchor="center")
        self.tabla_carrito.column("subtotal", width=120, anchor="center")

        self.tabla_carrito.pack(fill="x")

        self.lbl_total = tk.Label(
            card,
            text="Total: $0.00",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 16, "bold")
        )
        self.lbl_total.pack(anchor="e", pady=(0, 15))

        frame_ventas = tk.LabelFrame(
            card,
            text="Ventas registradas",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_ventas.pack(fill="both", expand=True)

        columnas_ventas = ("id", "fecha", "total", "usuario")
        self.tabla_ventas = ttk.Treeview(frame_ventas, columns=columnas_ventas, show="headings", height=8)

        self.tabla_ventas.heading("id", text="ID")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("total", text="Total")
        self.tabla_ventas.heading("usuario", text="Usuario")

        self.tabla_ventas.column("id", width=60, anchor="center")
        self.tabla_ventas.column("fecha", width=220)
        self.tabla_ventas.column("total", width=120, anchor="center")
        self.tabla_ventas.column("usuario", width=180)

        self.tabla_ventas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_ventas, orient="vertical", command=self.tabla_ventas.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)

    def crear_boton(self, parent, texto, color, comando):
        return tk.Button(
            parent,
            text=texto,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=comando
        )

    def cargar_productos(self):
        self.productos = self.producto_controller.listar_productos()

        valores = []
        for producto in self.productos:
            cantidad = producto[7] if len(producto) > 7 else 0
            valores.append(f"{producto[0]} - {producto[1]} | ${producto[3]} | Stock: {cantidad}")

        self.combo_producto["values"] = valores

    def obtener_producto_seleccionado(self):
        seleccionado = self.combo_producto.get()

        if seleccionado == "":
            return None

        try:
            id_producto = int(seleccionado.split(" - ")[0])
        except ValueError:
            return None

        for producto in self.productos:
            if int(producto[0]) == id_producto:
                return producto

        return None

    def agregar_al_carrito(self):
        producto = self.obtener_producto_seleccionado()

        if producto is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        try:
            cantidad = int(self.entry_cantidad.get().strip())
        except ValueError:
            messagebox.showwarning("Aviso", "La cantidad debe ser un número entero.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Aviso", "La cantidad debe ser mayor que cero.")
            return

        stock = producto[7] if len(producto) > 7 else 0

        if cantidad > stock:
            messagebox.showwarning("Stock insuficiente", "No hay suficiente stock.")
            return

        id_producto = producto[0]
        nombre = producto[1]
        precio = float(producto[3])
        subtotal = cantidad * precio

        self.carrito.append({
            "id_producto": id_producto,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal
        })

        self.total += subtotal

        self.tabla_carrito.insert(
            "",
            "end",
            values=(id_producto, nombre, cantidad, f"${precio:.2f}", f"${subtotal:.2f}")
        )

        self.lbl_total.config(text=f"Total: ${self.total:.2f}")

    def confirmar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El carrito está vacío.")
            return

        resultado, mensaje, id_venta = self.venta_controller.registrar_venta(
            total=self.total,
            id_usuario=self.id_usuario
        )

        if not resultado:
            messagebox.showerror("Error", mensaje)
            return

        for item in self.carrito:
            resultado_detalle, mensaje_detalle = self.venta_controller.registrar_detalle_venta(
                id_venta=id_venta,
                id_producto=item["id_producto"],
                cantidad=item["cantidad"],
                subtotal=item["subtotal"],
                precio_unitario=item["precio"]
            )

            if not resultado_detalle:
                messagebox.showerror("Error", mensaje_detalle)
                return

            resultado_salida, mensaje_salida = self.inventario_controller.registrar_salida(
                item["id_producto"],
                item["cantidad"]
            )

            if not resultado_salida:
                messagebox.showerror("Error", mensaje_salida)
                return

        messagebox.showinfo("Éxito", f"Venta registrada correctamente. Total: ${self.total:.2f}")
        self.limpiar_carrito()
        self.cargar_productos()
        self.cargar_ventas()

    def limpiar_carrito(self):
        self.carrito = []
        self.total = 0.0

        for fila in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(fila)

        self.lbl_total.config(text="Total: $0.00")
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")

    def cargar_ventas(self):
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        ventas = self.venta_controller.obtener_ventas()

        for venta in ventas:
            if len(venta) >= 5:
                valores = (venta[0], venta[1], venta[2], venta[4])
            else:
                valores = (venta[0], venta[1], venta[2], "")
            self.tabla_ventas.insert("", "end", values=valores)


def abrir_ventas(parent=None):
    ventana = VentanaVentas(parent)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaVentas(root)
    root.mainloop()
