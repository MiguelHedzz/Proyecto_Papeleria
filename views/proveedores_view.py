# ==============================
# VISTA DE PROVEEDORES
# ==============================

"""
Vista para la gestión completa de proveedores.

Permite:
- Crear proveedor.
- Listar proveedores.
- Buscar por nombre.
- Seleccionar proveedor.
- Actualizar proveedor.
- Eliminar proveedor.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.proveedor_controller import ProveedorController


class ProveedoresView(tk.Toplevel):
    """
    Ventana de administración de proveedores.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.title("Proveedores")
        self.geometry("900x560")
        self.minsize(820, 520)
        self.configure(bg="#ecf0f1")

        self.proveedor_controller = ProveedorController()
        self.id_proveedor_seleccionado = None
        self.usuario = usuario

        self.crear_interfaz()
        self.cargar_proveedores()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Proveedores",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_form = tk.LabelFrame(
            card,
            text="Datos del proveedor",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(fill="x", pady=(0, 15))

        self.entry_nombre = self.crear_campo(frame_form, "Nombre:", 0, 0)
        self.entry_telefono = self.crear_campo(frame_form, "Teléfono:", 0, 2)
        self.entry_correo = self.crear_campo(frame_form, "Correo:", 1, 0)

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Agregar", "#e67e22", self.agregar_proveedor).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#e67e22", self.actualizar_proveedor).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Eliminar", "#e74c3c", self.eliminar_proveedor).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Limpiar", "#95a5a6", self.limpiar_formulario).pack(side="left", padx=(0, 10))

        frame_busqueda = tk.Frame(card, bg="white")
        frame_busqueda.pack(fill="x", pady=(0, 15))

        tk.Label(frame_busqueda, text="Buscar nombre:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        self.entry_buscar = tk.Entry(frame_busqueda, font=("Segoe UI", 10), width=25)
        self.entry_buscar.pack(side="left", padx=(0, 10), ipady=4)

        self.crear_boton(frame_busqueda, "Buscar", "#e67e22", self.buscar_proveedor).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_busqueda, "Mostrar todos", "#34495e", self.cargar_proveedores).pack(side="left", padx=(0, 10))

        frame_tabla = tk.LabelFrame(
            card,
            text="Proveedores registrados",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "telefono", "correo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("correo", text="Correo")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=240)
        self.tabla.column("telefono", width=160)
        self.tabla.column("correo", width=260)

        self.tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def crear_campo(self, parent, texto, fila, columna):
        tk.Label(
            parent,
            text=texto,
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 10, "bold")
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 8), pady=8)

        entry = tk.Entry(parent, font=("Segoe UI", 10), width=28)
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

    def cargar_proveedores(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        proveedores = self.proveedor_controller.listar_proveedores()

        for proveedor in proveedores:
            self.tabla.insert("", "end", values=proveedor)

        self.entry_buscar.delete(0, tk.END)

    def agregar_proveedor(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()

        if nombre == "":
            messagebox.showwarning("Aviso", "El nombre del proveedor es obligatorio.")
            return

        resultado, mensaje = self.proveedor_controller.registrar_proveedor(
            nombre, telefono, correo
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_proveedor(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")
        self.id_proveedor_seleccionado = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, valores[2])

        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, valores[3])

    def actualizar_proveedor(self):
        if self.id_proveedor_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un proveedor de la tabla.")
            return

        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()

        if nombre == "":
            messagebox.showwarning("Aviso", "El nombre del proveedor es obligatorio.")
            return

        resultado, mensaje = self.proveedor_controller.actualizar_proveedor(
            self.id_proveedor_seleccionado, nombre, telefono, correo
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_proveedor(self):
        if self.id_proveedor_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un proveedor de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este proveedor?"
        )

        if not confirmar:
            return

        resultado, mensaje = self.proveedor_controller.eliminar_proveedor(
            self.id_proveedor_seleccionado
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar_proveedor(self):
        nombre = self.entry_buscar.get().strip()

        if nombre == "":
            messagebox.showwarning("Aviso", "Ingresa un nombre para buscar.")
            return

        proveedores = self.proveedor_controller.buscar_por_nombre(nombre)

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for proveedor in proveedores:
            self.tabla.insert("", "end", values=proveedor)

    def limpiar_formulario(self):
        self.id_proveedor_seleccionado = None

        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(seleccion)


def abrir_proveedores(parent=None, usuario=None):
    ventana = ProveedoresView(parent, usuario)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ProveedoresView(root)
    root.mainloop()