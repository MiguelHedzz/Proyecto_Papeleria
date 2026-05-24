# ==============================
# VISTA DE PRODUCTOS
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
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Esto permite que el archivo funcione aunque se ejecute directamente.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.producto_controller import ProductoController


# ==============================
# CLASE PRINCIPAL DE LA VISTA
# ==============================

class ProductosView(tk.Frame):
    """
    Esta clase representa la pantalla de administración de productos.

    Hereda de tk.Frame, lo que permite colocarla dentro de una ventana principal
    o abrirla como una pantalla independiente.
    """

    def __init__(self, parent):
        """
        Constructor de la pantalla.

        Parámetro:
        parent: ventana o contenedor donde se mostrará esta vista.
        """

        super().__init__(parent)

        # Guardamos el controlador de productos.
        self.producto_controller = ProductoController()

        # Variable para saber qué producto está seleccionado en la tabla.
        self.id_producto_seleccionado = None

        # Variables para conservar categoría y proveedor del producto seleccionado.
        self.id_categoria_actual = None
        self.id_proveedor_actual = None

        # Configuración visual general.
        self.config(bg="#f4f6f8")

        # Creamos todos los elementos de la pantalla.
        self.crear_interfaz()

        # Cargamos productos al iniciar.
        self.cargar_productos()

    # ==============================
    # CREAR INTERFAZ
    # ==============================

    def crear_interfaz(self):
        """
        Crea los elementos visuales de la pantalla:
        títulos, entradas de texto, botones y tabla.
        """

        # Título principal.
        titulo = tk.Label(
            self,
            text="Administración de Productos",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        )
        titulo.pack(pady=15)

        # Contenedor principal.
        contenedor = tk.Frame(self, bg="#f4f6f8")
        contenedor.pack(fill="both", expand=True, padx=20, pady=10)

        # ==============================
        # FORMULARIO
        # ==============================

        frame_formulario = tk.LabelFrame(
            contenedor,
            text="Datos del producto",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#111827",
            padx=15,
            pady=15
        )
        frame_formulario.pack(fill="x", pady=10)

        # Nombre.
        tk.Label(
            frame_formulario,
            text="Nombre:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.entry_nombre = tk.Entry(frame_formulario, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Código.
        tk.Label(
            frame_formulario,
            text="Código:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)

        self.entry_codigo = tk.Entry(frame_formulario, width=20)
        self.entry_codigo.grid(row=0, column=3, padx=5, pady=5)

        # Precio.
        tk.Label(
            frame_formulario,
            text="Precio:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.entry_precio = tk.Entry(frame_formulario, width=30)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=5)

        # Stock mínimo.
        tk.Label(
            frame_formulario,
            text="Stock mínimo:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=1, column=2, sticky="w", padx=5, pady=5)

        self.entry_stock_minimo = tk.Entry(frame_formulario, width=20)
        self.entry_stock_minimo.grid(row=1, column=3, padx=5, pady=5)

        # Cantidad inicial / actual.
        tk.Label(
            frame_formulario,
            text="Cantidad:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.entry_cantidad = tk.Entry(frame_formulario, width=30)
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

        # Ubicación.
        tk.Label(
            frame_formulario,
            text="Ubicación:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.entry_ubicacion = tk.Entry(frame_formulario, width=20)
        self.entry_ubicacion.grid(row=2, column=3, padx=5, pady=5)

        # ==============================
        # BOTONES
        # ==============================

        frame_botones = tk.Frame(contenedor, bg="#f4f6f8")
        frame_botones.pack(fill="x", pady=10)

        btn_agregar = tk.Button(
            frame_botones,
            text="Agregar",
            width=15,
            command=self.agregar_producto
        )
        btn_agregar.grid(row=0, column=0, padx=5, pady=5)

        btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar",
            width=15,
            command=self.actualizar_producto
        )
        btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            width=15,
            command=self.eliminar_producto
        )
        btn_eliminar.grid(row=0, column=2, padx=5, pady=5)

        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            width=15,
            command=self.limpiar_formulario
        )
        btn_limpiar.grid(row=0, column=3, padx=5, pady=5)

        # Búsqueda.
        tk.Label(
            frame_botones,
            text="Buscar código:",
            bg="#f4f6f8",
            font=("Arial", 10)
        ).grid(row=1, column=0, padx=5, pady=5)

        self.entry_buscar = tk.Entry(frame_botones, width=20)
        self.entry_buscar.grid(row=1, column=1, padx=5, pady=5)

        btn_buscar = tk.Button(
            frame_botones,
            text="Buscar",
            width=15,
            command=self.buscar_producto
        )
        btn_buscar.grid(row=1, column=2, padx=5, pady=5)

        btn_mostrar_todos = tk.Button(
            frame_botones,
            text="Mostrar todos",
            width=15,
            command=self.cargar_productos
        )
        btn_mostrar_todos.grid(row=1, column=3, padx=5, pady=5)

        # ==============================
        # TABLA
        # ==============================

        frame_tabla = tk.LabelFrame(
            contenedor,
            text="Lista de productos",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#111827",
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True, pady=10)

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
            height=10
        )

        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock_minimo", text="Stock mínimo")
        self.tabla_productos.heading("cantidad", text="Cantidad")
        self.tabla_productos.heading("ubicacion", text="Ubicación")

        self.tabla_productos.column("id", width=50, anchor="center")
        self.tabla_productos.column("nombre", width=180)
        self.tabla_productos.column("codigo", width=100, anchor="center")
        self.tabla_productos.column("precio", width=90, anchor="center")
        self.tabla_productos.column("stock_minimo", width=100, anchor="center")
        self.tabla_productos.column("cantidad", width=90, anchor="center")
        self.tabla_productos.column("ubicacion", width=130)

        self.tabla_productos.pack(side="left", fill="both", expand=True)

        # Scroll vertical.
        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tabla_productos.configure(yscrollcommand=scrollbar.set)

        # Evento al seleccionar una fila.
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    # ==============================
    # CARGAR PRODUCTOS
    # ==============================

    def cargar_productos(self):
        """
        Carga todos los productos en la tabla.
        """

        # Limpiamos la tabla.
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        productos = self.producto_controller.listar_productos()

        for producto in productos:
            # Según el controlador:
            # 0 id_producto
            # 1 nombre
            # 2 codigo
            # 3 precio
            # 4 stock_minimo
            # 5 id_categoria
            # 6 id_proveedor
            # 7 cantidad_actual
            # 8 ubicacion

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

    # ==============================
    # OBTENER DATOS DEL FORMULARIO
    # ==============================

    def obtener_datos_formulario(self):
        """
        Obtiene los datos capturados en el formulario.

        Retorna:
        nombre, codigo, precio, stock_minimo, cantidad, ubicacion
        """

        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        precio = self.entry_precio.get().strip()
        stock_minimo = self.entry_stock_minimo.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        ubicacion = self.entry_ubicacion.get().strip()

        return nombre, codigo, precio, stock_minimo, cantidad, ubicacion

    # ==============================
    # AGREGAR PRODUCTO
    # ==============================

    def agregar_producto(self):
        """
        Registra un nuevo producto.
        """

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

    # ==============================
    # SELECCIONAR PRODUCTO
    # ==============================

    def seleccionar_producto(self, event):
        """
        Cuando el usuario selecciona un producto en la tabla,
        los datos se cargan en el formulario.
        """

        seleccion = self.tabla_productos.selection()

        if not seleccion:
            return

        valores = self.tabla_productos.item(seleccion[0], "values")

        self.id_producto_seleccionado = valores[0]

        # Buscamos el producto completo para conservar categoría y proveedor.
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

    # ==============================
    # ACTUALIZAR PRODUCTO
    # ==============================

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

        nombre, codigo, precio, stock_minimo, cantidad, ubicacion = self.obtener_datos_formulario()

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

    # ==============================
    # ELIMINAR PRODUCTO
    # ==============================

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
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    # ==============================
    # BUSCAR PRODUCTO
    # ==============================

    def buscar_producto(self):
        """
        Busca un producto por código.
        """

        codigo = self.entry_buscar.get().strip()

        if codigo == "":
            messagebox.showwarning(
                "Aviso",
                "Ingresa un código para buscar."
            )
            return

        producto = self.producto_controller.buscar_por_codigo(codigo)

        # Limpiamos la tabla.
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
            messagebox.showinfo(
                "Sin resultados",
                "No se encontró un producto con ese código."
            )

    # ==============================
    # LIMPIAR FORMULARIO
    # ==============================

    def limpiar_formulario(self):
        """
        Limpia todos los campos del formulario.
        """

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
# FUNCIÓN PARA ABRIR LA VISTA
# ==============================

def abrir_productos(parent=None):
    """
    Abre la pantalla de productos.

    Si recibe una ventana padre, abre un Toplevel.
    Si no recibe padre, crea una ventana nueva.
    """

    if parent is None:
        ventana = tk.Tk()
    else:
        ventana = tk.Toplevel(parent)

    ventana.title("Administración de Productos")
    ventana.geometry("1000x650")
    ventana.resizable(True, True)

    vista = ProductosView(ventana)
    vista.pack(fill="both", expand=True)

    if parent is None:
        ventana.mainloop()


# ==============================
# EJECUCIÓN DIRECTA
# ==============================

if __name__ == "__main__":
    abrir_productos()