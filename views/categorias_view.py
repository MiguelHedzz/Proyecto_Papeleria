# ==============================
# VISTA DE CATEGORÍAS
# ==============================

"""
Esta pantalla permite administrar las categorías de productos.

Funciones principales:
- Registrar categoría.
- Listar categorías.
- Buscar categoría por nombre.
- Actualizar categoría.
- Eliminar categoría (solo si no tiene productos asociados).

Esta vista se conecta con:
controllers/categoria_controller.py

Diseño basado en el prototipo de Figma:
- Sidebar izquierdo fijo
- Topbar con acciones
- Card blanca para el contenido
- Colores corporativos Dunder Mifflin
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Manejo de rutas para ejecución directa
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.categoria_controller import CategoriaController


# ==============================
# CLASE PRINCIPAL DE LA VISTA
# ==============================

class CategoriasView(tk.Toplevel):
    """
    Esta clase representa la pantalla de administración de categorías.

    Hereda de tk.Toplevel para abrirse como ventana independiente.
    Incluye diseño de sidebar y topbar como en el prototipo de Figma.
    """

    def __init__(self, parent, usuario=None):
        """
        Constructor de la pantalla.

        Parámetros:
        parent: ventana padre.
        usuario: objeto Usuario (opcional, para verificar rol).
        """

        super().__init__(parent)

        # Configuración de la ventana.
        self.title("Dunder Mifflin - Administrar Categorías")
        self.geometry("1000x600")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        # Centramos la ventana.
        self._centrar_ventana()

        # Guardamos el usuario.
        self.usuario = usuario

        # Controlador de categorías.
        self.categoria_controller = CategoriaController()

        # Variable para la categoría seleccionada.
        self.id_categoria_seleccionado = None

        # Construimos la interfaz completa.
        self._construir_interfaz()

        # Cargamos las categorías al iniciar.
        self.cargar_categorias()

    # ==============================
    # MÉTODOS PRIVADOS (DISEÑO)
    # ==============================

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"+{x}+{y}")

    def _construir_interfaz(self):
        """
        Construye toda la interfaz siguiendo el diseño del prototipo.
        Estructura: Sidebar izquierdo + Main (Topbar + Content)
        """

        # Frame principal
        self.frame_principal = tk.Frame(self, bg="#e8ecef")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self._crear_sidebar()

        # Área principal
        frame_main = tk.Frame(self.frame_principal, bg="#e8ecef")
        frame_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._crear_topbar(frame_main)
        self._crear_content(frame_main)

    def _crear_sidebar(self):
        """
        Crea la barra lateral izquierda con:
        - Logo / Brand
        - Rol del usuario
        - Navegación
        """

        frame_sidebar = tk.Frame(
            self.frame_principal,
            bg="#3a4f63",
            width=240
        )
        frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        frame_sidebar.pack_propagate(False)

        # Brand / Logo
        lbl_brand = tk.Label(
            frame_sidebar,
            text="Dunder Mifflin",
            font=("Segoe UI", 20, "bold"),
            bg="#3a4f63",
            fg="white"
        )
        lbl_brand.pack(pady=(40, 10))

        # Rol del usuario
        rol_texto = self.usuario.rol if self.usuario else "Administrador"
        lbl_rol = tk.Label(
            frame_sidebar,
            text=f"Rol: {rol_texto}",
            font=("Segoe UI", 11),
            bg="#3a4f63",
            fg="#b0c0d0"
        )
        lbl_rol.pack(pady=(0, 30))

        # Navegación
        nav_items = [
            ("Productos", self._ir_a_productos),
            ("Inventario", self._ir_a_inventario),
            ("Nueva Venta", self._ir_a_ventas),
            ("Cerrar Sesión", self._cerrar_sesion),
        ]

        for texto, comando in nav_items:
            btn_nav = tk.Button(
                frame_sidebar,
                text=texto,
                font=("Segoe UI", 11),
                bg="#3a4f63",
                fg="#b0c0d0",
                activebackground="#2c3e50",
                activeforeground="white",
                relief=tk.FLAT,
                anchor="w",
                padx=20,
                command=comando
            )
            btn_nav.pack(fill=tk.X, pady=2)

    def _crear_topbar(self, parent):
        """Crea la barra superior con botones de acciones rápidas."""

        frame_topbar = tk.Frame(parent, bg="white", height=60)
        frame_topbar.pack(fill=tk.X, side=tk.TOP)
        frame_topbar.pack_propagate(False)

        frame_acciones = tk.Frame(frame_topbar, bg="white")
        frame_acciones.pack(side=tk.RIGHT, padx=20, pady=10)

        # Botón: Gestión Categorías (actual, en negrita)
        btn_categorias = tk.Button(
            frame_acciones,
            text="Gestión Categorías",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            activebackground="#e8ecef",
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_categorias.pack(side=tk.LEFT, padx=5)

        # Botón: Soporte
        btn_soporte = tk.Button(
            frame_acciones,
            text="Soporte",
            font=("Segoe UI", 10),
            bg="white",
            fg="#2c3e50",
            activebackground="#e8ecef",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._ir_a_soporte
        )
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        """Crea el área de contenido principal."""

        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Card blanca
        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = tk.Label(
            card,
            text="Administrar Categorías",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        # Contenido
        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Formulario
        self._crear_formulario(frame_contenido_card)

        # Botones de acción
        self._crear_botones_accion(frame_contenido_card)

        # Tabla de categorías
        self._crear_tabla(frame_contenido_card)

    def _crear_formulario(self, parent):
        """Crea el formulario de categorías."""

        frame_campos = tk.Frame(parent, bg="white")
        frame_campos.pack(fill=tk.X, pady=10)

        # Nombre
        tk.Label(
            frame_campos, text="Nombre:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Descripción
        tk.Label(
            frame_campos, text="Descripción:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_descripcion = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

    def _crear_botones_accion(self, parent):
        """Crea los botones de acción y búsqueda."""

        frame_botones = tk.Frame(parent, bg="white")
        frame_botones.pack(fill=tk.X, pady=15)

        # Fila 0: Botones CRUD
        btn_agregar = tk.Button(
            frame_botones,
            text="Agregar",
            font=("Segoe UI", 10, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            command=self.agregar_categoria
        )
        btn_agregar.grid(row=0, column=0, padx=5, pady=5)

        btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar",
            font=("Segoe UI", 10, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            command=self.actualizar_categoria
        )
        btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            font=("Segoe UI", 10, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            command=self.eliminar_categoria
        )
        btn_eliminar.grid(row=0, column=2, padx=5, pady=5)

        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            font=("Segoe UI", 10, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#6c7a7d",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            command=self.limpiar_formulario
        )
        btn_limpiar.grid(row=0, column=3, padx=5, pady=5)

        # Fila 1: Búsqueda
        tk.Label(
            frame_botones, text="Buscar nombre:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_buscar = tk.Entry(frame_botones, width=30, font=("Segoe UI", 10))
        self.entry_buscar.grid(row=1, column=1, padx=5, pady=5)

        btn_buscar = tk.Button(
            frame_botones,
            text="Buscar",
            font=("Segoe UI", 10),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            command=self.buscar_categoria
        )
        btn_buscar.grid(row=1, column=2, padx=5, pady=5)

        btn_mostrar_todos = tk.Button(
            frame_botones,
            text="Mostrar todos",
            font=("Segoe UI", 10),
            bg="#7f8c8d",
            fg="white",
            activebackground="#6c7a7d",
            cursor="hand2",
            relief=tk.FLAT,
            command=self.cargar_categorias
        )
        btn_mostrar_todos.grid(row=1, column=3, padx=5, pady=5)

    def _crear_tabla(self, parent):
        """Crea el Treeview para listar categorías."""

        frame_tabla = tk.LabelFrame(
            parent,
            text="Lista de categorías",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        columnas = ("id", "nombre", "descripcion")

        self.tabla_categorias = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tabla_categorias.heading("id", text="ID")
        self.tabla_categorias.heading("nombre", text="Nombre")
        self.tabla_categorias.heading("descripcion", text="Descripción")

        self.tabla_categorias.column("id", width=50, anchor="center")
        self.tabla_categorias.column("nombre", width=200)
        self.tabla_categorias.column("descripcion", width=400)

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_categorias.yview
        )
        self.tabla_categorias.configure(yscrollcommand=scrollbar.set)

        self.tabla_categorias.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_categorias.bind("<<TreeviewSelect>>", self.seleccionar_categoria)

    # ==============================
    # MÉTODOS DE NAVEGACIÓN
    # ==============================

    def _ir_a_productos(self):
        """Abre la ventana de productos."""
        from views.productos_view import ProductosView
        self.destroy()
        ventana = ProductosView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_inventario(self):
        """Abre la ventana de inventario."""
        messagebox.showinfo("En desarrollo", "Módulo de inventario en construcción")

    def _ir_a_ventas(self):
        """Abre la ventana de ventas."""
        messagebox.showinfo("En desarrollo", "Módulo de ventas en construcción")

    def _ir_a_soporte(self):
        """Abre la ventana de soporte."""
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        """Cierra la sesión y vuelve al login."""
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()

    # ==============================
    # MÉTODOS DE NEGOCIO (CRUD)
    # ==============================

    def cargar_categorias(self):
        """Carga todas las categorías en la tabla."""
        for fila in self.tabla_categorias.get_children():
            self.tabla_categorias.delete(fila)

        categorias = self.categoria_controller.listar_categorias()

        for categoria in categorias:
            self.tabla_categorias.insert(
                "",
                "end",
                values=(
                    categoria[0],  # id
                    categoria[1],  # nombre
                    categoria[2]   # descripcion
                )
            )

        self.entry_buscar.delete(0, tk.END)

    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario."""
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        return nombre, descripcion

    def agregar_categoria(self):
        """Registra una nueva categoría."""
        nombre, descripcion = self.obtener_datos_formulario()

        resultado, mensaje = self.categoria_controller.registrar_categoria(
            nombre=nombre,
            descripcion=descripcion
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_categoria(self, event):
        """Carga la categoría seleccionada en el formulario."""
        seleccion = self.tabla_categorias.selection()

        if not seleccion:
            return

        valores = self.tabla_categorias.item(seleccion[0], "values")

        self.id_categoria_seleccionado = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, valores[2] if valores[2] else "")

    def actualizar_categoria(self):
        """Actualiza la categoría seleccionada."""
        if self.id_categoria_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una categoría de la tabla.")
            return

        nombre, descripcion = self.obtener_datos_formulario()

        resultado, mensaje = self.categoria_controller.actualizar_categoria(
            id_categoria=self.id_categoria_seleccionado,
            nombre=nombre,
            descripcion=descripcion
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_categoria(self):
        """Elimina la categoría seleccionada."""
        if self.id_categoria_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona una categoría de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar esta categoría?\n\nNota: No se puede eliminar si tiene productos asociados."
        )

        if not confirmar:
            return

        resultado, mensaje = self.categoria_controller.eliminar_categoria(
            self.id_categoria_seleccionado
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar_categoria(self):
        """Busca categorías por nombre."""
        nombre = self.entry_buscar.get().strip()

        if nombre == "":
            messagebox.showwarning("Aviso", "Ingresa un nombre para buscar.")
            return

        categorias = self.categoria_controller.buscar_por_nombre(nombre)

        for fila in self.tabla_categorias.get_children():
            self.tabla_categorias.delete(fila)

        for categoria in categorias:
            self.tabla_categorias.insert(
                "",
                "end",
                values=(
                    categoria[0],
                    categoria[1],
                    categoria[2]
                )
            )

        if len(categorias) == 0:
            messagebox.showinfo("Sin resultados", "No se encontraron categorías con ese nombre.")

    def limpiar_formulario(self):
        """Limpia el formulario."""
        self.id_categoria_seleccionado = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.tabla_categorias.selection_remove(self.tabla_categorias.selection())


# ==============================
# FUNCIÓN PARA ABRIR LA VISTA
# ==============================

def abrir_categorias(parent=None, usuario=None):
    """Abre la pantalla de categorías."""
    ventana = CategoriasView(parent, usuario)
    return ventana


# ==============================
# EJECUCIÓN DIRECTA
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = CategoriasView(root)
    ventana.mainloop()