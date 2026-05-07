import sqlite3
import tkinter as tk
from tkinter import messagebox


# ==============================
# CONEXIÓN A BASE DE DATOS
# ==============================

def conectar_bd():
    conexion = sqlite3.connect("inventario_papeleria.db")
    return conexion


def crear_tablas():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    # Tabla de categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    """)

    # Tabla de proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedor (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            correo TEXT
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL,
            stock_minimo INTEGER NOT NULL,
            id_categoria INTEGER,
            id_proveedor INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        )
    """)

    # Tabla de inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            cantidad_actual INTEGER NOT NULL,
            ubicacion TEXT,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    # Tabla de ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    # Tabla detalle de venta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    # Tabla de alertas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerta (
            id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            atendida INTEGER DEFAULT 0,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    # Usuario administrador por defecto
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (id_usuario, nombre, usuario, password, rol)
        VALUES (1, 'Administrador', 'admin', 'admin123', 'Administrador')
    """)

    conexion.commit()
    conexion.close()


# ==============================
# VALIDAR INICIO DE SESIÓN
# ==============================

def validar_login(usuario, password):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_usuario, nombre, usuario, rol
        FROM usuario
        WHERE usuario = ? AND password = ?
    """, (usuario, password))

    resultado = cursor.fetchone()
    conexion.close()

    return resultado


# ==============================
# VENTANA PRINCIPAL
# ==============================

class SistemaInventario:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Inventario - Papelería")
        self.root.geometry("900x550")
        self.root.resizable(False, False)

        self.usuario_actual = None

        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==============================
    # LOGIN
    # ==============================

    def mostrar_login(self):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack(expand=True)

        titulo = tk.Label(
            frame,
            text="Sistema de Inventario",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            frame,
            text="Papelería Dunder Mifflin",
            font=("Arial", 14)
        )
        subtitulo.pack(pady=5)

        tk.Label(frame, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        self.entry_usuario = tk.Entry(frame, font=("Arial", 12), width=30)
        self.entry_usuario.pack()

        tk.Label(frame, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        self.entry_password = tk.Entry(frame, font=("Arial", 12), width=30, show="*")
        self.entry_password.pack()

        btn_login = tk.Button(
            frame,
            text="Iniciar sesión",
            font=("Arial", 12),
            width=20,
            command=self.iniciar_sesion
        )
        btn_login.pack(pady=20)

        ayuda = tk.Label(
            frame,
            text="Usuario de prueba: admin | Contraseña: admin123",
            font=("Arial", 10)
        )
        ayuda.pack(pady=5)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if usuario == "" or password == "":
            messagebox.showwarning("Campos vacíos", "Ingresa usuario y contraseña.")
            return

        resultado = validar_login(usuario, password)

        if resultado:
            self.usuario_actual = resultado
            messagebox.showinfo("Bienvenido", f"Bienvenido {resultado[1]}")
            self.mostrar_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    # ==============================
    # MENÚ PRINCIPAL
    # ==============================

    def mostrar_menu(self):
        self.limpiar_ventana()

        nombre = self.usuario_actual[1]
        rol = self.usuario_actual[3]

        titulo = tk.Label(
            self.root,
            text="Menú Principal",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        usuario_label = tk.Label(
            self.root,
            text=f"Usuario: {nombre} | Rol: {rol}",
            font=("Arial", 12)
        )
        usuario_label.pack(pady=5)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=30)

        botones = [
            ("Administrar productos", self.ventana_productos),
            ("Gestionar categorías", self.ventana_categorias),
            ("Gestionar proveedores", self.ventana_proveedores),
            ("Inventario", self.ventana_inventario),
            ("Registrar venta", self.ventana_ventas),
            ("Alertas de stock bajo", self.ventana_alertas),
            ("Reportes", self.ventana_reportes),
            ("Administrar usuarios", self.ventana_usuarios),
        ]

        fila = 0
        columna = 0

        for texto, comando in botones:
            btn = tk.Button(
                frame_botones,
                text=texto,
                width=25,
                height=2,
                font=("Arial", 11),
                command=comando
            )
            btn.grid(row=fila, column=columna, padx=10, pady=10)

            columna += 1
            if columna == 2:
                columna = 0
                fila += 1

        btn_salir = tk.Button(
            self.root,
            text="Cerrar sesión",
            width=20,
            font=("Arial", 11),
            command=self.mostrar_login
        )
        btn_salir.pack(pady=10)

    # ==============================
    # VENTANAS TEMPORALES
    # ==============================

    def mostrar_ventana_temporal(self, titulo, descripcion):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("500x300")
        ventana.resizable(False, False)

        label_titulo = tk.Label(
            ventana,
            text=titulo,
            font=("Arial", 18, "bold")
        )
        label_titulo.pack(pady=20)

        label_descripcion = tk.Label(
            ventana,
            text=descripcion,
            font=("Arial", 12),
            wraplength=420,
            justify="center"
        )
        label_descripcion.pack(pady=20)

        btn_cerrar = tk.Button(
            ventana,
            text="Cerrar",
            width=15,
            command=ventana.destroy
        )
        btn_cerrar.pack(pady=20)

    def ventana_productos(self):
        self.mostrar_ventana_temporal(
            "Administrar productos",
            "Aquí se registrarán, modificarán, eliminarán y consultarán los productos de la papelería."
        )

    def ventana_categorias(self):
        self.mostrar_ventana_temporal(
            "Gestionar categorías",
            "Aquí se administrarán las categorías de productos, como útiles escolares, papelería, oficina, etc."
        )

    def ventana_proveedores(self):
        self.mostrar_ventana_temporal(
            "Gestionar proveedores",
            "Aquí se registrarán los proveedores que suministran productos a la papelería."
        )

    def ventana_inventario(self):
        self.mostrar_ventana_temporal(
            "Inventario",
            "Aquí se controlarán las entradas, existencias y ubicación de los productos."
        )

    def ventana_ventas(self):
        self.mostrar_ventana_temporal(
            "Registrar venta",
            "Aquí el vendedor podrá seleccionar productos, calcular el total y registrar la venta."
        )

    def ventana_alertas(self):
        self.mostrar_ventana_temporal(
            "Alertas de stock bajo",
            "Aquí se mostrarán los productos que tienen existencia baja o llegaron al stock mínimo."
        )

    def ventana_reportes(self):
        self.mostrar_ventana_temporal(
            "Reportes",
            "Aquí se generarán reportes de inventario, ventas, movimientos y productos con bajo stock."
        )

    def ventana_usuarios(self):
        self.mostrar_ventana_temporal(
            "Administrar usuarios",
            "Aquí el administrador podrá registrar, modificar o desactivar usuarios del sistema."
        )

    def ejecutar(self):
        self.root.mainloop()


# ==============================
# INICIO DEL PROGRAMA
# ==============================

if __name__ == "__main__":
    crear_tablas()
    app = SistemaInventario()
    app.ejecutar()