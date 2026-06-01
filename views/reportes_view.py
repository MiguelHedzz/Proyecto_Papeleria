# ==============================
# VISTA DE REPORTES
# ==============================

"""
Esta pantalla permite generar y visualizar reportes del sistema.

Funciones principales:
- Reporte de inventario actual.
- Reporte de productos con stock bajo.
- Reporte de ventas por período.
- Reporte de productos más vendidos.
- Exportar reportes a CSV/Excel.
- Filtrar por fechas y categorías.

Esta vista se conecta con:
controllers/reporte_controller.py
services/reporte_service.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.reporte_controller import ReporteController
from controllers.producto_controller import ProductoController
from controllers.categoria_controller import CategoriaController


class ReportesView(tk.Toplevel):
    """Pantalla de generación de reportes."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Reportes")
        self.geometry("1100x700")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario = usuario
        self.reporte_controller = ReporteController()
        self.producto_controller = ProductoController()
        self.categoria_controller = CategoriaController()

        self.reporte_actual = None
        self.tipo_reporte_actual = "inventario"

        self._construir_interfaz()
        self._cargar_filtros()
        self.generar_reporte_inventario()

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
            ("Alertas", self._ir_a_alertas),
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

        btn_reportes = tk.Button(frame_acciones, text="Generar Reportes", font=("Segoe UI", 10, "bold"),
                                 bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_reportes.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Generar Reportes", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel de selección de reporte
        self._crear_panel_seleccion(frame_contenido_card)

        # Panel de filtros (para ventas)
        self._crear_panel_filtros(frame_contenido_card)

        # Tabla de resultados
        self._crear_tabla(frame_contenido_card)

        # Panel de acciones
        self._crear_panel_acciones(frame_contenido_card)

    def _crear_panel_seleccion(self, parent):
        frame_seleccion = tk.Frame(parent, bg="white")
        frame_seleccion.pack(fill=tk.X, pady=(0, 10))

        tk.Label(frame_seleccion, text="Tipo de Reporte:", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.tipo_reporte = ttk.Combobox(frame_seleccion, values=[
            "Inventario Actual",
            "Stock Bajo",
            "Ventas por Período",
            "Productos Más Vendidos"
        ], width=25, font=("Segoe UI", 10))
        self.tipo_reporte.current(0)
        self.tipo_reporte.pack(side=tk.LEFT, padx=5)
        self.tipo_reporte.bind("<<ComboboxSelected>>", self.cambiar_tipo_reporte)

    def _crear_panel_filtros(self, parent):
        self.frame_filtros = tk.Frame(parent, bg="white")
        self.frame_filtros.pack(fill=tk.X, pady=(0, 10))

        # Filtros por fecha (solo visibles para reportes de ventas)
        self.frame_fechas = tk.Frame(self.frame_filtros, bg="white")

        tk.Label(self.frame_fechas, text="Fecha Inicio:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.entry_fecha_inicio = tk.Entry(self.frame_fechas, width=12, font=("Segoe UI", 10))
        self.entry_fecha_inicio.pack(side=tk.LEFT, padx=5)

        tk.Label(self.frame_fechas, text="Fecha Fin:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.entry_fecha_fin = tk.Entry(self.frame_fechas, width=12, font=("Segoe UI", 10))
        self.entry_fecha_fin.pack(side=tk.LEFT, padx=5)

        # Botón para aplicar fechas
        self.btn_aplicar_fechas = tk.Button(self.frame_fechas, text="Aplicar Fechas", font=("Segoe UI", 9),
                                            bg="#e67e22", fg="white", activebackground="#d35400",
                                            cursor="hand2", relief=tk.FLAT, command=self.aplicar_fechas)
        self.btn_aplicar_fechas.pack(side=tk.LEFT, padx=10)

        # Filtro por categoría
        self.frame_categoria = tk.Frame(self.frame_filtros, bg="white")
        tk.Label(self.frame_categoria, text="Categoría:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.combo_categoria = ttk.Combobox(self.frame_categoria, width=20, font=("Segoe UI", 10))
        self.combo_categoria.pack(side=tk.LEFT, padx=5)
        self.combo_categoria.bind("<<ComboboxSelected>>", self.filtrar_por_categoria)

        # Ocultar filtros inicialmente
        self.frame_fechas.pack_forget()
        self.frame_categoria.pack_forget()

    def _crear_tabla(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Resultados", font=("Segoe UI", 11, "bold"),
                                     bg="white", fg="#2c3e50", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Frame para scroll
        self.frame_tabla_contenedor = tk.Frame(frame_tabla, bg="white")
        self.frame_tabla_contenedor.pack(fill=tk.BOTH, expand=True)

        # Treeview se creará dinámicamente según el reporte
        self.tabla_reportes = None

        scrollbar_y = ttk.Scrollbar(self.frame_tabla_contenedor, orient="vertical")
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(self.frame_tabla_contenedor, orient="horizontal")
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.scrollbar_y = scrollbar_y
        self.scrollbar_x = scrollbar_x

    def _crear_panel_acciones(self, parent):
        frame_acciones = tk.Frame(parent, bg="white")
        frame_acciones.pack(fill=tk.X)

        btn_exportar_csv = tk.Button(frame_acciones, text="Exportar a CSV", font=("Segoe UI", 10),
                                     bg="#27ae60", fg="white", activebackground="#219a52", cursor="hand2",
                                     relief=tk.FLAT, padx=15, command=self.exportar_csv)
        btn_exportar_csv.pack(side=tk.LEFT, padx=5)

        btn_exportar_excel = tk.Button(frame_acciones, text="Exportar a Excel", font=("Segoe UI", 10),
                                       bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                       relief=tk.FLAT, padx=15, command=self.exportar_excel)
        btn_exportar_excel.pack(side=tk.LEFT, padx=5)

        btn_imprimir = tk.Button(frame_acciones, text="Imprimir", font=("Segoe UI", 10),
                                 bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                 relief=tk.FLAT, padx=15, command=self.imprimir_reporte)
        btn_imprimir.pack(side=tk.LEFT, padx=5)

        self.lbl_info = tk.Label(frame_acciones, text="", bg="white", font=("Segoe UI", 9), fg="#7f8c8d")
        self.lbl_info.pack(side=tk.RIGHT, padx=10)

    def _cargar_filtros(self):
        """Carga las categorías en el combo."""
        categorias = self.categoria_controller.listar_categorias()
        self.categorias_map = {c[1]: c[0] for c in categorias}
        lista_categorias = ["Todas"] + list(self.categorias_map.keys())
        self.combo_categoria['values'] = lista_categorias
        self.combo_categoria.current(0)

        # Fechas por defecto: últimos 30 días
        hoy = datetime.now()
        hace_30_dias = hoy - timedelta(days=30)
        self.entry_fecha_inicio.insert(0, hace_30_dias.strftime("%Y-%m-%d"))
        self.entry_fecha_fin.insert(0, hoy.strftime("%Y-%m-%d"))

    def cambiar_tipo_reporte(self, event=None):
        """Cambia el tipo de reporte y muestra los filtros correspondientes."""
        seleccion = self.tipo_reporte.get()

        # Ocultar todos los filtros
        self.frame_fechas.pack_forget()
        self.frame_categoria.pack_forget()

        if seleccion == "Ventas por Período":
            self.frame_fechas.pack(fill=tk.X, pady=(0, 5))
            self.generar_reporte_ventas()
        elif seleccion == "Productos Más Vendidos":
            self.generar_reporte_mas_vendidos()
        elif seleccion == "Inventario Actual":
            self.generar_reporte_inventario()
        elif seleccion == "Stock Bajo":
            self.generar_reporte_stock_bajo()

    def aplicar_fechas(self):
        """Aplica el filtro de fechas al reporte de ventas."""
        self.generar_reporte_ventas()

    def filtrar_por_categoria(self, event=None):
        """Filtra el reporte de productos por categoría."""
        seleccion = self.tipo_reporte.get()
        if seleccion == "Inventario Actual":
            self.generar_reporte_inventario()
        elif seleccion == "Stock Bajo":
            self.generar_reporte_stock_bajo()

    def generar_reporte_inventario(self):
        """Genera reporte de inventario actual."""
        self.tipo_reporte_actual = "inventario"

        # Obtener datos
        inventario = self.reporte_controller.reporte_inventario_actual()

        if inventario and inventario.datos:
            self._crear_tabla_dinamica(inventario.datos[0].keys() if inventario.datos else [])
            self._llenar_tabla(inventario.datos)
            self.lbl_info.config(text=f"Total productos: {len(inventario.datos)} | Generado: {inventario.fecha_generacion}")
        else:
            self._limpiar_tabla()
            self.lbl_info.config(text="No hay datos de inventario")

    def generar_reporte_stock_bajo(self):
        """Genera reporte de productos con stock bajo."""
        self.tipo_reporte_actual = "stock_bajo"

        # Aplicar filtro de categoría
        categoria = self.combo_categoria.get()
        id_categoria = self.categorias_map.get(categoria) if categoria != "Todas" else None

        reporte = self.reporte_controller.reporte_stock_bajo()

        if reporte and reporte.datos:
            # Filtrar por categoría si es necesario
            datos = reporte.datos
            if id_categoria:
                # Obtener productos de esa categoría
                productos_cat = self.producto_controller.listar_productos()
                ids_categoria = [p[0] for p in productos_cat if p[5] == id_categoria]
                datos = [d for d in datos if d.get('id_producto') in ids_categoria]

            self._crear_tabla_dinamica(datos[0].keys() if datos else [])
            self._llenar_tabla(datos)
            self.lbl_info.config(text=f"Productos con stock bajo: {len(datos)} | {reporte.fecha_generacion}")
        else:
            self._limpiar_tabla()
            self.lbl_info.config(text="No hay productos con stock bajo")

    def generar_reporte_ventas(self):
        """Genera reporte de ventas por período."""
        self.tipo_reporte_actual = "ventas"

        fecha_inicio = self.entry_fecha_inicio.get().strip()
        fecha_fin = self.entry_fecha_fin.get().strip()

        if not fecha_inicio or not fecha_fin:
            messagebox.showwarning("Aviso", "Ingresa fechas válidas")
            return

        try:
            reporte = self.reporte_controller.reporte_ventas_por_periodo(fecha_inicio, fecha_fin)
            if reporte and reporte.datos:
                self._crear_tabla_dinamica(reporte.datos[0].keys() if reporte.datos else [])
                self._llenar_tabla(reporte.datos)
                total_general = getattr(reporte, 'total_general', 0)
                self.lbl_info.config(text=f"Período: {fecha_inicio} a {fecha_fin} | Total ventas: {len(reporte.datos)} | Total general: ${total_general:.2f}")
            else:
                self._limpiar_tabla()
                self.lbl_info.config(text=f"No hay ventas en el período {fecha_inicio} a {fecha_fin}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")

    def generar_reporte_mas_vendidos(self):
        """Genera reporte de productos más vendidos."""
        self.tipo_reporte_actual = "mas_vendidos"

        reporte = self.reporte_controller.reporte_productos_mas_vendidos(15)

        if reporte and reporte.datos:
            self._crear_tabla_dinamica(reporte.datos[0].keys() if reporte.datos else [])
            self._llenar_tabla(reporte.datos)
            self.lbl_info.config(text=f"Top {len(reporte.datos)} productos más vendidos | {reporte.fecha_generacion}")
        else:
            self._limpiar_tabla()
            self.lbl_info.config(text="No hay datos de productos vendidos")

    def _crear_tabla_dinamica(self, columnas):
        """Crea una tabla dinámica según las columnas del reporte."""
        # Destruir tabla anterior si existe
        if self.tabla_reportes:
            self.tabla_reportes.destroy()

        # Crear nueva tabla
        self.tabla_reportes = ttk.Treeview(self.frame_tabla_contenedor, columns=columnas, show="headings")

        for col in columnas:
            self.tabla_reportes.heading(col, text=col.replace('_', ' ').title())
            self.tabla_reportes.column(col, width=120, anchor="center")

        self.tabla_reportes.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.config(command=self.tabla_reportes.yview)
        self.scrollbar_x.config(command=self.tabla_reportes.xview)

        self.tabla_reportes.pack(side="left", fill="both", expand=True)

    def _llenar_tabla(self, datos):
        """Llena la tabla con los datos del reporte."""
        for fila in self.tabla_reportes.get_children():
            self.tabla_reportes.delete(fila)

        for registro in datos:
            valores = [str(registro.get(col, "")) for col in self.tabla_reportes['columns']]
            self.tabla_reportes.insert("", "end", values=valores)

    def _limpiar_tabla(self):
        """Limpia la tabla."""
        if self.tabla_reportes:
            for fila in self.tabla_reportes.get_children():
                self.tabla_reportes.delete(fila)

    def exportar_csv(self):
        """Exporta el reporte actual a CSV."""
        if not self.tabla_reportes or not self.tabla_reportes.get_children():
            messagebox.showwarning("Aviso", "No hay datos para exportar")
            return

        from utils.exportar import exportar_a_csv
        from datetime import datetime

        # Obtener datos
        columnas = self.tabla_reportes['columns']
        datos = []

        for fila in self.tabla_reportes.get_children():
            valores = self.tabla_reportes.item(fila, "values")
            datos.append(list(valores))

        nombre_archivo = f"reporte_{self.tipo_reporte_actual}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        resultado, mensaje = exportar_a_csv(nombre_archivo, columnas, datos)

        if resultado:
            messagebox.showinfo("Éxito", f"Reporte exportado a:\n{nombre_archivo}")
        else:
            messagebox.showerror("Error", mensaje)

    def exportar_excel(self):
        """Exporta el reporte actual a Excel."""
        messagebox.showinfo("En desarrollo", "Exportación a Excel próximamente")

    def imprimir_reporte(self):
        """Imprime el reporte actual."""
        if not self.tabla_reportes or not self.tabla_reportes.get_children():
            messagebox.showwarning("Aviso", "No hay datos para imprimir")
            return

        # Crear ventana de vista previa
        preview = tk.Toplevel(self)
        preview.title("Vista Previa - Reporte")
        preview.geometry("800x600")
        preview.configure(bg="white")

        text_area = tk.Text(preview, font=("Courier", 10), wrap=tk.NONE)
        text_area.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(preview, orient="vertical", command=text_area.yview)
        scroll_y.pack(side="right", fill="y")
        text_area.configure(yscrollcommand=scroll_y.set)

        scroll_x = tk.Scrollbar(preview, orient="horizontal", command=text_area.xview)
        scroll_x.pack(side="bottom", fill="x")
        text_area.configure(xscrollcommand=scroll_x.set)

        # Construir texto
        texto = f"{'='*80}\n"
        texto += f"REPORTE: {self.tipo_reporte.get()}\n"
        texto += f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        texto += f"{'='*80}\n\n"

        # Encabezados
        columnas = self.tabla_reportes['columns']
        for col in columnas:
            texto += f"{col.replace('_', ' ').title():<20}"
        texto += "\n" + "-" * 80 + "\n"

        # Datos
        for fila in self.tabla_reportes.get_children():
            valores = self.tabla_reportes.item(fila, "values")
            for val in valores:
                texto += f"{str(val):<20}"
            texto += "\n"

        text_area.insert(tk.END, texto)
        text_area.config(state=tk.DISABLED)

        btn_cerrar = tk.Button(preview, text="Cerrar", command=preview.destroy,
                               bg="#e67e22", fg="white", relief=tk.FLAT, padx=20)
        btn_cerrar.pack(pady=10)

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

    def _ir_a_alertas(self):
        from views.alertas_view import AlertasView
        self.destroy()
        ventana = AlertasView(self.master, self.usuario)
        ventana.focus_set()

    def _ir_a_soporte(self):
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()


def abrir_reportes(parent=None, usuario=None):
    ventana = ReportesView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = ReportesView(root)
    ventana.mainloop()