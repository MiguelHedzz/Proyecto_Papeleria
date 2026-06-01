# ==============================
# VISTA DE PROVEEDORES
# ==============================

"""
Esta pantalla permite administrar los proveedores.

Funciones principales:
- Registrar proveedor.
- Listar proveedores.
- Buscar proveedor por nombre.
- Actualizar proveedor.
- Eliminar proveedor (solo si no tiene productos asociados).

Esta vista se conecta con:
controllers/proveedor_controller.py

Diseño basado en el prototipo de Figma.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.proveedor_controller import ProveedorController


class ProveedoresView(tk.Toplevel):
    """Pantalla de administración de proveedores."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Administrar Proveedores")
        self.geometry("1000x600")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario = usuario
        self.proveedor_controller = ProveedorController()
        self.id_proveedor_seleccionado = None

        self._construir_interfaz()
        self.cargar_proveedores()

    def _centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"+{x}+{y}")

    def _construir_interfaz(self):
        self.frame_principal = tk.Frame(self, bg="#e8ecef")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        self._crear_sidebar()

        frame_main = tk.Frame(self.frame_principal, bg="#e8ecef")
        frame_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._crear_topbar(frame_main)
        self._crear_content(frame_main)

    def _crear_sidebar(self):
        frame_sidebar = tk.Frame(self.frame_principal, bg="#3a4f63", width=240)
        frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        frame_sidebar.pack_propagate(False)

        lbl_brand = tk.Label(frame_sidebar, text="Dunder Mifflin", font=("Segoe UI", 20, "bold"), bg="#3a4f63", fg="white")
        lbl_brand.pack(pady=(40, 10))

        rol_texto = self.usuario.rol if self.usuario else "Administrador"
        lbl_rol = tk.Label(frame_sidebar, text=f"Rol: {rol_texto}", font=("Segoe UI", 11), bg="#3a4f63", fg="#b0c0d0")
        lbl_rol.pack(pady=(0, 30))

        nav_items = [
            ("Productos", self._ir_a_productos),
            ("Categorías", self._ir_a_categorias),
            ("Inventario", self._ir_a_inventario),
            ("Nueva Venta", self._ir_a_ventas),
            ("Cerrar Sesión", self._cerrar_sesion),
        ]

        for texto, comando in nav_items:
            btn_nav = tk.Button(frame_sidebar, text=texto, font=("Segoe UI", 11), bg="#3a4f63", fg="#b0c0d0",
                               activebackground="#2c3e50", activeforeground="white", relief=tk.FLAT, anchor="w",
                               padx=20, command=comando)
            btn_nav.pack(fill=tk.X, pady=2)

    def _crear_topbar(self, parent):
        frame_topbar = tk.Frame(parent, bg="white", height=60)
        frame_topbar.pack(fill=tk.X, side=tk.TOP)
        frame_topbar.pack_propagate(False)

        frame_acciones = tk.Frame(frame_topbar, bg="white")
        frame_acciones.pack(side=tk.RIGHT, padx=20, pady=10)

        btn_proveedores = tk.Button(frame_acciones, text="Gestión Proveedores", font=("Segoe UI", 10, "bold"),
                                    bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_proveedores.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Administrar Proveedores", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._crear_formulario(frame_contenido_card)
        self._crear_botones_accion(frame_contenido_card)
        self._crear_tabla(frame_contenido_card)

    def _crear_formulario(self, parent):
        frame_campos = tk.Frame(parent, bg="white")
        frame_campos.pack(fill=tk.X, pady=10)

        tk.Label(frame_campos, text="Nombre:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_campos, text="Teléfono:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_telefono = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_telefono.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_campos, text="Correo:", bg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_correo = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5)

    def _crear_botones_accion(self, parent):
        frame_botones = tk.Frame(parent, bg="white")
        frame_botones.pack(fill=tk.X, pady=15)

        btn_agregar = tk.Button(frame_botones, text="Agregar", font=("Segoe UI", 10, "bold"), bg="#e67e22", fg="white",
                                activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=15, command=self.agregar_proveedor)
        btn_agregar.grid(row=0, column=0, padx=5, pady=5)

        btn_actualizar = tk.Button(frame_botones, text="Actualizar", font=("Segoe UI", 10, "bold"), bg="#e67e22", fg="white",
                                   activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=15, command=self.actualizar_proveedor)
        btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar", font=("Segoe UI", 10, "bold"), bg="#e67e22", fg="white",
                                 activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=15, command=self.eliminar_proveedor)
        btn_eliminar.grid(row=0, column=2, padx=5, pady=5)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar", font=("Segoe UI", 10, "bold"), bg="#7f8c8d", fg="white",
                                activebackground="#6c7a7d", cursor="hand2", relief=tk.FLAT, padx=15, command=self.limpiar_formulario)
        btn_limpiar.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_botones, text="Buscar nombre:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_buscar = tk.Entry(frame_botones, width=30, font=("Segoe UI", 10))
        self.entry_buscar.grid(row=1, column=1, padx=5, pady=5)

        btn_buscar = tk.Button(frame_botones, text="Buscar", font=("Segoe UI", 10), bg="#e67e22", fg="white",
                               activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=10, command=self.buscar_proveedor)
        btn_buscar.grid(row=1, column=2, padx=5, pady=5)

        btn_mostrar_todos = tk.Button(frame_botones, text="Mostrar todos", font=("Segoe UI", 10), bg="#7f8c8d", fg="white",
                                      activebackground="#6c7a7d", cursor="hand2", relief=tk.FLAT, command=self.cargar_proveedores)
        btn_mostrar_todos.grid(row=1, column=3, padx=5, pady=5)

    def _crear_tabla(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Lista de proveedores", font=("Segoe UI", 11, "bold"), bg="white", fg="#2c3e50")
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        columnas = ("id", "nombre", "telefono", "correo")
        self.tabla_proveedores = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        self.tabla_proveedores.heading("id", text="ID")
        self.tabla_proveedores.heading("nombre", text="Nombre")
        self.tabla_proveedores.heading("telefono", text="Teléfono")
        self.tabla_proveedores.heading("correo", text="Correo")

        self.tabla_proveedores.column("id", width=50, anchor="center")
        self.tabla_proveedores.column("nombre", width=200)
        self.tabla_proveedores.column("telefono", width=150, anchor="center")
        self.tabla_proveedores.column("correo", width=300)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_proveedores.yview)
        self.tabla_proveedores.configure(yscrollcommand=scrollbar.set)

        self.tabla_proveedores.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_proveedores.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def _ir_a_productos(self):
        from views.productos_view import ProductosView
        self.destroy()
        ventana = ProductosView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_categorias(self):
        from views.categorias_view import CategoriasView
        self.destroy()
        ventana = CategoriasView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_inventario(self):
        messagebox.showinfo("En desarrollo", "Módulo de inventario en construcción")

    def _ir_a_ventas(self):
        messagebox.showinfo("En desarrollo", "Módulo de ventas en construcción")

    def _ir_a_soporte(self):
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()

    def cargar_proveedores(self):
        for fila in self.tabla_proveedores.get_children():
            self.tabla_proveedores.delete(fila)

        proveedores = self.proveedor_controller.listar_proveedores()

        for proveedor in proveedores:
            self.tabla_proveedores.insert("", "end", values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3]))

        self.entry_buscar.delete(0, tk.END)

    def obtener_datos_formulario(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        return nombre, telefono, correo

    def agregar_proveedor(self):
        nombre, telefono, correo = self.obtener_datos_formulario()
        resultado, mensaje = self.proveedor_controller.registrar_proveedor(nombre, telefono, correo)

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_proveedor(self, event):
        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            return

        valores = self.tabla_proveedores.item(seleccion[0], "values")
        self.id_proveedor_seleccionado = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, valores[2] if valores[2] else "")
        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, valores[3] if valores[3] else "")

    def actualizar_proveedor(self):
        if self.id_proveedor_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un proveedor de la tabla.")
            return

        nombre, telefono, correo = self.obtener_datos_formulario()
        resultado, mensaje = self.proveedor_controller.actualizar_proveedor(self.id_proveedor_seleccionado, nombre, telefono, correo)

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

        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar este proveedor?\n\nNota: No se puede eliminar si tiene productos asociados.")

        if not confirmar:
            return

        resultado, mensaje = self.proveedor_controller.eliminar_proveedor(self.id_proveedor_seleccionado)

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

        for fila in self.tabla_proveedores.get_children():
            self.tabla_proveedores.delete(fila)

        for proveedor in proveedores:
            self.tabla_proveedores.insert("", "end", values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3]))

        if len(proveedores) == 0:
            messagebox.showinfo("Sin resultados", "No se encontraron proveedores con ese nombre.")

    def limpiar_formulario(self):
        self.id_proveedor_seleccionado = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.tabla_proveedores.selection_remove(self.tabla_proveedores.selection())


def abrir_proveedores(parent=None, usuario=None):
    ventana = ProveedoresView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ProveedoresView(root)
    ventana.mainloop()