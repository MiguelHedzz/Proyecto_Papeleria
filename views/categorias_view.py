# ==============================
# VISTA DE CATEGORÍAS
# ==============================

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.categoria_controller import CategoriaController


class CategoriasView(tk.Toplevel):
    """
    Ventana de administración de categorías.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)
        self.title("Categorías")
        self.geometry("850x560")
        self.minsize(780, 520)
        self.configure(bg="#ecf0f1")

        self.categoria_controller = CategoriaController()
        self.id_categoria_seleccionada = None
        self.usuario = usuario

        self.crear_interfaz()
        self.cargar_categorias()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        titulo = tk.Label(
            contenedor,
            text="Categorías",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_form = tk.LabelFrame(
            card,
            text="Datos de la categoría",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(fill="x", pady=(0, 15))

        tk.Label(frame_form, text="Nombre:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=8)
        self.entry_nombre = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.entry_nombre.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=8, ipady=4)

        tk.Label(frame_form, text="Descripción:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="nw", padx=(0, 8), pady=8)
        self.txt_descripcion = tk.Text(frame_form, font=("Segoe UI", 10), width=55, height=4)
        self.txt_descripcion.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=8)

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Agregar", "#e67e22", self.agregar_categoria).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#e67e22", self.actualizar_categoria).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Eliminar", "#e74c3c", self.eliminar_categoria).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Limpiar", "#95a5a6", self.limpiar_formulario).pack(side="left", padx=(0, 10))

        frame_busqueda = tk.Frame(card, bg="white")
        frame_busqueda.pack(fill="x", pady=(0, 15))

        tk.Label(frame_busqueda, text="Buscar nombre:", bg="white", fg="#2c3e50", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        self.entry_buscar = tk.Entry(frame_busqueda, font=("Segoe UI", 10), width=25)
        self.entry_buscar.pack(side="left", padx=(0, 10), ipady=4)

        self.crear_boton(frame_busqueda, "Buscar", "#e67e22", self.buscar_categoria).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_busqueda, "Mostrar todos", "#34495e", self.cargar_categorias).pack(side="left", padx=(0, 10))

        frame_tabla = tk.LabelFrame(
            card,
            text="Categorías registradas",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "descripcion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("descripcion", text="Descripción")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=220)
        self.tabla.column("descripcion", width=420)

        self.tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_categoria)

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

    def obtener_descripcion(self):
        return self.txt_descripcion.get("1.0", tk.END).strip()

    def cargar_categorias(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        categorias = self.categoria_controller.listar_categorias()
        for categoria in categorias:
            self.tabla.insert("", "end", values=categoria)
        self.entry_buscar.delete(0, tk.END)

    def agregar_categoria(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.obtener_descripcion()

        if not nombre:
            messagebox.showwarning("Aviso", "El nombre es obligatorio.")
            return

        resultado, mensaje = self.categoria_controller.registrar_categoria(nombre, descripcion)
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_categoria(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")
        self.id_categoria_seleccionada = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.txt_descripcion.delete("1.0", tk.END)
        self.txt_descripcion.insert("1.0", valores[2])

    def actualizar_categoria(self):
        if not self.id_categoria_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una categoría.")
            return

        nombre = self.entry_nombre.get().strip()
        descripcion = self.obtener_descripcion()

        if not nombre:
            messagebox.showwarning("Aviso", "El nombre es obligatorio.")
            return

        resultado, mensaje = self.categoria_controller.actualizar_categoria(
            self.id_categoria_seleccionada, nombre, descripcion
        )
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_categoria(self):
        if not self.id_categoria_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una categoría.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Eliminar esta categoría?")
        if not confirmar:
            return

        resultado, mensaje = self.categoria_controller.eliminar_categoria(self.id_categoria_seleccionada)
        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar_categoria(self):
        nombre = self.entry_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Ingresa un nombre para buscar.")
            return

        categorias = self.categoria_controller.buscar_por_nombre(nombre)
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for categoria in categorias:
            self.tabla.insert("", "end", values=categoria)

    def limpiar_formulario(self):
        self.id_categoria_seleccionada = None
        self.entry_nombre.delete(0, tk.END)
        self.txt_descripcion.delete("1.0", tk.END)
        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(seleccion)