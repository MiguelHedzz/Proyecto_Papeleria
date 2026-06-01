# ==============================
# VISTA DE ALERTAS
# ==============================

"""
Esta pantalla permite visualizar y gestionar alertas de stock bajo.

Funciones principales:
- Mostrar alertas de productos con stock bajo.
- Marcar alertas como atendidas.
- Ver historial de alertas (atendidas/no atendidas).
- Actualizar lista de alertas.
- Generar reporte de alertas.

Esta vista se conecta con:
controllers/alerta_controller.py
services/inventario_service.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.alerta_controller import AlertaController
from controllers.producto_controller import ProductoController
from services.inventario_service import InventarioService


class AlertasView(tk.Toplevel):
    """Pantalla de gestión de alertas de stock bajo."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Alertas de Stock Bajo")
        self.geometry("1000x600")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario = usuario
        self.alerta_controller = AlertaController()
        self.producto_controller = ProductoController()
        self.inventario_service = InventarioService()

        self.alerta_seleccionada = None
        self.filtro_actual = "pendientes"  # pendientes, todas

        self._construir_interfaz()
        self.cargar_alertas()

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
            ("Ventas", self._ir_a_ventas),
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

        btn_alertas = tk.Button(frame_acciones, text="Alertas de Stock", font=("Segoe UI", 10, "bold"),
                                bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_alertas.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Alertas de Stock Bajo", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel de filtros
        self._crear_filtros(frame_contenido_card)

        # Tabla de alertas
        self._crear_tabla(frame_contenido_card)

        # Botones de acción
        self._crear_botones_accion(frame_contenido_card)

        # Panel de información
        self._crear_panel_info(frame_contenido_card)

    def _crear_filtros(self, parent):
        frame_filtros = tk.Frame(parent, bg="white")
        frame_filtros.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame_filtros, text="Mostrar:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)

        self.combo_filtro = ttk.Combobox(frame_filtros, values=["Pendientes", "Todas"], width=15, font=("Segoe UI", 10))
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side=tk.LEFT, padx=5)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.cambiar_filtro)

        btn_actualizar = tk.Button(frame_filtros, text="Actualizar", font=("Segoe UI", 9), bg="#e67e22", fg="white",
                                   activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=15,
                                   command=self.cargar_alertas)
        btn_actualizar.pack(side=tk.LEFT, padx=20)

        btn_verificar = tk.Button(frame_filtros, text="Verificar Stock Bajo", font=("Segoe UI", 9), bg="#7f8c8d", fg="white",
                                  activebackground="#6c7a7d", cursor="hand2", relief=tk.FLAT, padx=15,
                                  command=self.verificar_y_generar_alertas)
        btn_verificar.pack(side=tk.LEFT, padx=5)

    def _crear_tabla(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Lista de Alertas", font=("Segoe UI", 11, "bold"),
                                     bg="white", fg="#2c3e50", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columnas = ("id", "producto", "mensaje", "fecha", "estado")
        self.tabla_alertas = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla_alertas.heading("id", text="ID")
        self.tabla_alertas.heading("producto", text="Producto")
        self.tabla_alertas.heading("mensaje", text="Mensaje")
        self.tabla_alertas.heading("fecha", text="Fecha")
        self.tabla_alertas.heading("estado", text="Estado")

        self.tabla_alertas.column("id", width=50, anchor="center")
        self.tabla_alertas.column("producto", width=200)
        self.tabla_alertas.column("mensaje", width=350)
        self.tabla_alertas.column("fecha", width=150, anchor="center")
        self.tabla_alertas.column("estado", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_alertas.yview)
        self.tabla_alertas.configure(yscrollcommand=scrollbar.set)

        self.tabla_alertas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_alertas.bind("<<TreeviewSelect>>", self.seleccionar_alerta)

    def _crear_botones_accion(self, parent):
        frame_botones = tk.Frame(parent, bg="white")
        frame_botones.pack(fill=tk.X, pady=10)

        btn_marcar_atendida = tk.Button(frame_botones, text="Marcar como Atendida", font=("Segoe UI", 10, "bold"),
                                        bg="#27ae60", fg="white", activebackground="#219a52", cursor="hand2",
                                        relief=tk.FLAT, padx=15, command=self.marcar_atendida)
        btn_marcar_atendida.pack(side=tk.LEFT, padx=5)

        btn_ver_producto = tk.Button(frame_botones, text="Ver Producto", font=("Segoe UI", 10),
                                     bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                     relief=tk.FLAT, padx=15, command=self.ver_producto)
        btn_ver_producto.pack(side=tk.LEFT, padx=5)

        btn_exportar = tk.Button(frame_botones, text="Exportar Alertas", font=("Segoe UI", 10),
                                 bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                 relief=tk.FLAT, padx=15, command=self.exportar_alertas)
        btn_exportar.pack(side=tk.LEFT, padx=5)

    def _crear_panel_info(self, parent):
        frame_info = tk.LabelFrame(parent, text="Resumen", font=("Segoe UI", 10, "bold"),
                                    bg="white", fg="#2c3e50", padx=10, pady=5)
        frame_info.pack(fill=tk.X)

        self.lbl_resumen = tk.Label(frame_info, text="Cargando...", bg="white", font=("Segoe UI", 10))
        self.lbl_resumen.pack(anchor="w", pady=5)

    def cargar_alertas(self):
        """Carga las alertas según el filtro seleccionado."""
        for fila in self.tabla_alertas.get_children():
            self.tabla_alertas.delete(fila)

        filtro = self.combo_filtro.get()
        self.filtro_actual = "pendientes" if filtro == "Pendientes" else "todas"

        # Obtener alertas
        if self.filtro_actual == "pendientes":
            alertas = self.alerta_controller.obtener_alertas_pendientes()
        else:
            # Para todas las alertas, necesitamos un método adicional
            # Por ahora, usamos las pendientes + una consulta general
            alertas = self._obtener_todas_alertas()

        for alerta in alertas:
            # alerta: (id_alerta, nombre_producto, mensaje, fecha, atendida)
            estado = "✓ Atendida" if alerta[4] == 1 else "⚠️ Pendiente"
            self.tabla_alertas.insert("", "end", values=(
                alerta[0], alerta[1], alerta[2], alerta[3], estado
            ))

        self.actualizar_resumen()

    def _obtener_todas_alertas(self):
        """Obtiene todas las alertas (pendientes y atendidas)."""
        try:
            import sqlite3
            from database.conexion import conectar_bd

            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT a.id_alerta, p.nombre, a.mensaje, 
                       COALESCE(a.fecha, 'Sin fecha') as fecha,
                       a.atendida
                FROM alerta a
                INNER JOIN producto p ON a.id_producto = p.id_producto
                ORDER BY a.atendida ASC, a.id_alerta DESC
            """)

            alertas = cursor.fetchall()
            conexion.close()
            return alertas
        except Exception as e:
            print(f"Error al obtener alertas: {e}")
            return []

    def actualizar_resumen(self):
        """Actualiza el resumen de alertas."""
        try:
            import sqlite3
            from database.conexion import conectar_bd

            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Contar pendientes
            cursor.execute("SELECT COUNT(*) FROM alerta WHERE atendida = 0")
            pendientes = cursor.fetchone()[0]

            # Contar total
            cursor.execute("SELECT COUNT(*) FROM alerta")
            total = cursor.fetchone()[0]

            conexion.close()

            self.lbl_resumen.config(text=f"📊 Resumen: {pendientes} alertas pendientes | {total} alertas en total")
        except:
            self.lbl_resumen.config(text="📊 No se pudo cargar el resumen")

    def seleccionar_alerta(self, event):
        """Selecciona una alerta de la tabla."""
        seleccion = self.tabla_alertas.selection()
        if not seleccion:
            return

        valores = self.tabla_alertas.item(seleccion[0], "values")
        self.alerta_seleccionada = {
            "id": valores[0],
            "producto": valores[1],
            "mensaje": valores[2],
            "fecha": valores[3],
            "estado": valores[4]
        }

    def cambiar_filtro(self, event=None):
        """Cambia el filtro de alertas."""
        self.cargar_alertas()

    def marcar_atendida(self):
        """Marca la alerta seleccionada como atendida."""
        if not self.alerta_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una alerta de la tabla.")
            return

        if "Pendiente" not in self.alerta_seleccionada['estado']:
            messagebox.showinfo("Info", "Esta alerta ya fue atendida.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Marcar como atendida la alerta del producto '{self.alerta_seleccionada['producto']}'?")

        if confirmar:
            resultado = self.alerta_controller.marcar_alerta_como_leida(self.alerta_seleccionada['id'])
            if resultado:
                messagebox.showinfo("Éxito", "Alerta marcada como atendida.")
                self.cargar_alertas()
                self.alerta_seleccionada = None
            else:
                messagebox.showerror("Error", "No se pudo marcar la alerta.")

    def ver_producto(self):
        """Abre la ventana de productos para ver/editar el producto."""
        if not self.alerta_seleccionada:
            messagebox.showwarning("Aviso", "Selecciona una alerta de la tabla.")
            return

        # Buscar el producto por nombre
        nombre_producto = self.alerta_seleccionada['producto']
        productos = self.producto_controller.buscar_por_nombre(nombre_producto)

        if productos:
            id_producto = productos[0][0]
            from views.productos_view import ProductosView
            self.destroy()
            ventana = ProductosView(self.master, self.usuario)
            # Aquí se podría seleccionar el producto automáticamente
            ventana.focus_set()
        else:
            messagebox.showinfo("Info", "No se pudo encontrar el producto.")

    def verificar_y_generar_alertas(self):
        """Verifica todos los productos y genera alertas para stock bajo."""
        productos = self.producto_controller.listar_productos()
        productos_con_stock = []

        for p in productos:
            id_producto = p[0]
            nombre = p[1]
            stock_minimo = p[4]
            stock_actual = p[7] if len(p) > 7 else 0
            productos_con_stock.append((id_producto, nombre, stock_actual, stock_minimo))

        generadas = self.alerta_controller.verificar_stock_y_generar_alertas(productos_con_stock)

        if generadas > 0:
            messagebox.showinfo("Alertas generadas", f"Se generaron {generadas} alerta(s) de stock bajo.")
            self.cargar_alertas()
        else:
            messagebox.showinfo("Sin alertas", "No se encontraron productos con stock bajo.")

    def exportar_alertas(self):
        """Exporta las alertas a un archivo CSV."""
        from utils.exportar import exportar_a_csv
        from datetime import datetime

        # Obtener datos de la tabla
        datos = []
        for fila in self.tabla_alertas.get_children():
            valores = self.tabla_alertas.item(fila, "values")
            datos.append(list(valores))

        if not datos:
            messagebox.showwarning("Aviso", "No hay datos para exportar.")
            return

        nombre_archivo = f"alertas_stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        encabezados = ["ID", "Producto", "Mensaje", "Fecha", "Estado"]

        resultado, mensaje = exportar_a_csv(nombre_archivo, encabezados, datos)

        if resultado:
            messagebox.showinfo("Éxito", f"Alertas exportadas a:\n{nombre_archivo}")
        else:
            messagebox.showerror("Error", mensaje)

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

    def _ir_a_ventas(self):
        from views.ventas_view import VentasView
        self.destroy()
        ventana = VentasView(self.master, self.usuario)
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


def abrir_alertas(parent=None, usuario=None):
    ventana = AlertasView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = AlertasView(root)
    ventana.mainloop()