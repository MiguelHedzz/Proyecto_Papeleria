# ==============================
# VISTA DE INVENTARIO
# ==============================

"""
Esta pantalla permite controlar el inventario de productos.

Funciones principales:
- Ver listado de productos con stock actual.
- Registrar entrada de productos.
- Registrar salida de productos.
- Actualizar ubicación.
- Ver productos con stock bajo.

Esta vista se conecta con:
controllers/inventario_controller.py
services/inventario_service.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from services.inventario_service import InventarioService
from controllers.producto_controller import ProductoController


class InventarioView(tk.Toplevel):
    """Pantalla de control de inventario."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Control de Inventario")
        self.geometry("1100x700")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario = usuario
        self.inventario_service = InventarioService()
        self.producto_controller = ProductoController()

        self.id_producto_seleccionado = None
        self.productos_map = {}

        self._construir_interfaz()
        self._cargar_productos_combo()
        self.cargar_inventario()

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
            ("Proveedores", self._ir_a_proveedores),
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

        btn_inventario = tk.Button(frame_acciones, text="Control de Inventario", font=("Segoe UI", 10, "bold"),
                                   bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_inventario.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Control de Inventario", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._crear_formulario(frame_contenido_card)
        self._crear_botones_accion(frame_contenido_card)
        self._crear_tabla(frame_contenido_card)

    def _crear_formulario(self, parent):
        frame_campos = tk.Frame(parent, bg="white")
        frame_campos.pack(fill=tk.X, pady=10)

        tk.Label(frame_campos, text="Producto:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_productos = ttk.Combobox(frame_campos, width=40, font=("Segoe UI", 10))
        self.combo_productos.grid(row=0, column=1, padx=5, pady=5)
        self.combo_productos.bind("<<ComboboxSelected>>", self._cargar_producto_seleccionado)

        tk.Label(frame_campos, text="Cantidad:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_campos, width=20, font=("Segoe UI", 10))
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_campos, text="Ubicación:", bg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_ubicacion = tk.Entry(frame_campos, width=40, font=("Segoe UI", 10))
        self.entry_ubicacion.grid(row=2, column=1, padx=5, pady=5)

        self.lbl_stock_actual = tk.Label(frame_campos, text="Stock actual: --", bg="white", font=("Segoe UI", 10), fg="#2c3e50")
        self.lbl_stock_actual.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    def _cargar_productos_combo(self):
        productos = self.producto_controller.listar_productos()
        self.productos_map = {}
        lista_productos = []

        for p in productos:
            nombre = p[1]
            codigo = p[2]
            self.productos_map[f"{nombre} ({codigo})"] = p[0]
            lista_productos.append(f"{nombre} ({codigo})")

        self.combo_productos['values'] = lista_productos
        if lista_productos:
            self.combo_productos.current(0)
            self._cargar_producto_seleccionado()

    def _cargar_producto_seleccionado(self, event=None):
        seleccion = self.combo_productos.get()
        if seleccion and seleccion in self.productos_map:
            id_producto = self.productos_map[seleccion]
            self.id_producto_seleccionado = id_producto
            stock = self.inventario_service.consultar_stock(id_producto)
            self.lbl_stock_actual.config(text=f"Stock actual: {stock} unidades")

    def _crear_botones_accion(self, parent):
        frame_botones = tk.Frame(parent, bg="white")
        frame_botones.pack(fill=tk.X, pady=15)

        btn_entrada = tk.Button(frame_botones, text="Registrar Entrada (+)", font=("Segoe UI", 10, "bold"),
                                bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                relief=tk.FLAT, padx=15, command=self.registrar_entrada)
        btn_entrada.grid(row=0, column=0, padx=5, pady=5)

        btn_salida = tk.Button(frame_botones, text="Registrar Salida (-)", font=("Segoe UI", 10, "bold"),
                               bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                               relief=tk.FLAT, padx=15, command=self.registrar_salida)
        btn_salida.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar_ubicacion = tk.Button(frame_botones, text="Actualizar Ubicación", font=("Segoe UI", 10, "bold"),
                                             bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                             relief=tk.FLAT, padx=15, command=self.actualizar_ubicacion)
        btn_actualizar_ubicacion.grid(row=0, column=2, padx=5, pady=5)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar", font=("Segoe UI", 10, "bold"),
                                bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                relief=tk.FLAT, padx=15, command=self.limpiar_formulario)
        btn_limpiar.grid(row=0, column=3, padx=5, pady=5)

    def _crear_tabla(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Inventario actual", font=("Segoe UI", 11, "bold"), bg="white", fg="#2c3e50")
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        columnas = ("id", "producto", "codigo", "stock", "stock_minimo", "ubicacion", "estado")
        self.tabla_inventario = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        self.tabla_inventario.heading("id", text="ID")
        self.tabla_inventario.heading("producto", text="Producto")
        self.tabla_inventario.heading("codigo", text="Código")
        self.tabla_inventario.heading("stock", text="Stock actual")
        self.tabla_inventario.heading("stock_minimo", text="Stock mín.")
        self.tabla_inventario.heading("ubicacion", text="Ubicación")
        self.tabla_inventario.heading("estado", text="Estado")

        self.tabla_inventario.column("id", width=50, anchor="center")
        self.tabla_inventario.column("producto", width=200)
        self.tabla_inventario.column("codigo", width=100, anchor="center")
        self.tabla_inventario.column("stock", width=90, anchor="center")
        self.tabla_inventario.column("stock_minimo", width=80, anchor="center")
        self.tabla_inventario.column("ubicacion", width=150)
        self.tabla_inventario.column("estado", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_inventario.yview)
        self.tabla_inventario.configure(yscrollcommand=scrollbar.set)

        self.tabla_inventario.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ==============================
    # MÉTODOS DE NAVEGACIÓN
    # ==============================

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

    def _ir_a_proveedores(self):
        from views.proveedores_view import ProveedoresView
        self.destroy()
        ventana = ProveedoresView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_ventas(self):
        messagebox.showinfo("En desarrollo", "Módulo de ventas en construcción")

    def _ir_a_soporte(self):
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()

    # ==============================
    # MÉTODOS DE NEGOCIO
    # ==============================

    def cargar_inventario(self):
        """Carga el inventario en la tabla."""
        for fila in self.tabla_inventario.get_children():
            self.tabla_inventario.delete(fila)

        inventario = self.inventario_service.listar_inventario()

        for item in inventario:
            # item: (id_producto, nombre, codigo, precio, stock_minimo, cantidad_actual, ubicacion)
            id_producto = item[0]
            nombre = item[1]
            codigo = item[2]
            stock_minimo = item[4]
            stock_actual = item[5]
            ubicacion = item[6] if len(item) > 6 else ""

            estado = "⚠️ STOCK BAJO" if stock_actual <= stock_minimo else "Normal"

            self.tabla_inventario.insert("", "end", values=(
                id_producto, nombre, codigo, stock_actual, stock_minimo, ubicacion, estado
            ))

    def registrar_entrada(self):
        """Registra una entrada de productos."""
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        cantidad = self.entry_cantidad.get().strip()
        if not cantidad:
            messagebox.showwarning("Aviso", "Ingresa una cantidad.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        ubicacion = self.entry_ubicacion.get().strip()

        resultado, mensaje = self.inventario_service.registrar_entrada(
            self.id_producto_seleccionado, cantidad, ubicacion
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_inventario()
            self._cargar_productos_combo()
        else:
            messagebox.showerror("Error", mensaje)

    def registrar_salida(self):
        """Registra una salida de productos."""
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        cantidad = self.entry_cantidad.get().strip()
        if not cantidad:
            messagebox.showwarning("Aviso", "Ingresa una cantidad.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        resultado, mensaje = self.inventario_service.registrar_salida(
            self.id_producto_seleccionado, cantidad
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_inventario()
            self._cargar_productos_combo()
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar_ubicacion(self):
        """Actualiza la ubicación de un producto."""
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        ubicacion = self.entry_ubicacion.get().strip()
        if not ubicacion:
            messagebox.showwarning("Aviso", "Ingresa una ubicación.")
            return

        resultado, mensaje = self.inventario_service.actualizar_ubicacion(
            self.id_producto_seleccionado, ubicacion
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_inventario()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        """Limpia el formulario."""
        self.id_producto_seleccionado = None
        self.entry_cantidad.delete(0, tk.END)
        self.entry_ubicacion.delete(0, tk.END)
        self.lbl_stock_actual.config(text="Stock actual: --")
        if self.combo_productos['values']:
            self.combo_productos.current(0)
            self._cargar_producto_seleccionado()


def abrir_inventario(parent=None, usuario=None):
    """Abre la pantalla de inventario."""
    ventana = InventarioView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = InventarioView(root)
    ventana.mainloop()