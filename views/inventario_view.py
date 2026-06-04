# ==============================
# VISTA DE INVENTARIO
# ==============================

"""
Vista para inventario.

Permite:
- Ver inventario actual.
- Registrar entradas.
- Registrar salidas.
- Guardar historial de movimientos.
- Registrar motivo del movimiento.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.inventario_controller import InventarioController


class InventarioView(tk.Toplevel):
    """
    Ventana para gestionar inventario.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.title("Inventario")
        self.geometry("1050x650")
        self.minsize(950, 600)
        self.configure(bg="#ecf0f1")

        self.usuario = usuario
        self.inventario_controller = InventarioController()
        self.productos = []

        self.crear_interfaz()
        self.cargar_productos()

    def obtener_id_usuario(self):
        if self.usuario is None:
            return 1
        if hasattr(self.usuario, "id_usuario"):
            return self.usuario.id_usuario
        if isinstance(self.usuario, dict):
            return self.usuario.get("id_usuario", 1)
        if isinstance(self.usuario, (tuple, list)) and len(self.usuario) > 0:
            return self.usuario[0]
        return 1

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Inventario",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_formulario = tk.LabelFrame(
            card,
            text="Movimiento de inventario",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_formulario.pack(fill="x", pady=(0, 15))

        tk.Label(frame_formulario, text="Producto:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=8)
        self.combo_productos = ttk.Combobox(frame_formulario, state="readonly", font=("Segoe UI", 10), width=50)
        self.combo_productos.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=8, ipady=4)

        tk.Label(frame_formulario, text="Cantidad:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=(0, 8), pady=8)
        self.entry_cantidad = tk.Entry(frame_formulario, font=("Segoe UI", 10), width=12)
        self.entry_cantidad.grid(row=0, column=3, sticky="w", padx=(0, 20), pady=8, ipady=4)
        self.entry_cantidad.insert(0, "1")

        tk.Label(frame_formulario, text="Ubicacion:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=8)
        self.entry_ubicacion = tk.Entry(frame_formulario, font=("Segoe UI", 10), width=50)
        self.entry_ubicacion.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=8, ipady=4)

        tk.Label(frame_formulario, text="Motivo:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, sticky="w", padx=(0, 8), pady=8)
        self.entry_motivo = tk.Entry(frame_formulario, font=("Segoe UI", 10), width=30)
        self.entry_motivo.grid(row=1, column=3, sticky="w", padx=(0, 20), pady=8, ipady=4)
        self.entry_motivo.insert(0, "Movimiento manual")

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Registrar entrada", "#27ae60", self.registrar_entrada).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Registrar salida", "#e74c3c", self.registrar_salida).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar tabla", "#34495e", self.cargar_productos).pack(side="left", padx=(0, 10))

        frame_tabla = tk.LabelFrame(
            card,
            text="Inventario actual",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "codigo", "nombre", "precio", "stock_minimo", "cantidad", "ubicacion")

        self.tabla_inventario = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        encabezados = {
            "id": "ID",
            "codigo": "Codigo",
            "nombre": "Nombre",
            "precio": "Precio",
            "stock_minimo": "Stock min.",
            "cantidad": "Cantidad",
            "ubicacion": "Ubicacion"
        }

        for columna, texto in encabezados.items():
            self.tabla_inventario.heading(columna, text=texto)

        self.tabla_inventario.column("id", width=60, anchor="center")
        self.tabla_inventario.column("codigo", width=120, anchor="center")
        self.tabla_inventario.column("nombre", width=280)
        self.tabla_inventario.column("precio", width=100, anchor="center")
        self.tabla_inventario.column("stock_minimo", width=100, anchor="center")
        self.tabla_inventario.column("cantidad", width=100, anchor="center")
        self.tabla_inventario.column("ubicacion", width=180)

        self.tabla_inventario.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_inventario.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_inventario.configure(yscrollcommand=scrollbar.set)

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
        self.productos = self.inventario_controller.listar_inventario()

        valores_combo = []
        for producto in self.productos:
            valores_combo.append(f"{producto[0]} - {producto[1]} | Stock: {producto[5]}")

        self.combo_productos["values"] = valores_combo

        for fila in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(fila)

        for producto in self.productos:
            self.tabla_inventario.insert(
                "",
                "end",
                values=(
                    producto[0],
                    producto[2],
                    producto[1],
                    f"${float(producto[3]):.2f}",
                    producto[4],
                    producto[5],
                    producto[6]
                )
            )

    def obtener_id_producto_seleccionado(self):
        seleccionado = self.combo_productos.get()
        if seleccionado == "":
            return None
        try:
            return int(seleccionado.split(" - ")[0])
        except ValueError:
            return None

    def obtener_cantidad(self):
        try:
            return int(self.entry_cantidad.get().strip())
        except ValueError:
            return None

    def registrar_entrada(self):
        id_producto = self.obtener_id_producto_seleccionado()
        cantidad = self.obtener_cantidad()
        ubicacion = self.entry_ubicacion.get().strip()
        motivo = self.entry_motivo.get().strip()

        if id_producto is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        if cantidad is None or cantidad <= 0:
            messagebox.showwarning("Aviso", "La cantidad debe ser mayor que cero.")
            return

        resultado, mensaje = self.inventario_controller.registrar_entrada(
            id_producto=id_producto,
            cantidad=cantidad,
            ubicacion=ubicacion,
            id_usuario=self.obtener_id_usuario(),
            motivo=motivo
        )

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def registrar_salida(self):
        id_producto = self.obtener_id_producto_seleccionado()
        cantidad = self.obtener_cantidad()
        motivo = self.entry_motivo.get().strip()

        if id_producto is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        if cantidad is None or cantidad <= 0:
            messagebox.showwarning("Aviso", "La cantidad debe ser mayor que cero.")
            return

        resultado, mensaje = self.inventario_controller.registrar_salida(
            id_producto=id_producto,
            cantidad=cantidad,
            id_usuario=self.obtener_id_usuario(),
            motivo=motivo
        )

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)


def abrir_inventario(parent=None, usuario=None):
    ventana = InventarioView(parent, usuario)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    InventarioView(root)
    root.mainloop()
