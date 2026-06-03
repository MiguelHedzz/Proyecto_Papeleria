# ==============================
# LAYOUT PRINCIPAL DEL SISTEMA
# ==============================

"""
Este archivo contiene el diseño base del sistema según el prototipo de Figma.

Incluye:
- Sidebar izquierdo azul oscuro.
- Topbar superior blanca.
- Área principal gris claro.
- Card blanca central.
- Pantallas internas: Nueva Venta, Gestión Productos, Reportes y Soporte.
- Botón de Usuarios para registrar usuarios.
- Cambio de rol Administrador/Vendedor.
- CRUD completo de productos conectado con ProductoController.
- Venta básica conectada con productos reales y VentaService.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Permite importar correctamente aunque se ejecute este archivo directamente.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.producto_controller import ProductoController
from services.venta_service import VentaService
from services.reporte_service import ReporteService


class LayoutPrincipal(tk.Toplevel):
    """
    Ventana principal del sistema después del login.

    Esta ventana respeta el diseño del prototipo de Figma:
    sidebar, topbar y contenido central dinámico.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.parent = parent
        self.usuario = usuario

        # Datos del usuario.
        self.nombre_usuario = self.obtener_nombre_usuario()
        self.rol_usuario = self.obtener_rol_usuario()
        self.id_usuario = self.obtener_id_usuario()

        # Configuración de la ventana.
        self.title("Dunder Mifflin - Sistema de Inventario")
        self.geometry("1280x720")
        self.minsize(1100, 650)
        self.configure(bg="#ecf0f1")

        # Colores del prototipo.
        self.color_sidebar = "#2c3e50"
        self.color_sidebar_boton = "#34495e"
        self.color_fondo = "#ecf0f1"
        self.color_card = "white"
        self.color_texto = "#2c3e50"
        self.color_naranja = "#e67e22"
        self.color_gris = "#95a5a6"
        self.color_rojo = "#e74c3c"
        self.color_verde = "#27ae60"

        # Controladores y servicios.
        self.producto_controller = ProductoController()
        self.venta_service = VentaService()
        self.reporte_service = ReporteService()

        # Referencias visuales.
        self.contenedor_general = None
        self.sidebar = None
        self.area_derecha = None
        self.topbar = None
        self.area_contenido = None
        self.card_actual = None

        # Variables de productos.
        self.id_producto_seleccionado = None

        # Variables de venta.
        self.carrito = []
        self.total_venta = 0.0
        self.productos_combo = []

        # Construir diseño.
        self.crear_layout()

        # Pantalla inicial.
        self.mostrar_venta()

    # ==============================
    # DATOS DEL USUARIO
    # ==============================

    def obtener_id_usuario(self):
        """
        Obtiene el ID del usuario.

        Si no existe, usa 1 como administrador de prueba.
        """

        if self.usuario is None:
            return 1

        if hasattr(self.usuario, "id_usuario"):
            return self.usuario.id_usuario

        if isinstance(self.usuario, dict):
            return self.usuario.get("id_usuario", 1)

        if isinstance(self.usuario, (tuple, list)):
            if len(self.usuario) > 0:
                return self.usuario[0]

        return 1

    def obtener_nombre_usuario(self):
        """
        Obtiene el nombre del usuario.

        Puede recibir usuario como objeto, diccionario, tupla o lista.
        """

        if self.usuario is None:
            return "Usuario"

        if hasattr(self.usuario, "nombre"):
            return self.usuario.nombre

        if isinstance(self.usuario, dict):
            return self.usuario.get("nombre", "Usuario")

        if isinstance(self.usuario, (tuple, list)):
            if len(self.usuario) > 1:
                return self.usuario[1]

        return "Usuario"

    def obtener_rol_usuario(self):
        """
        Obtiene el rol del usuario.

        Si no existe rol, se usa Administrador por defecto.
        """

        if self.usuario is None:
            return "Administrador"

        if hasattr(self.usuario, "rol"):
            return self.usuario.rol

        if isinstance(self.usuario, dict):
            return self.usuario.get("rol", "Administrador")

        if isinstance(self.usuario, (tuple, list)):
            if len(self.usuario) > 3:
                return self.usuario[3]

        return "Administrador"

    # ==============================
    # LAYOUT GENERAL
    # ==============================

    def crear_layout(self):
        """
        Crea la estructura principal:
        sidebar izquierdo, topbar superior y área de contenido.
        """

        self.contenedor_general = tk.Frame(self, bg=self.color_fondo)
        self.contenedor_general.pack(fill="both", expand=True)

        self.crear_sidebar()

        self.area_derecha = tk.Frame(
            self.contenedor_general,
            bg=self.color_fondo
        )
        self.area_derecha.pack(side="left", fill="both", expand=True)

        self.crear_topbar()

        self.area_contenido = tk.Frame(
            self.area_derecha,
            bg=self.color_fondo
        )
        self.area_contenido.pack(fill="both", expand=True)

    # ==============================
    # SIDEBAR
    # ==============================

    def crear_sidebar(self):
        """
        Crea el menú lateral izquierdo.
        """

        self.sidebar = tk.Frame(
            self.contenedor_general,
            bg=self.color_sidebar,
            width=255
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        titulo = tk.Label(
            self.sidebar,
            text="Dunder Mifflin",
            bg=self.color_sidebar,
            fg="white",
            font=("Segoe UI", 22, "bold")
        )
        titulo.pack(anchor="w", padx=20, pady=(45, 35))

        rol = tk.Label(
            self.sidebar,
            text=f"Rol: {self.rol_usuario}",
            bg=self.color_sidebar,
            fg="white",
            font=("Segoe UI", 14)
        )
        rol.pack(anchor="w", padx=20, pady=(0, 55))

        self.crear_boton_sidebar(
            texto="🛒 Nueva Venta (RF05)",
            comando=self.mostrar_venta
        )

        if self.rol_usuario == "Administrador":
            self.crear_boton_sidebar(
                texto="📊 Reportes (RF07)",
                comando=self.mostrar_reportes
            )

        espacio = tk.Frame(self.sidebar, bg=self.color_sidebar)
        espacio.pack(fill="both", expand=True)

        btn_cambiar = tk.Button(
            self.sidebar,
            text="Simular Cambio de Rol",
            bg=self.color_gris,
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.simular_cambio_rol
        )
        btn_cambiar.pack(fill="x", padx=20, pady=(0, 35))

    def crear_boton_sidebar(self, texto, comando):
        """
        Crea un botón del menú lateral.
        """

        boton = tk.Button(
            self.sidebar,
            text=texto,
            bg=self.color_sidebar_boton,
            fg="white",
            activebackground=self.color_naranja,
            activeforeground="white",
            font=("Segoe UI", 12),
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=12,
            height=2,
            command=comando
        )
        boton.pack(fill="x", padx=20, pady=6)

        return boton

    # ==============================
    # TOPBAR
    # ==============================

    def crear_topbar(self):
        """
        Crea la barra superior blanca.
        """

        self.topbar = tk.Frame(
            self.area_derecha,
            bg="white",
            height=65
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        # Botón Soporte, visible para todos.
        btn_soporte = self.crear_boton_topbar(
            texto="🎧 Soporte",
            comando=self.mostrar_soporte
        )
        btn_soporte.pack(side="right", padx=(10, 25), pady=12)

        # Botones exclusivos del administrador.
        if self.rol_usuario == "Administrador":
            btn_usuarios = self.crear_boton_topbar(
                texto="👤 Usuarios",
                comando=self.mostrar_usuarios
            )
            btn_usuarios.pack(side="right", padx=(10, 5), pady=12)

            btn_productos = self.crear_boton_topbar(
                texto="📦 Gestión Productos",
                comando=self.mostrar_productos
            )
            btn_productos.pack(side="right", padx=(10, 5), pady=12)

    def crear_boton_topbar(self, texto, comando):
        """
        Crea un botón de la barra superior.
        """

        boton = tk.Button(
            self.topbar,
            text=texto,
            bg="white",
            fg=self.color_texto,
            activebackground="#f8f9fa",
            activeforeground=self.color_texto,
            font=("Segoe UI", 11, "bold"),
            relief="solid",
            bd=2,
            cursor="hand2",
            padx=15,
            command=comando
        )

        return boton

    # ==============================
    # CONTENIDO DINÁMICO
    # ==============================

    def limpiar_contenido(self):
        """
        Limpia el área principal antes de mostrar otra pantalla.
        """

        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    def crear_card(self):
        """
        Crea la tarjeta blanca central.
        """

        self.limpiar_contenido()

        card = tk.Frame(
            self.area_contenido,
            bg=self.color_card,
            relief="flat",
            bd=0
        )
        card.pack(fill="both", expand=True, padx=35, pady=35)

        self.card_actual = card
        return card

    # ==============================
    # PANTALLA NUEVA VENTA
    # ==============================

    def mostrar_venta(self):
        """
        Muestra la pantalla Nueva Venta basada en Figma.
        """

        self.carrito = []
        self.total_venta = 0.0

        card = self.crear_card()

        titulo = tk.Label(
            card,
            text="Registrar Venta",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(anchor="w", padx=25, pady=(25, 20))

        lbl_buscar = tk.Label(
            card,
            text="Buscar Producto",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 13, "bold")
        )
        lbl_buscar.pack(anchor="w", padx=25)

        # Cargamos productos para el combo.
        productos = self.producto_controller.listar_productos()
        self.productos_combo = productos

        valores_combo = []
        for producto in productos:
            # producto[0] id, producto[1] nombre, producto[2] código,
            # producto[3] precio, producto[7] cantidad actual
            cantidad = producto[7] if len(producto) > 7 else 0
            valores_combo.append(
                f"{producto[0]} - {producto[1]} (${producto[3]}) | Stock: {cantidad}"
            )

        self.combo_producto_venta = ttk.Combobox(
            card,
            values=valores_combo,
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.combo_producto_venta.pack(fill="x", padx=25, pady=(5, 15), ipady=5)

        frame_cantidad = tk.Frame(card, bg="white")
        frame_cantidad.pack(fill="x", padx=25, pady=(0, 15))

        lbl_cantidad = tk.Label(
            frame_cantidad,
            text="Cantidad:",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 12, "bold")
        )
        lbl_cantidad.pack(side="left")

        self.entry_cantidad_venta = tk.Entry(
            frame_cantidad,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=10
        )
        self.entry_cantidad_venta.insert(0, "1")
        self.entry_cantidad_venta.pack(side="left", padx=10, ipady=5)

        btn_agregar = tk.Button(
            frame_cantidad,
            text="Agregar al Carrito",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.agregar_producto_carrito
        )
        btn_agregar.pack(side="left", padx=15)

        columnas = ("id_producto", "producto", "cantidad", "precio", "subtotal")

        self.tabla_carrito = ttk.Treeview(
            card,
            columns=columnas,
            show="headings",
            height=5
        )

        self.tabla_carrito.heading("id_producto", text="ID")
        self.tabla_carrito.heading("producto", text="Producto")
        self.tabla_carrito.heading("cantidad", text="Cant.")
        self.tabla_carrito.heading("precio", text="Precio")
        self.tabla_carrito.heading("subtotal", text="Subtotal")

        self.tabla_carrito.column("id_producto", width=60, anchor="center")
        self.tabla_carrito.column("producto", width=350)
        self.tabla_carrito.column("cantidad", width=120, anchor="center")
        self.tabla_carrito.column("precio", width=120, anchor="center")
        self.tabla_carrito.column("subtotal", width=160, anchor="center")

        self.tabla_carrito.pack(fill="x", padx=25, pady=(0, 20))

        self.lbl_total = tk.Label(
            card,
            text="Total: $0.00",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 16, "bold")
        )
        self.lbl_total.pack(anchor="e", padx=25, pady=(0, 20))

        frame_pago = tk.Frame(card, bg="white")
        frame_pago.pack(fill="x", padx=25, pady=(0, 25))

        lbl_metodo = tk.Label(
            frame_pago,
            text="Método de Pago:",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 13, "bold")
        )
        lbl_metodo.pack(side="left", padx=(520, 15))

        self.entry_metodo_pago = tk.Entry(
            frame_pago,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=20
        )
        self.entry_metodo_pago.insert(0, "Efectivo")
        self.entry_metodo_pago.pack(side="left", ipady=8)

        btn_confirmar = tk.Button(
            frame_pago,
            text="Confirmar Venta",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.confirmar_venta
        )
        btn_confirmar.pack(side="right")

    def obtener_producto_combo(self):
        """
        Obtiene el producto seleccionado en el combo de venta.
        """

        seleccionado = self.combo_producto_venta.get()

        if seleccionado == "":
            return None

        try:
            id_producto = int(seleccionado.split(" - ")[0])
        except Exception:
            return None

        for producto in self.productos_combo:
            if int(producto[0]) == id_producto:
                return producto

        return None

    def agregar_producto_carrito(self):
        """
        Agrega el producto seleccionado al carrito.
        """

        producto = self.obtener_producto_combo()

        if producto is None:
            messagebox.showwarning(
                "Producto requerido",
                "Selecciona un producto para agregar al carrito."
            )
            return

        cantidad_texto = self.entry_cantidad_venta.get().strip()

        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "La cantidad debe ser un número entero."
            )
            return

        if cantidad <= 0:
            messagebox.showwarning(
                "Cantidad inválida",
                "La cantidad debe ser mayor que cero."
            )
            return

        stock_actual = producto[7] if len(producto) > 7 else 0

        if cantidad > stock_actual:
            messagebox.showwarning(
                "Stock insuficiente",
                "No hay suficiente stock para este producto."
            )
            return

        id_producto = producto[0]
        nombre = producto[1]
        precio = float(producto[3])
        subtotal = cantidad * precio

        item_carrito = {
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio": precio
        }

        self.carrito.append(item_carrito)
        self.total_venta += subtotal

        self.tabla_carrito.insert(
            "",
            "end",
            values=(
                id_producto,
                nombre,
                cantidad,
                f"${precio:.2f}",
                f"${subtotal:.2f}"
            )
        )

        self.lbl_total.config(text=f"Total: ${self.total_venta:.2f}")

    def confirmar_venta(self):
        """
        Confirma la venta usando VentaService.
        """

        if not self.carrito:
            messagebox.showwarning(
                "Carrito vacío",
                "Agrega al menos un producto al carrito."
            )
            return

        resultado, mensaje = self.venta_service.procesar_venta(
            productos=self.carrito,
            id_usuario=self.id_usuario
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.mostrar_venta()
        else:
            messagebox.showerror("Error", mensaje)

    # ==============================
    # PANTALLA GESTIÓN PRODUCTOS
    # ==============================

    def mostrar_productos(self):
        """
        Muestra la pantalla Gestión Productos basada en Figma.

        Esta pantalla cumple con el CRUD de Producto:
        - Crear producto.
        - Leer productos en tabla.
        - Actualizar producto seleccionado.
        - Eliminar producto seleccionado.
        """

        if self.rol_usuario != "Administrador":
            messagebox.showwarning(
                "Acceso denegado",
                "Solo el administrador puede gestionar productos."
            )
            return

        self.id_producto_seleccionado = None

        card = self.crear_card()

        frame_titulo = tk.Frame(card, bg="white")
        frame_titulo.pack(anchor="w", padx=25, pady=(25, 15))

        titulo = tk.Label(
            frame_titulo,
            text="Administrar Catálogo",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 26, "bold")
        )
        titulo.pack(side="left")

        solo_admin = tk.Label(
            frame_titulo,
            text=" (Sólo Administrador)",
            bg="white",
            fg=self.color_rojo,
            font=("Segoe UI", 18, "bold")
        )
        solo_admin.pack(side="left", padx=5)

        # Formulario
        frame_formulario = tk.Frame(card, bg="white")
        frame_formulario.pack(fill="x", padx=25, pady=(5, 15))

        tk.Label(
            frame_formulario,
            text="Código del Producto",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(0, 5))

        tk.Label(
            frame_formulario,
            text="Nombre",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=1, sticky="w", padx=(0, 15), pady=(0, 5))

        tk.Label(
            frame_formulario,
            text="Precio de Venta",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 15), pady=(0, 5))

        self.entry_codigo_producto = tk.Entry(
            frame_formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=24
        )
        self.entry_codigo_producto.grid(row=1, column=0, padx=(0, 15), ipady=6)

        self.entry_nombre_producto = tk.Entry(
            frame_formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_nombre_producto.grid(row=1, column=1, padx=(0, 15), ipady=6)

        self.entry_precio_producto = tk.Entry(
            frame_formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=20
        )
        self.entry_precio_producto.grid(row=1, column=2, padx=(0, 15), ipady=6)

        # Botones CRUD
        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", padx=25, pady=(5, 15))

        tk.Button(
            frame_botones,
            text="Guardar Producto",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.guardar_producto
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            frame_botones,
            text="Actualizar",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=14,
            height=2,
            command=self.actualizar_producto
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            frame_botones,
            text="Eliminar",
            bg=self.color_rojo,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=14,
            height=2,
            command=self.eliminar_producto
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            frame_botones,
            text="Limpiar",
            bg=self.color_gris,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=12,
            height=2,
            command=self.limpiar_formulario_producto
        ).pack(side="left", padx=(0, 10))

        # Tabla
        frame_tabla = tk.LabelFrame(
            card,
            text="Productos registrados",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 11, "bold"),
            padx=8,
            pady=8
        )
        frame_tabla.pack(fill="both", expand=True, padx=25, pady=(0, 25))

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
            height=8
        )

        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock_minimo", text="Stock mín.")
        self.tabla_productos.heading("cantidad", text="Cantidad")
        self.tabla_productos.heading("ubicacion", text="Ubicación")

        self.tabla_productos.column("id", width=55, anchor="center")
        self.tabla_productos.column("codigo", width=120, anchor="center")
        self.tabla_productos.column("nombre", width=260)
        self.tabla_productos.column("precio", width=100, anchor="center")
        self.tabla_productos.column("stock_minimo", width=100, anchor="center")
        self.tabla_productos.column("cantidad", width=100, anchor="center")
        self.tabla_productos.column("ubicacion", width=160)

        self.tabla_productos.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

        self.cargar_productos_tabla()

    def guardar_producto(self):
        """
        Guarda un producto nuevo en la base de datos.
        """

        codigo = self.entry_codigo_producto.get().strip()
        nombre = self.entry_nombre_producto.get().strip()
        precio = self.entry_precio_producto.get().strip()

        if codigo == "" or nombre == "" or precio == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Debes llenar código, nombre y precio del producto."
            )
            return

        resultado, mensaje = self.producto_controller.registrar_producto(
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            stock_minimo=0,
            cantidad_inicial=10,
            ubicacion=""
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_producto()
            self.cargar_productos_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_productos_tabla(self):
        """
        Carga los productos registrados en la tabla.
        """

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

    def seleccionar_producto(self, event):
        """
        Carga en el formulario el producto seleccionado en la tabla.
        """

        seleccion = self.tabla_productos.selection()

        if not seleccion:
            return

        valores = self.tabla_productos.item(seleccion[0], "values")

        self.id_producto_seleccionado = valores[0]

        self.entry_codigo_producto.delete(0, tk.END)
        self.entry_codigo_producto.insert(0, valores[1])

        self.entry_nombre_producto.delete(0, tk.END)
        self.entry_nombre_producto.insert(0, valores[2])

        self.entry_precio_producto.delete(0, tk.END)
        self.entry_precio_producto.insert(0, valores[3])

    def actualizar_producto(self):
        """
        Actualiza el producto seleccionado.
        """

        if self.id_producto_seleccionado is None:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un producto de la tabla."
            )
            return

        codigo = self.entry_codigo_producto.get().strip()
        nombre = self.entry_nombre_producto.get().strip()
        precio = self.entry_precio_producto.get().strip()

        if codigo == "" or nombre == "" or precio == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Debes llenar código, nombre y precio."
            )
            return

        resultado, mensaje = self.producto_controller.actualizar_producto(
            id_producto=self.id_producto_seleccionado,
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            stock_minimo=0,
            id_categoria=None,
            id_proveedor=None
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_producto()
            self.cargar_productos_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_producto(self):
        """
        Elimina el producto seleccionado.
        """

        if self.id_producto_seleccionado is None:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un producto de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este producto?"
        )

        if not confirmar:
            return

        resultado, mensaje = self.producto_controller.eliminar_producto(
            self.id_producto_seleccionado
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_producto()
            self.cargar_productos_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario_producto(self):
        """
        Limpia los campos del formulario de productos.
        """

        self.id_producto_seleccionado = None

        if hasattr(self, "entry_codigo_producto"):
            self.entry_codigo_producto.delete(0, tk.END)

        if hasattr(self, "entry_nombre_producto"):
            self.entry_nombre_producto.delete(0, tk.END)

        if hasattr(self, "entry_precio_producto"):
            self.entry_precio_producto.delete(0, tk.END)

        if hasattr(self, "tabla_productos"):
            seleccion = self.tabla_productos.selection()
            if seleccion:
                self.tabla_productos.selection_remove(seleccion)

    # ==============================
    # PANTALLA USUARIOS
    # ==============================

    def mostrar_usuarios(self):
        """
        Abre la ventana de registro de usuarios.

        Esta opción solo está disponible para el administrador.
        """

        if self.rol_usuario != "Administrador":
            messagebox.showwarning(
                "Acceso denegado",
                "Solo el administrador puede registrar usuarios."
            )
            return

        try:
            from views.usuarios_view import VentanaUsuarios

            ventana = VentanaUsuarios(self)
            ventana.focus_set()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir la ventana de usuarios.\n\nDetalle: {error}"
            )

    # ==============================
    # PANTALLA REPORTES
    # ==============================

    def mostrar_reportes(self):
        """
        Muestra la pantalla Reportes basada en Figma.

        Esta versión ya se conecta con ReporteService para mostrar:
        - Total de productos.
        - Total de ventas.
        - Total de ingresos.
        - Productos con stock bajo.
        - Tabla de ventas.
        - Tabla de productos.
        """

        if self.rol_usuario != "Administrador":
            messagebox.showwarning(
                "Acceso denegado",
                "Solo el administrador puede ver reportes."
            )
            return

        card = self.crear_card()

        frame_titulo = tk.Frame(card, bg="white")
        frame_titulo.pack(anchor="w", padx=25, pady=(25, 15))

        titulo = tk.Label(
            frame_titulo,
            text="Reportes del Sistema",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 26, "bold")
        )
        titulo.pack(side="left")

        solo_admin = tk.Label(
            frame_titulo,
            text=" (Sólo Administrador)",
            bg="white",
            fg=self.color_rojo,
            font=("Segoe UI", 18, "bold")
        )
        solo_admin.pack(side="left", padx=5)

        try:
            resumen = self.reporte_service.resumen_general()
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo cargar el resumen de reportes.\n\nDetalle: {error}"
            )
            resumen = {}

        # Tarjetas de resumen
        frame_resumen = tk.Frame(card, bg="white")
        frame_resumen.pack(fill="x", padx=25, pady=(5, 20))

        tarjetas = [
            ("Productos", resumen.get("total_productos", 0), self.color_naranja),
            ("Ventas", resumen.get("total_ventas", 0), self.color_verde),
            ("Ingresos", f"${float(resumen.get('total_ingresos', 0)):.2f}", self.color_texto),
            ("Stock bajo", resumen.get("productos_stock_bajo", 0), self.color_rojo),
        ]

        for titulo_tarjeta, valor, color in tarjetas:
            tarjeta = tk.Frame(
                frame_resumen,
                bg="#f8f9fa",
                relief="solid",
                bd=1,
                padx=15,
                pady=12
            )
            tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 12))

            tk.Label(
                tarjeta,
                text=titulo_tarjeta,
                bg="#f8f9fa",
                fg=self.color_texto,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w")

            tk.Label(
                tarjeta,
                text=str(valor),
                bg="#f8f9fa",
                fg=color,
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", pady=(5, 0))

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", padx=25, pady=(0, 15))

        tk.Button(
            frame_botones,
            text="Actualizar reportes",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.mostrar_reportes
        ).pack(side="left")

        # Pestañas de reportes
        notebook = ttk.Notebook(card)
        notebook.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        tab_stock = tk.Frame(notebook, bg="white")
        tab_ventas = tk.Frame(notebook, bg="white")
        tab_productos = tk.Frame(notebook, bg="white")

        notebook.add(tab_stock, text="Stock bajo")
        notebook.add(tab_ventas, text="Ventas")
        notebook.add(tab_productos, text="Productos")

        self.crear_tabla_stock_bajo(tab_stock)
        self.crear_tabla_ventas(tab_ventas)
        self.crear_tabla_productos_reporte(tab_productos)

    def crear_tabla_stock_bajo(self, parent):
        """
        Crea la tabla de productos con stock bajo.
        """

        columnas = ("id", "nombre", "codigo", "stock_minimo", "cantidad", "ubicacion")

        tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=8
        )

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "codigo": "Código",
            "stock_minimo": "Stock mín.",
            "cantidad": "Cantidad",
            "ubicacion": "Ubicación",
        }

        for columna, texto in encabezados.items():
            tabla.heading(columna, text=texto)

        tabla.column("id", width=60, anchor="center")
        tabla.column("nombre", width=250)
        tabla.column("codigo", width=120, anchor="center")
        tabla.column("stock_minimo", width=120, anchor="center")
        tabla.column("cantidad", width=120, anchor="center")
        tabla.column("ubicacion", width=160)

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            datos = self.reporte_service.reporte_stock_bajo()
        except Exception:
            datos = []

        for item in datos:
            tabla.insert("", "end", values=item)

    def crear_tabla_ventas(self, parent):
        """
        Crea la tabla de ventas registradas.
        """

        columnas = ("id", "fecha", "total", "usuario")

        tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=8
        )

        tabla.heading("id", text="ID")
        tabla.heading("fecha", text="Fecha")
        tabla.heading("total", text="Total")
        tabla.heading("usuario", text="Usuario")

        tabla.column("id", width=60, anchor="center")
        tabla.column("fecha", width=220)
        tabla.column("total", width=120, anchor="center")
        tabla.column("usuario", width=180)

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            datos = self.reporte_service.reporte_ventas()
        except Exception:
            datos = []

        for venta in datos:
            # VentaController puede regresar 4 o 5 columnas dependiendo de la versión.
            if len(venta) >= 5:
                valores = (venta[0], venta[1], venta[2], venta[4])
            else:
                valores = (venta[0], venta[1], venta[2], "")
            tabla.insert("", "end", values=valores)

    def crear_tabla_productos_reporte(self, parent):
        """
        Crea la tabla de productos registrados.
        """

        columnas = ("id", "codigo", "nombre", "precio", "cantidad")

        tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=8
        )

        tabla.heading("id", text="ID")
        tabla.heading("codigo", text="Código")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("precio", text="Precio")
        tabla.heading("cantidad", text="Cantidad")

        tabla.column("id", width=60, anchor="center")
        tabla.column("codigo", width=120, anchor="center")
        tabla.column("nombre", width=280)
        tabla.column("precio", width=120, anchor="center")
        tabla.column("cantidad", width=120, anchor="center")

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            datos = self.reporte_service.reporte_productos()
        except Exception:
            datos = []

        for producto in datos:
            cantidad = producto[7] if len(producto) > 7 else 0
            tabla.insert(
                "",
                "end",
                values=(producto[0], producto[2], producto[1], producto[3], cantidad)
            )


    # ==============================
    # PANTALLA SOPORTE
    # ==============================

    def mostrar_soporte(self):
        """
        Muestra la pantalla Soporte Técnico basada en Figma.
        """

        card = self.crear_card()

        titulo = tk.Label(
            card,
            text="Soporte Técnico",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(anchor="w", padx=25, pady=(30, 20))

        descripcion = tk.Label(
            card,
            text="¿Tienes problemas con el sistema? Envía un reporte al administrador.",
            bg="white",
            fg="black",
            font=("Segoe UI", 13)
        )
        descripcion.pack(anchor="w", padx=25, pady=(0, 20))

        lbl_asunto = tk.Label(
            card,
            text="Asunto",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 13, "bold")
        )
        lbl_asunto.pack(anchor="w", padx=25)

        self.entry_asunto = tk.Entry(
            card,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        self.entry_asunto.insert(0, "Ej: Error al registrar venta")
        self.entry_asunto.pack(fill="x", padx=25, pady=(5, 18), ipady=8)

        lbl_descripcion = tk.Label(
            card,
            text="Descripción del problema",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 13, "bold")
        )
        lbl_descripcion.pack(anchor="w", padx=25)

        self.txt_descripcion = tk.Text(
            card,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            height=6
        )
        self.txt_descripcion.insert("1.0", "Describe detalladamente el problema...")
        self.txt_descripcion.pack(fill="x", padx=25, pady=(5, 20))

        btn_enviar = tk.Button(
            card,
            text="Enviar Reporte",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.enviar_reporte_demo
        )
        btn_enviar.pack(anchor="w", padx=25, pady=(0, 25))

    def enviar_reporte_demo(self):
        """
        Simula el envío de reporte de soporte.
        """

        messagebox.showinfo(
            "Soporte",
            "Reporte enviado de forma demostrativa."
        )

    # ==============================
    # CAMBIO DE ROL
    # ==============================

    def simular_cambio_rol(self):
        """
        Cambia entre Administrador y Vendedor.
        """

        if self.rol_usuario == "Administrador":
            self.rol_usuario = "Vendedor"
        else:
            self.rol_usuario = "Administrador"

        if self.contenedor_general is not None:
            self.contenedor_general.destroy()

        self.crear_layout()
        self.mostrar_venta()


# ==============================
# PRUEBA DIRECTA
# ==============================

if __name__ == "__main__":
    class UsuarioPrueba:
        def __init__(self):
            self.nombre = "Administrador"
            self.rol = "Administrador"

    root = tk.Tk()
    root.withdraw()

    ventana = LayoutPrincipal(root, UsuarioPrueba())
    ventana.mainloop()
