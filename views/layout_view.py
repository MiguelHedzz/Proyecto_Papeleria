# ==============================
# LAYOUT PRINCIPAL DEL SISTEMA
# ==============================

"""
Este archivo contiene el diseño base del sistema segun el prototipo de Figma.

Incluye:
- Sidebar izquierdo azul oscuro.
- Topbar superior blanca.
- Area principal gris claro.
- Card blanca central.
- Pantallas internas: Nueva Venta, Productos, Categorias, Proveedores, Inventario, Reportes y Soporte.
"""

import os
import sys
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.producto_controller import ProductoController
from services.venta_service import VentaService
from services.reporte_service import ReporteService
from database.conexion import conectar_bd


class LayoutPrincipal(tk.Toplevel):
    """
    Ventana principal del sistema despues del login.
    
    Esta ventana contiene el diseño completo con sidebar y topbar,
    y gestiona todas las pantallas internas del sistema.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.parent = parent
        self.usuario = usuario

        self.nombre_usuario = self.obtener_nombre_usuario()
        self.rol_usuario = self.obtener_rol_usuario()
        self.id_usuario = self.obtener_id_usuario()

        self.title("Dunder Mifflin - Sistema de Inventario")
        self.geometry("1280x720")
        self.minsize(1100, 650)
        self.configure(bg="#ecf0f1")

        # Colores del prototipo
        self.color_sidebar = "#2c3e50"
        self.color_sidebar_boton = "#34495e"
        self.color_fondo = "#ecf0f1"
        self.color_card = "white"
        self.color_texto = "#2c3e50"
        self.color_naranja = "#e67e22"
        self.color_gris = "#95a5a6"
        self.color_rojo = "#e74c3c"
        self.color_verde = "#27ae60"
        self.color_azul = "#3498db"

        # Controladores y servicios
        self.producto_controller = ProductoController()
        self.venta_service = VentaService()
        self.reporte_service = ReporteService()

        # Variables de venta
        self.carrito = []
        self.total_venta = 0.0
        self.productos_combo = []

        # Construir interfaz
        self.crear_layout()
        self.mostrar_venta()

    # ==============================
    # DATOS DEL USUARIO
    # ==============================

    def obtener_id_usuario(self):
        """
        Obtiene el ID del usuario autenticado.
        
        Puede recibir el usuario como objeto, diccionario, tupla o lista.
        Si no se encuentra, retorna 1 como valor por defecto.
        """
        if self.usuario is None:
            return 1
        if hasattr(self.usuario, "id_usuario"):
            return self.usuario.id_usuario
        if isinstance(self.usuario, dict):
            return self.usuario.get("id_usuario", 1)
        if isinstance(self.usuario, (tuple, list)) and len(self.usuario) > 0:
            return self.usuario[0]
        return 1

    def obtener_nombre_usuario(self):
        """
        Obtiene el nombre del usuario autenticado.
        
        Retorna el nombre si existe, o 'Usuario' como valor por defecto.
        """
        if self.usuario is None:
            return "Usuario"
        if hasattr(self.usuario, "nombre"):
            return self.usuario.nombre
        if isinstance(self.usuario, dict):
            return self.usuario.get("nombre", "Usuario")
        if isinstance(self.usuario, (tuple, list)) and len(self.usuario) > 1:
            return self.usuario[1]
        return "Usuario"

    def obtener_rol_usuario(self):
        """
        Obtiene el rol del usuario autenticado.
        
        Retorna el rol si existe, o 'Administrador' como valor por defecto.
        """
        if self.usuario is None:
            return "Administrador"
        if hasattr(self.usuario, "rol"):
            return self.usuario.rol
        if isinstance(self.usuario, dict):
            return self.usuario.get("rol", "Administrador")
        if isinstance(self.usuario, (tuple, list)) and len(self.usuario) > 3:
            return self.usuario[3]
        return "Administrador"

    # ==============================
    # LAYOUT GENERAL
    # ==============================

    def crear_layout(self):
        """
        Crea la estructura principal de la ventana.
        
        La estructura se compone de:
        - Sidebar izquierdo (menu de navegacion)
        - Area derecha (topbar + contenido)
        """
        self.contenedor_general = tk.Frame(self, bg=self.color_fondo)
        self.contenedor_general.pack(fill="both", expand=True)

        self.crear_sidebar()
        self.area_derecha = tk.Frame(self.contenedor_general, bg=self.color_fondo)
        self.area_derecha.pack(side="left", fill="both", expand=True)
        self.crear_topbar()
        self.area_contenido = tk.Frame(self.area_derecha, bg=self.color_fondo)
        self.area_contenido.pack(fill="both", expand=True)

    # ==============================
    # SIDEBAR
    # ==============================

    def crear_sidebar(self):
        """
        Crea el menu lateral izquierdo.
        
        El sidebar contiene:
        - Titulo del sistema
        - Rol del usuario actual
        - Botones de navegacion segun el rol
        - Boton de cerrar sesion al final
        """
        self.sidebar = tk.Frame(self.contenedor_general, bg=self.color_sidebar, width=255)
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
        rol.pack(anchor="w", padx=20, pady=(0, 35))

        # Botones del menu
        self.crear_boton_sidebar("Nueva Venta", self.mostrar_venta)

        if self.rol_usuario == "Administrador":
            self.crear_boton_sidebar("Productos", self.mostrar_productos)
            self.crear_boton_sidebar("Categorias", self.mostrar_categorias)
            self.crear_boton_sidebar("Proveedores", self.mostrar_proveedores)
            self.crear_boton_sidebar("Inventario", self.mostrar_inventario)
            self.crear_boton_sidebar("Reportes", self.mostrar_reportes)

        # Espacio flexible para empujar el boton de cerrar sesion hacia abajo
        espacio = tk.Frame(self.sidebar, bg=self.color_sidebar)
        espacio.pack(fill="both", expand=True)

        # Boton Cerrar Sesion al final del sidebar
        self.crear_boton_sidebar("Cerrar Sesion", self.cerrar_sesion, color="#c0392b")

    def crear_boton_sidebar(self, texto, comando, color=None):
        """
        Crea un boton del menu lateral.
        
        Parametros:
        texto: Texto que mostrara el boton
        comando: Funcion a ejecutar al hacer clic
        color: Color de fondo del boton (opcional)
        """
        if color is None:
            color = self.color_sidebar_boton
        boton = tk.Button(
            self.sidebar,
            text=texto,
            bg=color,
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
        
        La topbar contiene:
        - Nombre del usuario actual
        - Botones de acceso rapido (Soporte, Usuarios)
        """
        self.topbar = tk.Frame(self.area_derecha, bg="white", height=65)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        lbl_usuario = tk.Label(
            self.topbar,
            text=f"Usuario: {self.nombre_usuario}",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 11)
        )
        lbl_usuario.pack(side="left", padx=25)

        btn_soporte = self.crear_boton_topbar("Soporte", self.mostrar_soporte)
        btn_soporte.pack(side="right", padx=(10, 25), pady=12)

        if self.rol_usuario == "Administrador":
            btn_usuarios = self.crear_boton_topbar("Usuarios", self.mostrar_usuarios)
            btn_usuarios.pack(side="right", padx=(10, 5), pady=12)

    def crear_boton_topbar(self, texto, comando):
        """
        Crea un boton de la barra superior.
        """
        return tk.Button(
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

    # ==============================
    # CONTENIDO DINAMICO
    # ==============================

    def limpiar_contenido(self):
        """Elimina todos los widgets del area de contenido."""
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    def crear_card(self):
        """
        Crea una tarjeta blanca central para el contenido.
        
        Retorna el frame de la tarjeta creada.
        """
        self.limpiar_contenido()
        card = tk.Frame(self.area_contenido, bg=self.color_card, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=35, pady=35)
        self.card_actual = card
        return card

    # ==============================
    # CERRAR SESION
    # ==============================

    def cerrar_sesion(self):
        """
        Cierra la sesion actual y vuelve a la pantalla de login.
        
        Muestra un mensaje de confirmacion antes de cerrar.
        """
        confirmar = messagebox.askyesno("Cerrar Sesion", "Seguro que deseas cerrar sesion?")
        if confirmar:
            self.destroy()
            if self.parent:
                self.parent.deiconify()

    # ==============================
    # PANTALLA NUEVA VENTA
    # ==============================

    def mostrar_venta(self):
        """
        Muestra la pantalla de nueva venta.
        
        Esta pantalla permite:
        - Seleccionar productos del catalogo
        - Agregar productos al carrito
        - Eliminar productos del carrito
        - Seleccionar metodo de pago (Efectivo o Tarjeta)
        - Confirmar la venta y generar ticket
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

        # Frame principal con dos columnas
        frame_principal = tk.Frame(card, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=25)

        # Columna izquierda - Seleccion de productos
        frame_izquierda = tk.Frame(frame_principal, bg="white")
        frame_izquierda.pack(side="left", fill="both", expand=True, padx=(0, 15))

        lbl_buscar = tk.Label(
            frame_izquierda,
            text="Seleccionar Producto",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 14, "bold")
        )
        lbl_buscar.pack(anchor="w", pady=(0, 10))

        # Cargar productos
        productos = self.producto_controller.listar_productos()
        self.productos_combo = productos

        valores_combo = []
        for producto in productos:
            cantidad = producto[7] if len(producto) > 7 else 0
            valores_combo.append(
                f"{producto[0]} - {producto[1]} (${producto[3]}) | Stock: {cantidad}"
            )

        self.combo_producto_venta = ttk.Combobox(
            frame_izquierda,
            values=valores_combo,
            state="readonly",
            font=("Segoe UI", 11)
        )
        self.combo_producto_venta.pack(fill="x", pady=(0, 15), ipady=5)

        frame_cantidad = tk.Frame(frame_izquierda, bg="white")
        frame_cantidad.pack(fill="x", pady=(0, 15))

        lbl_cantidad = tk.Label(
            frame_cantidad,
            text="Cantidad:",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 12, "bold")
        )
        lbl_cantidad.pack(side="left", padx=(0, 10))

        self.entry_cantidad_venta = tk.Entry(
            frame_cantidad,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            width=10
        )
        self.entry_cantidad_venta.insert(0, "1")
        self.entry_cantidad_venta.pack(side="left", padx=(0, 10), ipady=5)

        btn_agregar = tk.Button(
            frame_cantidad,
            text="Agregar al Carrito",
            bg=self.color_naranja,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.agregar_producto_carrito
        )
        btn_agregar.pack(side="left")

        # Columna derecha - Carrito y pago
        frame_derecha = tk.Frame(frame_principal, bg="white")
        frame_derecha.pack(side="right", fill="both", expand=True, padx=(15, 0))

        lbl_carrito = tk.Label(
            frame_derecha,
            text="Carrito de Venta",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 14, "bold")
        )
        lbl_carrito.pack(anchor="w", pady=(0, 10))

        # Frame para la tabla y boton eliminar
        frame_tabla_carrito = tk.Frame(frame_derecha, bg="white")
        frame_tabla_carrito.pack(fill="both", expand=True, pady=(0, 10))

        columnas = ("id", "producto", "cantidad", "precio", "subtotal")
        self.tabla_carrito = ttk.Treeview(
            frame_tabla_carrito,
            columns=columnas,
            show="headings",
            height=6
        )

        self.tabla_carrito.heading("id", text="ID")
        self.tabla_carrito.heading("producto", text="Producto")
        self.tabla_carrito.heading("cantidad", text="Cant.")
        self.tabla_carrito.heading("precio", text="Precio")
        self.tabla_carrito.heading("subtotal", text="Subtotal")

        self.tabla_carrito.column("id", width=50, anchor="center")
        self.tabla_carrito.column("producto", width=200)
        self.tabla_carrito.column("cantidad", width=80, anchor="center")
        self.tabla_carrito.column("precio", width=90, anchor="center")
        self.tabla_carrito.column("subtotal", width=90, anchor="center")

        self.tabla_carrito.pack(side="left", fill="both", expand=True)

        scrollbar_carrito = ttk.Scrollbar(frame_tabla_carrito, orient="vertical", command=self.tabla_carrito.yview)
        scrollbar_carrito.pack(side="right", fill="y")
        self.tabla_carrito.configure(yscrollcommand=scrollbar_carrito.set)

        # Boton eliminar del carrito
        btn_eliminar = tk.Button(
            frame_derecha,
            text="Eliminar seleccionado",
            bg=self.color_rojo,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.eliminar_del_carrito
        )
        btn_eliminar.pack(anchor="w", pady=(0, 10))

        self.lbl_total = tk.Label(
            frame_derecha,
            text="Total: $0.00",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 18, "bold")
        )
        self.lbl_total.pack(anchor="e", pady=(0, 15))

        # Metodo de pago
        frame_pago = tk.Frame(frame_derecha, bg="white")
        frame_pago.pack(fill="x", pady=(0, 15))

        lbl_metodo = tk.Label(
            frame_pago,
            text="Metodo de Pago:",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 12, "bold")
        )
        lbl_metodo.pack(side="left", padx=(0, 15))

        self.combo_metodo_pago = ttk.Combobox(
            frame_pago,
            values=["Efectivo", "Tarjeta"],
            state="readonly",
            font=("Segoe UI", 11),
            width=15
        )
        self.combo_metodo_pago.set("Efectivo")
        self.combo_metodo_pago.pack(side="left")

        btn_confirmar = tk.Button(
            frame_derecha,
            text="Confirmar Venta",
            bg=self.color_verde,
            fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.confirmar_venta
        )
        btn_confirmar.pack(fill="x", pady=(10, 0))

    def obtener_producto_combo(self):
        """
        Obtiene el producto seleccionado en el combobox.
        
        Retorna el producto como tupla o None si no hay seleccion.
        """
        seleccionado = self.combo_producto_venta.get()
        if not seleccionado:
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
        Agrega un producto al carrito de venta.
        
        Valida que haya stock suficiente antes de agregar.
        Si el producto ya existe en el carrito, acumula la cantidad.
        """
        producto = self.obtener_producto_combo()
        if not producto:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        try:
            cantidad = int(self.entry_cantidad_venta.get().strip())
        except ValueError:
            messagebox.showwarning("Aviso", "La cantidad debe ser un numero entero.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Aviso", "La cantidad debe ser mayor que cero.")
            return

        id_producto = int(producto[0])
        nombre = producto[1]
        precio = float(producto[3])
        stock_actual = producto[7] if len(producto) > 7 else 0

        # Calcular cantidad total en carrito + nueva cantidad
        cantidad_en_carrito = 0
        for item in self.carrito:
            if item["id_producto"] == id_producto:
                cantidad_en_carrito += item["cantidad"]

        cantidad_total = cantidad_en_carrito + cantidad

        if cantidad_total > stock_actual:
            messagebox.showwarning(
                "Stock insuficiente",
                f"Stock disponible: {stock_actual}\n"
                f"Ya tienes {cantidad_en_carrito} en el carrito.\n"
                f"No puedes agregar {cantidad} mas."
            )
            return

        # Verificar si el producto ya esta en el carrito
        encontrado = False
        for item in self.carrito:
            if item["id_producto"] == id_producto:
                item["cantidad"] += cantidad
                item["subtotal"] = item["cantidad"] * item["precio"]
                encontrado = True
                break

        if not encontrado:
            self.carrito.append({
                "id_producto": id_producto,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": cantidad * precio
            })

        # Recalcular total
        self.total_venta = sum(item["subtotal"] for item in self.carrito)

        # Actualizar tabla
        self.actualizar_tabla_carrito()

        self.lbl_total.config(text=f"Total: ${self.total_venta:.2f}")
        self.entry_cantidad_venta.delete(0, tk.END)
        self.entry_cantidad_venta.insert(0, "1")

    def actualizar_tabla_carrito(self):
        """Actualiza la tabla del carrito con los productos actuales."""
        for fila in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(fila)

        for item in self.carrito:
            self.tabla_carrito.insert(
                "", "end",
                values=(
                    item["id_producto"],
                    item["nombre"],
                    item["cantidad"],
                    f"${item['precio']:.2f}",
                    f"${item['subtotal']:.2f}"
                )
            )

    def eliminar_del_carrito(self):
        """
        Elimina un producto seleccionado del carrito.
        """
        seleccion = self.tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito para eliminar.")
            return

        valores = self.tabla_carrito.item(seleccion[0], "values")
        id_producto = int(valores[0])

        self.carrito = [item for item in self.carrito if item["id_producto"] != id_producto]
        self.total_venta = sum(item["subtotal"] for item in self.carrito)

        self.actualizar_tabla_carrito()
        self.lbl_total.config(text=f"Total: ${self.total_venta:.2f}")

    def confirmar_venta(self):
        """
        Confirma la venta y la registra en la base de datos.
        
        Realiza las siguientes acciones:
        - Valida que el carrito no este vacio
        - Obtiene el metodo de pago seleccionado
        - Registra la venta en la base de datos
        - Descuenta el inventario
        - Genera alertas de stock bajo
        - Muestra el ticket de venta
        """
        if not self.carrito:
            messagebox.showwarning("Carrito vacio", "Agrega al menos un producto.")
            return

        metodo_pago = self.combo_metodo_pago.get()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO venta (fecha, total, id_usuario, metodo_pago)
                VALUES (?, ?, ?, ?)
            """, (fecha, self.total_venta, self.id_usuario, metodo_pago))

            id_venta = cursor.lastrowid

            for item in self.carrito:
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal)
                    VALUES (?, ?, ?, ?)
                """, (id_venta, item["id_producto"], item["cantidad"], item["subtotal"]))

                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = cantidad_actual - ?
                    WHERE id_producto = ?
                """, (item["cantidad"], item["id_producto"]))

                # Verificar stock bajo y generar alerta
                cursor.execute("""
                    SELECT cantidad_actual, stock_minimo
                    FROM inventario i
                    JOIN producto p ON i.id_producto = p.id_producto
                    WHERE i.id_producto = ?
                """, (item["id_producto"],))
                resultado_stock = cursor.fetchone()

                if resultado_stock and resultado_stock[0] <= resultado_stock[1]:
                    cursor.execute("""
                        SELECT COUNT(*) FROM alerta
                        WHERE id_producto = ? AND atendida = 0
                    """, (item["id_producto"],))
                    existe_alerta = cursor.fetchone()[0]

                    if existe_alerta == 0:
                        cursor.execute("""
                            INSERT INTO alerta (id_producto, mensaje, atendida)
                            VALUES (?, ?, 0)
                        """, (item["id_producto"], f"Stock bajo: {item['nombre']}. Quedan {resultado_stock[0]} unidades."))

            conexion.commit()
            conexion.close()

            self.mostrar_ticket(id_venta)

            messagebox.showinfo("Exito", f"Venta registrada correctamente.\nTotal: ${self.total_venta:.2f}\nMetodo de pago: {metodo_pago}")

            self.mostrar_venta()

        except Exception as error:
            messagebox.showerror("Error", f"No se pudo registrar la venta.\n\nDetalle: {error}")

    def mostrar_ticket(self, id_venta):
        """
        Muestra un ticket de venta en una ventana emergente.
        
        Parametro:
        id_venta: Identificador de la venta registrada.
        """
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT v.id_venta, v.fecha, v.total, u.nombre, v.metodo_pago
                FROM venta v
                JOIN usuario u ON v.id_usuario = u.id_usuario
                WHERE v.id_venta = ?
            """, (id_venta,))
            venta = cursor.fetchone()

            cursor.execute("""
                SELECT p.nombre, dv.cantidad, dv.subtotal
                FROM detalle_venta dv
                JOIN producto p ON dv.id_producto = p.id_producto
                WHERE dv.id_venta = ?
            """, (id_venta,))
            detalles = cursor.fetchall()
            conexion.close()

            ticket = "=" * 40 + "\n"
            ticket += "     DUNDER MIFFLIN\n"
            ticket += "     Ticket de Venta\n"
            ticket += "=" * 40 + "\n"
            ticket += f"Venta #: {venta[0]}\n"
            ticket += f"Fecha: {venta[1]}\n"
            ticket += f"Vendedor: {venta[3]}\n"
            ticket += f"Pago: {venta[4]}\n"
            ticket += "-" * 40 + "\n"
            ticket += "Producto     Cant.     Subtotal\n"
            ticket += "-" * 40 + "\n"
            for detalle in detalles:
                nombre = detalle[0][:15]
                ticket += f"{nombre:<12} {detalle[1]:>3}     ${detalle[2]:>8.2f}\n"
            ticket += "-" * 40 + "\n"
            ticket += f"TOTAL: ${venta[2]:>33.2f}\n"
            ticket += "=" * 40 + "\n"
            ticket += "     Gracias por su compra\n"

            ventana_ticket = tk.Toplevel(self)
            ventana_ticket.title("Ticket de Venta")
            ventana_ticket.geometry("400x500")
            ventana_ticket.configure(bg="white")

            texto_ticket = tk.Text(ventana_ticket, font=("Courier", 10), bg="white", wrap="none")
            texto_ticket.insert("1.0", ticket)
            texto_ticket.config(state="disabled")
            texto_ticket.pack(fill="both", expand=True, padx=10, pady=10)

            btn_cerrar = tk.Button(ventana_ticket, text="Cerrar", command=ventana_ticket.destroy)
            btn_cerrar.pack(pady=10)

        except Exception as e:
            print(f"Error al generar ticket: {e}")

    # ==============================
    # PANTALLA PRODUCTOS
    # ==============================

    def mostrar_productos(self):
        """Abre la ventana de gestion de productos."""
        from views.productos_view import ProductosView
        ventana = ProductosView(self, self.usuario)
        ventana.focus_set()

    # ==============================
    # PANTALLA CATEGORIAS
    # ==============================

    def mostrar_categorias(self):
        """Abre la ventana de gestion de categorias."""
        from views.categorias_view import CategoriasView
        ventana = CategoriasView(self, self.usuario)
        ventana.focus_set()

    # ==============================
    # PANTALLA PROVEEDORES
    # ==============================

    def mostrar_proveedores(self):
        """Abre la ventana de gestion de proveedores."""
        from views.proveedores_view import ProveedoresView
        ventana = ProveedoresView(self, self.usuario)
        ventana.focus_set()

    # ==============================
    # PANTALLA INVENTARIO
    # ==============================

    def mostrar_inventario(self):
        """Abre la ventana de gestion de inventario."""
        from views.inventario_view import InventarioView
        ventana = InventarioView(self, self.usuario)
        ventana.focus_set()

    # ==============================
    # PANTALLA USUARIOS
    # ==============================

    def mostrar_usuarios(self):
        """Abre la ventana de gestion de usuarios."""
        from views.usuarios_view import VentanaUsuarios
        ventana = VentanaUsuarios(self, self.usuario)
        ventana.focus_set()

    # ==============================
    # PANTALLA REPORTES
    # ==============================

    def mostrar_reportes(self):
        """
        Muestra la pantalla de reportes del sistema.
        
        Los reportes incluyen:
        - Resumen general (productos, ventas, ingresos, stock bajo)
        - Tabla de productos con stock bajo
        - Tabla de ventas realizadas
        - Tabla de productos registrados
        - Botones para exportar a CSV
        """
        if self.rol_usuario != "Administrador":
            messagebox.showwarning("Acceso denegado", "Solo el administrador puede ver reportes.")
            return

        card = self.crear_card()

        titulo = tk.Label(
            card,
            text="Reportes del Sistema",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(anchor="w", padx=25, pady=(25, 20))

        # Botones de exportacion
        frame_exportar = tk.Frame(card, bg="white")
        frame_exportar.pack(fill="x", padx=25, pady=(0, 15))

        btn_exportar_stock = tk.Button(
            frame_exportar,
            text="Exportar Stock Bajo a CSV",
            bg=self.color_azul,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.exportar_stock_bajo_csv
        )
        btn_exportar_stock.pack(side="left", padx=(0, 10))

        btn_exportar_ventas = tk.Button(
            frame_exportar,
            text="Exportar Ventas a CSV",
            bg=self.color_azul,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.exportar_ventas_csv
        )
        btn_exportar_ventas.pack(side="left", padx=(0, 10))

        btn_exportar_productos = tk.Button(
            frame_exportar,
            text="Exportar Productos a CSV",
            bg=self.color_azul,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.exportar_productos_csv
        )
        btn_exportar_productos.pack(side="left")

        try:
            resumen = self.reporte_service.resumen_general()
        except Exception:
            resumen = {}

        frame_resumen = tk.Frame(card, bg="white")
        frame_resumen.pack(fill="x", padx=25, pady=(0, 20))

        tarjetas = [
            ("Productos", resumen.get("total_productos", 0), self.color_naranja),
            ("Ventas", resumen.get("total_ventas", 0), self.color_verde),
            ("Ingresos", f"${float(resumen.get('total_ingresos', 0)):.2f}", self.color_texto),
            ("Stock bajo", resumen.get("productos_stock_bajo", 0), self.color_rojo),
        ]

        for titulo_tarjeta, valor, color in tarjetas:
            tarjeta = tk.Frame(frame_resumen, bg="#f8f9fa", relief="solid", bd=1, padx=15, pady=12)
            tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 12))
            tk.Label(tarjeta, text=titulo_tarjeta, bg="#f8f9fa", fg=self.color_texto, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(tarjeta, text=str(valor), bg="#f8f9fa", fg=color, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(5, 0))

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
        tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=8)
        for col, text in [("id", "ID"), ("nombre", "Nombre"), ("codigo", "Codigo"),
                          ("stock_minimo", "Stock min."), ("cantidad", "Cantidad"),
                          ("ubicacion", "Ubicacion")]:
            tabla.heading(col, text=text)
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
        columnas = ("id", "fecha", "total", "usuario", "metodo_pago")
        tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=8)
        tabla.heading("id", text="ID")
        tabla.heading("fecha", text="Fecha")
        tabla.heading("total", text="Total")
        tabla.heading("usuario", text="Usuario")
        tabla.heading("metodo_pago", text="Metodo Pago")
        tabla.column("id", width=60, anchor="center")
        tabla.column("fecha", width=180)
        tabla.column("total", width=100, anchor="center")
        tabla.column("usuario", width=150)
        tabla.column("metodo_pago", width=100, anchor="center")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT v.id_venta, v.fecha, v.total, u.nombre, v.metodo_pago
                FROM venta v
                LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
                ORDER BY v.fecha DESC
            """)
            datos = cursor.fetchall()
            conexion.close()
        except Exception:
            datos = []
        for venta in datos:
            metodo = venta[4] if len(venta) > 4 and venta[4] else "Efectivo"
            tabla.insert("", "end", values=(venta[0], venta[1], f"${venta[2]:.2f}", venta[3], metodo))

    def crear_tabla_productos_reporte(self, parent):
        """
        Crea la tabla de productos registrados.
        """
        columnas = ("id", "codigo", "nombre", "precio", "cantidad")
        tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=8)
        tabla.heading("id", text="ID")
        tabla.heading("codigo", text="Codigo")
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
            tabla.insert("", "end", values=(producto[0], producto[2], producto[1], f"${producto[3]:.2f}", cantidad))

    # ==============================
    # EXPORTAR REPORTES A CSV
    # ==============================

    def exportar_stock_bajo_csv(self):
        """
        Exporta la lista de productos con stock bajo a un archivo CSV.
        """
        try:
            datos = self.reporte_service.reporte_stock_bajo()
            if not datos:
                messagebox.showwarning("Sin datos", "No hay productos con stock bajo para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"stock_bajo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if archivo:
                with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Nombre", "Codigo", "Stock Minimo", "Cantidad Actual", "Ubicacion"])
                    writer.writerows(datos)
                messagebox.showinfo("Exito", f"Reporte exportado a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    def exportar_ventas_csv(self):
        """
        Exporta la lista de ventas a un archivo CSV.
        """
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT v.id_venta, v.fecha, v.total, u.nombre, v.metodo_pago
                FROM venta v
                LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
                ORDER BY v.fecha DESC
            """)
            datos = cursor.fetchall()
            conexion.close()

            if not datos:
                messagebox.showwarning("Sin datos", "No hay ventas registradas para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if archivo:
                with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID Venta", "Fecha", "Total", "Usuario", "Metodo Pago"])
                    for venta in datos:
                        metodo = venta[4] if len(venta) > 4 and venta[4] else "Efectivo"
                        writer.writerow([venta[0], venta[1], f"${venta[2]:.2f}", venta[3], metodo])
                messagebox.showinfo("Exito", f"Reporte exportado a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    def exportar_productos_csv(self):
        """
        Exporta la lista de productos a un archivo CSV.
        """
        try:
            datos = self.reporte_service.reporte_productos()
            if not datos:
                messagebox.showwarning("Sin datos", "No hay productos registrados para exportar.")
                return

            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if archivo:
                with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Nombre", "Codigo", "Precio", "Stock Minimo", "Cantidad Actual", "Ubicacion"])
                    for producto in datos:
                        cantidad = producto[7] if len(producto) > 7 else 0
                        ubicacion = producto[8] if len(producto) > 8 else ""
                        writer.writerow([producto[0], producto[1], producto[2], producto[3], producto[4], cantidad, ubicacion])
                messagebox.showinfo("Exito", f"Reporte exportado a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    # ==============================
    # PANTALLA SOPORTE
    # ==============================

    def mostrar_soporte(self):
        """
        Muestra la pantalla de soporte tecnico.
        
        Permite al usuario enviar un reporte de problema
        de manera demostrativa.
        """
        card = self.crear_card()

        titulo = tk.Label(
            card,
            text="Soporte Tecnico",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(anchor="w", padx=25, pady=(25, 20))

        descripcion = tk.Label(
            card,
            text="Tienes problemas con el sistema? Describe tu situacion y envia un reporte.",
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

        self.entry_asunto = tk.Entry(card, font=("Segoe UI", 11), relief="solid", bd=1)
        self.entry_asunto.insert(0, "Ej: Error al registrar venta")
        self.entry_asunto.pack(fill="x", padx=25, pady=(5, 18), ipady=8)

        lbl_descripcion = tk.Label(
            card,
            text="Descripcion del problema",
            bg="white",
            fg=self.color_texto,
            font=("Segoe UI", 13, "bold")
        )
        lbl_descripcion.pack(anchor="w", padx=25)

        self.txt_descripcion = tk.Text(card, font=("Segoe UI", 11), relief="solid", bd=1, height=6)
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
            width=20,
            height=2,
            command=self.enviar_reporte_demo
        )
        btn_enviar.pack(anchor="w", padx=25, pady=(0, 25))

    def enviar_reporte_demo(self):
        """
        Envia un reporte de soporte de manera demostrativa.
        """
        asunto = self.entry_asunto.get().strip()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()
        messagebox.showinfo("Soporte", f"Reporte enviado.\n\nAsunto: {asunto}\n\nEl equipo de soporte revisara tu caso.")


if __name__ == "__main__":
    class UsuarioPrueba:
        def __init__(self):
            self.nombre = "Administrador"
            self.rol = "Administrador"

    root = tk.Tk()
    root.withdraw()
    ventana = LayoutPrincipal(root, UsuarioPrueba())
    ventana.mainloop()