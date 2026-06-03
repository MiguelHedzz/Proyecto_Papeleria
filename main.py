# ==============================
# ARCHIVO PRINCIPAL DEL SISTEMA
# ==============================

"""
Este archivo inicia la aplicación.

Funciones principales:
- Crear las tablas de la base de datos.
- Mostrar la pantalla de inicio de sesión.
- Validar usuario y contraseña.
- Abrir el layout principal basado en el diseño de Figma.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass

# Permite importar correctamente desde la raíz del proyecto.
RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from database.crear_tablas import crear_tablas
from database.conexion import conectar_bd
from views.layout_view import LayoutPrincipal


# ==============================
# CLASE PARA GUARDAR SESIÓN
# ==============================

@dataclass
class UsuarioSesion:
    """
    Guarda los datos del usuario que inició sesión.

    Estos datos se mandan al LayoutPrincipal para mostrar:
    - Nombre del usuario.
    - Rol del usuario.
    """

    id_usuario: int
    nombre: str
    usuario: str
    rol: str


# ==============================
# APLICACIÓN PRINCIPAL
# ==============================

class AplicacionInventario:
    """
    Clase principal del sistema.

    Se encarga del login y de abrir la pantalla principal.
    """

    def __init__(self):
        """
        Inicializa la aplicación.
        """

        # Creamos las tablas si no existen.
        crear_tablas()

        # Creamos la ventana de login.
        self.root = tk.Tk()
        self.root.title("Dunder Mifflin - Sistema de Inventario")
        self.root.geometry("500x430")
        self.root.resizable(False, False)
        self.root.configure(bg="#ecf0f1")

        self.centrar_ventana()
        self.crear_login()

    # ==============================
    # CENTRAR VENTANA
    # ==============================

    def centrar_ventana(self):
        """
        Centra la ventana de login en la pantalla.
        """

        self.root.update_idletasks()

        ancho = 500
        alto = 430

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ==============================
    # CREAR LOGIN
    # ==============================

    def crear_login(self):
        """
        Crea la pantalla de inicio de sesión.
        """

        frame_login = tk.Frame(
            self.root,
            bg="white",
            padx=35,
            pady=35
        )
        frame_login.pack(expand=True)

        titulo = tk.Label(
            frame_login,
            text="Dunder Mifflin",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        titulo.pack(pady=(0, 5))

        subtitulo = tk.Label(
            frame_login,
            text="Sistema de Inventario",
            font=("Segoe UI", 13),
            bg="white",
            fg="#7f8c8d"
        )
        subtitulo.pack(pady=(0, 25))

        # Campo usuario.
        lbl_usuario = tk.Label(
            frame_login,
            text="Usuario:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_usuario.pack(anchor="w")

        self.entry_usuario = tk.Entry(
            frame_login,
            font=("Segoe UI", 11),
            width=30,
            relief="solid",
            bd=1
        )
        self.entry_usuario.pack(pady=(5, 15), ipady=5)

        # Campo contraseña.
        lbl_password = tk.Label(
            frame_login,
            text="Contraseña:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_password.pack(anchor="w")

        self.entry_password = tk.Entry(
            frame_login,
            font=("Segoe UI", 11),
            width=30,
            show="*",
            relief="solid",
            bd=1
        )
        self.entry_password.pack(pady=(5, 20), ipady=5)

        # Botón iniciar sesión.
        btn_login = tk.Button(
            frame_login,
            text="Iniciar sesión",
            font=("Segoe UI", 11, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=24,
            height=2,
            command=self.iniciar_sesion
        )
        btn_login.pack(pady=10)

        # Usuario de prueba.
        ayuda = tk.Label(
            frame_login,
            text="Usuario: admin   |   Contraseña: admin123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#7f8c8d"
        )
        ayuda.pack(pady=(15, 0))

        # Permite iniciar sesión con Enter.
        self.root.bind("<Return>", lambda event: self.iniciar_sesion())

    # ==============================
    # VALIDAR USUARIO
    # ==============================

    def validar_usuario(self, usuario, password):
        """
        Valida usuario y contraseña en la base de datos.

        Retorna:
        UsuarioSesion si las credenciales son correctas.
        None si son incorrectas.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    usuario,
                    rol
                FROM usuario
                WHERE usuario = ? AND password = ?
            """, (
                usuario,
                password
            ))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return UsuarioSesion(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    usuario=resultado[2],
                    rol=resultado[3]
                )

            return None

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo validar el usuario.\n\nDetalle: {error}"
            )
            return None

    # ==============================
    # INICIAR SESIÓN
    # ==============================

    def iniciar_sesion(self):
        """
        Valida el login y abre el layout principal.
        """

        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if usuario == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Ingresa usuario y contraseña."
            )
            return

        usuario_sesion = self.validar_usuario(usuario, password)

        if usuario_sesion is None:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )
            return

        # Ocultamos el login.
        self.root.withdraw()

        # Abrimos la pantalla principal basada en Figma.
        ventana_principal = LayoutPrincipal(
            parent=self.root,
            usuario=usuario_sesion
        )

        ventana_principal.focus_set()

        # Si cierran la pantalla principal, se cierra todo el programa.
        ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    # ==============================
    # CERRAR APLICACIÓN
    # ==============================

    def cerrar_aplicacion(self):
        """
        Cierra completamente la aplicación.
        """

        confirmar = messagebox.askyesno(
            "Salir",
            "¿Seguro que deseas salir del sistema?"
        )

        if confirmar:
            self.root.destroy()

    # ==============================
    # EJECUTAR
    # ==============================

    def ejecutar(self):
        """
        Mantiene abierta la aplicación.
        """

        self.root.mainloop()


# ==============================
# INICIO DEL PROGRAMA
# ==============================

if __name__ == "__main__":
    app = AplicacionInventario()
    app.ejecutar()