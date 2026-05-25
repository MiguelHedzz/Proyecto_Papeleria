# ==============================
#  VENTANA_PRODUCTOS 
# ==============================

"""
Esta pantalla permite administrar productos.

Funciones principales:
- Registrar producto.
- Consultar productos.
- Buscar por código.
- Actualizar producto.
- Eliminar producto.
- Mostrar productos en una tabla.

Esta vista se conecta con:
controllers/producto_controller.py

Diseño basado en el prototipo de Figma:
- Sidebar izquierdo fijo
- Topbar con acciones
- Card blanca para el contenido
- Colores corporativos Dunder Mifflin
"""

import tkinter as tk
from tkinter import ttk, messagebox

from controllers.producto_controller import ProductoController


# ==============================
# CLASE PRINCIPAL DE LA VISTA
# ==============================

class VentanaProductos(tk.Toplevel):
    """
    Esta clase representa la pantalla de administración de productos.

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
        self.title("Dunder Mifflin - Administrar Productos")
        self.geometry("1100x700")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        # Centramos la ventana.
        self._centrar_ventana()

        # Guardamos el usuario (para control de rol si es necesario).
        self.usuario = usuario

        # Controlador de productos.
        self.producto_controller = ProductoController()

        # Variables para el producto seleccionado.
        self.id_producto_seleccionado = None
        self.id_categoria_actual = None
        self.id_proveedor_actual = None

        # Construimos la interfaz completa.
        self._construir_interfaz()

        # Cargamos los productos al iniciar.
        self.cargar_productos()

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

        # ==============================
        # CONTENEDOR PRINCIPAL (FLEX HORIZONTAL)
        # ==============================

        # Frame principal con display flex horizontal.
        self.frame_principal = tk.Frame(self, bg="#e8ecef")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # ==============================
        # SIDEBAR IZQUIERDA
        # ==============================

        self._crear_sidebar()

        # ==============================
        # ÁREA PRINCIPAL (TOPBAR + CONTENT)
        # ==============================

        frame_main = tk.Frame(self.frame_principal, bg="#e8ecef")
        frame_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._crear_topbar(frame_main)
        self._crear_content(frame_main)

    def _crear_sidebar(self):
        """
        Crea la barra lateral izquierda con:
        - Logo / Brand
        - Rol del usuario
        - Navegación (opciones del menú)
        """

        frame_sidebar = tk.Frame(
            self.frame_principal,
            bg="#3a4f63",
            width=240
        )
        frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        frame_sidebar.pack_propagate(False)  # Mantiene el ancho fijo.

        # ===== Brand / Logo =====
        lbl_brand = tk.Label(
            frame_sidebar,
            text="Dunder Mifflin",
            font=("Segoe UI", 20, "bold"),
            bg="#3a4f63",
            fg="white"
        )
        lbl_brand.pack(pady=(40, 10))

        # ===== Rol del usuario =====
        rol_texto = self.usuario.rol if self.usuario else "Administrador"
        lbl_rol = tk.Label(
            frame_sidebar,
            text=f"Rol: {rol_texto}",
            font=("Segoe UI", 11),
            bg="#3a4f63",
            fg="#b0c0d0"
        )
        lbl_rol.pack(pady=(0, 30))

        # ===== Navegación =====
        nav_items = [
            ("Nueva Venta (RF05)", self._ir_a_ventas),
            ("Reportes (RF07)", self._ir_a_reportes),
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

        # NOTA: El botón "Simular Cambio de Rol" NO se incluye.

    def _crear_topbar(self, parent):
        """
        Crea la barra superior con botones de acciones rápidas.
        """

        frame_topbar = tk.Frame(parent, bg="white", height=60)
        frame_topbar.pack(fill=tk.X, side=tk.TOP)
        frame_topbar.pack_propagate(False)

        # Contenedor para botones (alineados a la derecha).
        frame_acciones = tk.Frame(frame_topbar, bg="white")
        frame_acciones.pack(side=tk.RIGHT, padx=20, pady=10)

        # Botón: Gestión Productos (actual, en negrita)
        btn_productos = tk.Button(
            frame_acciones,
            text="Gestión Productos",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            activebackground="#e8ecef",
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_productos.pack(side=tk.LEFT, padx=5)

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
        """
        Crea el área de contenido principal (card blanca con formulario y tabla).
        """

        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # ===== CARD BLANCA =====
        card = tk.Frame(
            frame_content,
            bg="white",
            relief=tk.RAISED,
            bd=1
        )
        card.pack(fill=tk.BOTH, expand=True)

        # ===== TÍTULO DE LA CARD =====
        lbl_titulo = tk.Label(
            card,
            text="Administrar Catálogo (Solo Administrador)",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        # ===== CONTENIDO DE LA CARD =====
        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Formulario ---
        self._crear_formulario(frame_contenido_card)

        # --- Botones de acción ---
        self._crear_botones_accion(frame_contenido_card)

        # --- Tabla de productos ---
        self._crear_tabla(frame_contenido_card)

    def _crear_formulario(self, parent):
        """
        Crea el formulario de productos (campos).
        """

        # Frame para campos en grid (2 filas x 4 columnas).
        frame_campos = tk.Frame(parent, bg="white")
        frame_campos.pack(fill=tk.X, pady=10)

        # Fila 0
        # Nombre
        tk.Label(
            frame_campos, text="Nombre:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_campos, width=25, font=("Segoe UI", 10))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Código
        tk.Label(
            frame_campos, text="Código:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_codigo = tk.Entry(frame_campos, width=15, font=("Segoe UI", 10))
        self.entry_codigo.grid(row=0, column=3, padx=5, pady=5)

        # Precio
        tk.Label(
            frame_campos, text="Precio:", bg="white", font=("Segoe UI", 10)
        ).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.entry_precio = tk.Entry(frame_campos, width=12, font=("Segoe UI", 10))
        self.entry_precio.grid(row=0, column=5, padx=5, pady=5)

        # Fila 1
        # Stock mínimo
        tk.Label(
            frame_campos, text="Stock mínimo:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_stock_minimo = tk.Entry(frame_campos, width=15, font=("Segoe UI", 10))
        self.entry_stock_minimo.grid(row=1, column=1, padx=5, pady=5)

        # Cantidad
        tk.Label(
            frame_campos, text="Cantidad:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_campos, width=15, font=("Segoe UI", 10))
        self.entry_cantidad.grid(row=1, column=3, padx=5, pady=5)

        # Ubicación
        tk.Label(
            frame_campos, text="Ubicación:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.entry_ubicacion = tk.Entry(frame_campos, width=15, font=("Segoe UI", 10))
        self.entry_ubicacion.grid(row=1, column=5, padx=5, pady=5)

    def _crear_botones_accion(self, parent):
        """
        Crea los botones de acción (Agregar, Actualizar, Eliminar, Limpiar)
        y la sección de búsqueda.
        """

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
            command=self.agregar_producto
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
            command=self.actualizar_producto
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
            command=self.eliminar_producto
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
            frame_botones, text="Buscar código:", bg="white", font=("Segoe UI", 10)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_buscar = tk.Entry(frame_botones, width=20, font=("Segoe UI", 10))
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
            command=self.buscar_producto
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
            command=self.cargar_productos
        )
        btn_mostrar_todos.grid(row=1, column=3, padx=5, pady=5)

    def _crear_tabla(self, parent):
        """
        Crea el Treeview para listar productos.
        """

        # Frame contenedor con borde.
        frame_tabla = tk.LabelFrame(
            parent,
            text="Lista de productos",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        columnas = (
            "id",
            "nombre",
            "codigo",
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

        # Configurar encabezados.
        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock_minimo", text="Stock mín.")
        self.tabla_productos.heading("cantidad", text="Cantidad")
        self.tabla_productos.heading("ubicacion", text="Ubicación")

        # Configurar ancho de columnas.
        self.tabla_productos.column("id", width=50, anchor="center")
        self.tabla_productos.column("nombre", width=200)
        self.tabla_productos.column("codigo", width=100, anchor="center")
        self.tabla_productos.column("precio", width=90, anchor="center")
        self.tabla_productos.column("stock_minimo", width=80, anchor="center")
        self.tabla_productos.column("cantidad", width=90, anchor="center")
        self.tabla_productos.column("ubicacion", width=120)

        # Scrollbar.
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento al seleccionar una fila.
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    # ==============================
    # MÉTODOS DE NAVEGACIÓN
    # ==============================

    def _ir_a_ventas(self):
        """Abre la ventana de registro de ventas."""
        from views.ventana_ventas import VentanaVentas
        self.destroy()
        ventana = VentanaVentas(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_reportes(self):
        """Abre la ventana de reportes."""
        from views.ventana_reportes import VentanaReportes
        self.destroy()
        ventana = VentanaReportes(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_soporte(self):
        """Abre la ventana de soporte técnico."""
        from views.ventana_soporte import VentanaSoporte
        ventana = VentanaSoporte(self.master, self.usuario)
        ventana.focus_set()

    # ==============================
    # MÉTODOS DE NEGOCIO (CRUD)
    # ==============================

    def cargar_productos(self):
        """Carga todos los productos en la tabla."""
        # Limpiamos la tabla.
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        productos = self.producto_controller.listar_productos()

        for producto in productos:
            # estructura: 0 id, 1 nombre, 2 codigo, 3 precio, 4 stock_minimo,
            # 5 id_categoria, 6 id_proveedor, 7 cantidad_actual, 8 ubicacion
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto[0],
                    producto[1],
                    producto[2],
                    producto[3],
                    producto[4],
                    producto[7],
                    producto[8]
                )
            )

        self.entry_buscar.delete(0, tk.END)

    def obtener_datos_formulario(self):
        """Obtiene los datos capturados en el formulario."""
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        precio = self.entry_precio.get().strip()
        stock_minimo = self.entry_stock_minimo.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        ubicacion = self.entry_ubicacion.get().strip()

        return nombre, codigo, precio, stock_minimo, cantidad, ubicacion

    def agregar_producto(self):
        """Registra un nuevo producto."""
        nombre, codigo, precio, stock_minimo, cantidad, ubicacion = self.obtener_datos_formulario()

        resultado, mensaje = self.producto_controller.registrar_producto(
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            stock_minimo=stock_minimo,
            cantidad_inicial=cantidad,
            ubicacion=ubicacion
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_producto(self, event):
        """Carga los datos del producto seleccionado en el formulario."""
        seleccion = self.tabla_productos.selection()

        if not seleccion:
            return

        valores = self.tabla_productos.item(seleccion[0], "values")

        self.id_producto_seleccionado = valores[0]

        # Buscar producto completo para obtener categoría y proveedor.
        producto_completo = self.producto_controller.buscar_por_id(
            self.id_producto_seleccionado
        )

        if producto_completo:
            self.id_categoria_actual = producto_completo[5]
            self.id_proveedor_actual = producto_completo[6]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(0, valores[2])

        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, valores[3])

        self.entry_stock_minimo.delete(0, tk.END)
        self.entry_stock_minimo.insert(0, valores[4])

        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, valores[5])

        self.entry_ubicacion.delete(0, tk.END)
        self.entry_ubicacion.insert(0, valores[6])

    def actualizar_producto(self):
        """Actualiza el producto seleccionado."""
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
            return

        nombre, codigo, precio, stock_minimo, cantidad, ubicacion = self.obtener_datos_formulario()

        # Actualizar datos del producto.
        resultado, mensaje = self.producto_controller.actualizar_producto(
            id_producto=self.id_producto_seleccionado,
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            stock_minimo=stock_minimo,
            id_categoria=self.id_categoria_actual,
            id_proveedor=self.id_proveedor_actual
        )

        if not resultado:
            messagebox.showerror("Error", mensaje)
            return

        # Actualizar inventario.
        resultado_inv, mensaje_inv = self.producto_controller.actualizar_inventario(
            id_producto=self.id_producto_seleccionado,
            nueva_cantidad=cantidad,
            nueva_ubicacion=ubicacion
        )

        if resultado_inv:
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje_inv)

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto de la tabla.")
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
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar_producto(self):
        """Busca un producto por código y lo muestra en la tabla."""
        codigo = self.entry_buscar.get().strip()

        if codigo == "":
            messagebox.showwarning("Aviso", "Ingresa un código para buscar.")
            return

        producto = self.producto_controller.buscar_por_codigo(codigo)

        # Limpiar tabla.
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        if producto:
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto[0],
                    producto[1],
                    producto[2],
                    producto[3],
                    producto[4],
                    producto[7],
                    producto[8]
                )
            )
        else:
            messagebox.showinfo("Sin resultados", "No se encontró un producto con ese código.")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.id_producto_seleccionado = None
        self.id_categoria_actual = None
        self.id_proveedor_actual = None

        self.entry_nombre.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock_minimo.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)

        self.tabla_productos.selection_remove(
            self.tabla_productos.selection()
        )


# ==============================
# EJECUCIÓN DIRECTA PARA PRUEBAS
# ==============================

if __name__ == "__main__":
    # Prueba sin usuario (se muestra como Administrador)
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana raíz
    ventana = VentanaProductos(root)
    ventana.mainloop()
