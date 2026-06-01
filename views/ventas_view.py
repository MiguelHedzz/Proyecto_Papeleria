# ==============================
# VISTA DE VENTAS
# ==============================

"""
Esta pantalla permite registrar ventas de productos.

Funciones principales:
- Buscar productos por código o nombre.
- Agregar productos al carrito.
- Modificar cantidades.
- Eliminar productos del carrito.
- Calcular total automáticamente.
- Seleccionar método de pago.
- Generar comprobante/ticket de venta.
- Registrar venta en la base de datos.

Esta vista se conecta con:
services/venta_service.py
controllers/producto_controller.py
controllers/inventario_controller.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from services.venta_service import VentaService
from controllers.producto_controller import ProductoController
from controllers.inventario_controller import InventarioController


class VentasView(tk.Toplevel):
    """Pantalla de registro de ventas."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Registrar Venta")
        self.geometry("1200x700")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario = usuario
        self.venta_service = VentaService()
        self.producto_controller = ProductoController()
        self.inventario_controller = InventarioController()

        # Carrito de compras (lista de productos)
        self.carrito = []
        self.carrito_id_counter = 0

        self._construir_interfaz()
        self._cargar_productos_combo()

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
            ("Inventario", self._ir_a_inventario),
            ("Reportes", self._ir_a_reportes),
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

        btn_ventas = tk.Button(frame_acciones, text="Registrar Venta", font=("Segoe UI", 10, "bold"),
                               bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_ventas.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Registrar Venta", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel izquierdo: Búsqueda y carrito
        panel_izquierdo = tk.Frame(frame_contenido_card, bg="white")
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Panel derecho: Resumen y pago
        panel_derecho = tk.Frame(frame_contenido_card, bg="white", width=300)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        panel_derecho.pack_propagate(False)

        self._crear_panel_busqueda(panel_izquierdo)
        self._crear_tabla_carrito(panel_izquierdo)
        self._crear_panel_resumen(panel_derecho)

    def _crear_panel_busqueda(self, parent):
        frame_busqueda = tk.LabelFrame(parent, text="Agregar Producto", font=("Segoe UI", 11, "bold"),
                                        bg="white", fg="#2c3e50", padx=10, pady=10)
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))

        # Búsqueda por código
        tk.Label(frame_busqueda, text="Buscar por código:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_codigo = tk.Entry(frame_busqueda, width=20, font=("Segoe UI", 10))
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        self.entry_codigo.bind("<Return>", lambda e: self.buscar_por_codigo())

        btn_buscar = tk.Button(frame_busqueda, text="Buscar", font=("Segoe UI", 10), bg="#e67e22", fg="white",
                               activebackground="#d35400", cursor="hand2", relief=tk.FLAT, command=self.buscar_por_codigo)
        btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        # O seleccionar de lista
        tk.Label(frame_busqueda, text="O seleccionar:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_productos = ttk.Combobox(frame_busqueda, width=35, font=("Segoe UI", 10))
        self.combo_productos.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.combo_productos.bind("<<ComboboxSelected>>", self.seleccionar_producto_combo)

        # Cantidad
        tk.Label(frame_busqueda, text="Cantidad:", bg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_busqueda, width=10, font=("Segoe UI", 10))
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        btn_agregar = tk.Button(frame_busqueda, text="Agregar al Carrito", font=("Segoe UI", 10, "bold"),
                                bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                relief=tk.FLAT, padx=15, command=self.agregar_al_carrito)
        btn_agregar.grid(row=2, column=2, padx=5, pady=5)

        # Mostrar información del producto seleccionado
        self.lbl_info_producto = tk.Label(frame_busqueda, text="", bg="white", font=("Segoe UI", 9), fg="#7f8c8d")
        self.lbl_info_producto.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    def _crear_tabla_carrito(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Carrito de Compras", font=("Segoe UI", 11, "bold"),
                                     bg="white", fg="#2c3e50", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "producto", "codigo", "precio", "cantidad", "subtotal")
        self.tabla_carrito = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        self.tabla_carrito.heading("id", text="ID")
        self.tabla_carrito.heading("producto", text="Producto")
        self.tabla_carrito.heading("codigo", text="Código")
        self.tabla_carrito.heading("precio", text="Precio")
        self.tabla_carrito.heading("cantidad", text="Cantidad")
        self.tabla_carrito.heading("subtotal", text="Subtotal")

        self.tabla_carrito.column("id", width=40, anchor="center")
        self.tabla_carrito.column("producto", width=250)
        self.tabla_carrito.column("codigo", width=100, anchor="center")
        self.tabla_carrito.column("precio", width=80, anchor="center")
        self.tabla_carrito.column("cantidad", width=80, anchor="center")
        self.tabla_carrito.column("subtotal", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_carrito.yview)
        self.tabla_carrito.configure(yscrollcommand=scrollbar.set)

        self.tabla_carrito.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botones para modificar carrito
        frame_botones_carrito = tk.Frame(frame_tabla, bg="white")
        frame_botones_carrito.pack(fill=tk.X, pady=(10, 0))

        btn_modificar = tk.Button(frame_botones_carrito, text="Modificar Cantidad", font=("Segoe UI", 9),
                                  bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                  relief=tk.FLAT, padx=10, command=self.modificar_cantidad)
        btn_modificar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(frame_botones_carrito, text="Eliminar Producto", font=("Segoe UI", 9),
                                 bg="#e74c3c", fg="white", activebackground="#c0392b", cursor="hand2",
                                 relief=tk.FLAT, padx=10, command=self.eliminar_del_carrito)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_vaciar = tk.Button(frame_botones_carrito, text="Vaciar Carrito", font=("Segoe UI", 9),
                               bg="#95a5a6", fg="white", activebackground="#7f8c8d", cursor="hand2",
                               relief=tk.FLAT, padx=10, command=self.vaciar_carrito)
        btn_vaciar.pack(side=tk.LEFT, padx=5)

    def _crear_panel_resumen(self, parent):
        frame_resumen = tk.LabelFrame(parent, text="Resumen de Venta", font=("Segoe UI", 11, "bold"),
                                       bg="white", fg="#2c3e50", padx=15, pady=15)
        frame_resumen.pack(fill=tk.X, pady=(0, 15))

        # Método de pago
        tk.Label(frame_resumen, text="Método de Pago:", bg="white", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))
        self.metodo_pago = ttk.Combobox(frame_resumen, values=["Efectivo", "Tarjeta", "Transferencia"], font=("Segoe UI", 10))
        self.metodo_pago.current(0)
        self.metodo_pago.pack(fill=tk.X, pady=(0, 15))

        # Total
        tk.Label(frame_resumen, text="Total a Pagar:", bg="white", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 5))
        self.lbl_total = tk.Label(frame_resumen, text="$0.00", bg="white", font=("Segoe UI", 24, "bold"), fg="#e67e22")
        self.lbl_total.pack(anchor="w", pady=(0, 15))

        # Botones de acción
        btn_generar_ticket = tk.Button(frame_resumen, text="Generar Ticket", font=("Segoe UI", 10, "bold"),
                                        bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                        relief=tk.FLAT, pady=8, command=self.generar_ticket)
        btn_generar_ticket.pack(fill=tk.X, pady=5)

        btn_registrar = tk.Button(frame_resumen, text="Registrar Venta", font=("Segoe UI", 11, "bold"),
                                  bg="#27ae60", fg="white", activebackground="#219a52", cursor="hand2",
                                  relief=tk.FLAT, pady=10, command=self.registrar_venta)
        btn_registrar.pack(fill=tk.X, pady=5)

        btn_nueva = tk.Button(frame_resumen, text="Nueva Venta", font=("Segoe UI", 10),
                              bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                              relief=tk.FLAT, pady=8, command=self.nueva_venta)
        btn_nueva.pack(fill=tk.X, pady=5)

    def _cargar_productos_combo(self):
        productos = self.producto_controller.listar_productos()
        self.productos_map = {}
        lista_productos = []

        for p in productos:
            nombre = p[1]
            codigo = p[2]
            stock = p[7] if len(p) > 7 else 0
            self.productos_map[f"{nombre} ({codigo})"] = {
                "id": p[0],
                "nombre": nombre,
                "codigo": codigo,
                "precio": p[3],
                "stock": stock
            }
            lista_productos.append(f"{nombre} ({codigo}) - Stock: {stock}")

        self.combo_productos['values'] = lista_productos

    def buscar_por_codigo(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Ingresa un código de producto.")
            return

        producto = self.producto_controller.buscar_por_codigo(codigo)
        if producto:
            nombre = producto[1]
            precio = producto[3]
            stock = producto[7] if len(producto) > 7 else 0
            self.lbl_info_producto.config(text=f"Encontrado: {nombre} - Precio: ${precio:.2f} - Stock: {stock}")
            self.producto_seleccionado_temp = {
                "id": producto[0],
                "nombre": nombre,
                "codigo": codigo,
                "precio": precio,
                "stock": stock
            }
            self.entry_cantidad.focus_set()
        else:
            self.lbl_info_producto.config(text="Producto no encontrado")
            self.producto_seleccionado_temp = None

    def seleccionar_producto_combo(self, event=None):
        seleccion = self.combo_productos.get()
        if seleccion:
            clave = seleccion.split(" - ")[0]  # Quitar el stock del display
            if clave in self.productos_map:
                self.producto_seleccionado_temp = self.productos_map[clave]
                p = self.producto_seleccionado_temp
                self.lbl_info_producto.config(text=f"Seleccionado: {p['nombre']} - Precio: ${p['precio']:.2f} - Stock: {p['stock']}")
                self.entry_cantidad.focus_set()

    def agregar_al_carrito(self):
        if not hasattr(self, 'producto_seleccionado_temp') or not self.producto_seleccionado_temp:
            messagebox.showwarning("Aviso", "Primero busca o selecciona un producto.")
            return

        try:
            cantidad = int(self.entry_cantidad.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        producto = self.producto_seleccionado_temp
        if cantidad > producto['stock']:
            messagebox.showerror("Error", f"No hay suficiente stock. Disponible: {producto['stock']}")
            return

        # Verificar si ya existe en el carrito
        for item in self.carrito:
            if item['id'] == producto['id']:
                nueva_cantidad = item['cantidad'] + cantidad
                if nueva_cantidad > producto['stock']:
                    messagebox.showerror("Error", f"Stock insuficiente. Solo puedes agregar {producto['stock'] - item['cantidad']} más.")
                    return
                item['cantidad'] = nueva_cantidad
                item['subtotal'] = item['cantidad'] * item['precio']
                self.actualizar_tabla_carrito()
                self.actualizar_total()
                self.limpiar_seleccion()
                return

        # Agregar nuevo producto
        self.carrito_id_counter += 1
        self.carrito.append({
            'carrito_id': self.carrito_id_counter,
            'id': producto['id'],
            'nombre': producto['nombre'],
            'codigo': producto['codigo'],
            'precio': producto['precio'],
            'cantidad': cantidad,
            'subtotal': cantidad * producto['precio']
        })

        self.actualizar_tabla_carrito()
        self.actualizar_total()
        self.limpiar_seleccion()

    def actualizar_tabla_carrito(self):
        for fila in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(fila)

        for item in self.carrito:
            self.tabla_carrito.insert("", "end", values=(
                item['carrito_id'],
                item['nombre'],
                item['codigo'],
                f"${item['precio']:.2f}",
                item['cantidad'],
                f"${item['subtotal']:.2f}"
            ))

    def actualizar_total(self):
        total = sum(item['subtotal'] for item in self.carrito)
        self.lbl_total.config(text=f"${total:.2f}")
        return total

    def modificar_cantidad(self):
        seleccion = self.tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito.")
            return

        valores = self.tabla_carrito.item(seleccion[0], "values")
        carrito_id = int(valores[0])

        # Buscar el producto en el carrito
        item = next((i for i in self.carrito if i['carrito_id'] == carrito_id), None)
        if not item:
            return

        # Ventana para modificar cantidad
        dialog = tk.Toplevel(self)
        dialog.title("Modificar Cantidad")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text=f"Producto: {item['nombre']}", font=("Segoe UI", 10)).pack(pady=10)
        tk.Label(dialog, text="Nueva cantidad:", font=("Segoe UI", 10)).pack()
        entry_nueva = tk.Entry(dialog, font=("Segoe UI", 10))
        entry_nueva.insert(0, str(item['cantidad']))
        entry_nueva.pack(pady=5)

        def guardar_cambio():
            try:
                nueva = int(entry_nueva.get().strip())
                if nueva <= 0:
                    raise ValueError
                # Verificar stock
                stock = self.producto_controller.buscar_por_id(item['id'])
                stock_actual = stock[7] if stock and len(stock) > 7 else 0
                if nueva > stock_actual:
                    messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock_actual}")
                    return
                item['cantidad'] = nueva
                item['subtotal'] = nueva * item['precio']
                self.actualizar_tabla_carrito()
                self.actualizar_total()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida")

        btn_guardar = tk.Button(dialog, text="Guardar", command=guardar_cambio, bg="#e67e22", fg="white", relief=tk.FLAT, padx=20)
        btn_guardar.pack(pady=10)

    def eliminar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito.")
            return

        valores = self.tabla_carrito.item(seleccion[0], "values")
        carrito_id = int(valores[0])

        self.carrito = [i for i in self.carrito if i['carrito_id'] != carrito_id]
        self.actualizar_tabla_carrito()
        self.actualizar_total()

    def vaciar_carrito(self):
        if self.carrito and messagebox.askyesno("Confirmar", "¿Vaciar todo el carrito?"):
            self.carrito = []
            self.actualizar_tabla_carrito()
            self.actualizar_total()

    def limpiar_seleccion(self):
        self.entry_codigo.delete(0, tk.END)
        self.combo_productos.set('')
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
        self.lbl_info_producto.config(text="")
        self.producto_seleccionado_temp = None
        self.entry_codigo.focus_set()

    def generar_ticket(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "No hay productos en el carrito.")
            return

        total = self.actualizar_total()
        metodo = self.metodo_pago.get()
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        vendedor = self.usuario.nombre if self.usuario else "Administrador"

        ticket = f"""
{"="*50}
         DUNDER MIFFLIN
         Ticket de Venta
{"="*50}
Fecha: {fecha}
Vendedor: {vendedor}
Método de pago: {metodo}
{"="*50}

{"Producto":<25} {"Cant":<6} {"Precio":<8} {"Subtotal":<10}
{"-"*50}
"""
        for item in self.carrito:
            ticket += f"{item['nombre'][:24]:<25} {item['cantidad']:<6} ${item['precio']:<7.2f} ${item['subtotal']:<9.2f}\n"

        ticket += f"""
{"="*50}
TOTAL: ${total:.2f}
{"="*50}

¡Gracias por su compra!
"""
        # Mostrar ticket
        dialog = tk.Toplevel(self)
        dialog.title("Ticket de Venta")
        dialog.geometry("500x600")
        dialog.configure(bg="white")

        text_ticket = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black", wrap=tk.WORD)
        text_ticket.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_ticket.insert(tk.END, ticket)
        text_ticket.config(state=tk.DISABLED)

        btn_cerrar = tk.Button(dialog, text="Cerrar", command=dialog.destroy, bg="#e67e22", fg="white", relief=tk.FLAT, padx=20)
        btn_cerrar.pack(pady=10)

    def registrar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "No hay productos en el carrito.")
            return

        total = self.actualizar_total()
        metodo = self.metodo_pago.get()
        id_usuario = self.usuario.id_usuario if self.usuario else 1

        # Preparar productos para el servicio
        productos = []
        for item in self.carrito:
            productos.append({
                "id_producto": item['id'],
                "cantidad": item['cantidad'],
                "precio_unitario": item['precio']
            })

        resultado, mensaje = self.venta_service.procesar_venta(productos, id_usuario)

        if resultado:
            messagebox.showinfo("Éxito", f"{mensaje}\n\nMétodo de pago: {metodo}")
            self.nueva_venta()
        else:
            messagebox.showerror("Error", mensaje)

    def nueva_venta(self):
        self.carrito = []
        self.actualizar_tabla_carrito()
        self.actualizar_total()
        self.limpiar_seleccion()
        self.metodo_pago.current(0)
        self._cargar_productos_combo()

    # ==============================
    # MÉTODOS DE NAVEGACIÓN
    # ==============================

    def _ir_a_productos(self):
        from views.productos_view import ProductosView
        self.destroy()
        ventana = ProductosView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_inventario(self):
        from views.inventario_view import InventarioView
        self.destroy()
        ventana = InventarioView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_reportes(self):
        messagebox.showinfo("En desarrollo", "Módulo de reportes en construcción")

    def _ir_a_soporte(self):
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()


def abrir_ventas(parent=None, usuario=None):
    ventana = VentasView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = VentasView(root)
    ventana.mainloop()