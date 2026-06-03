# ==============================
# VISTA DE REGISTRO DE USUARIOS
# ==============================

"""
Esta pantalla permite registrar usuarios nuevos en el sistema.

Cumple con la parte de la documentación que pide:
- Login.
- Registro de usuario.

Campos:
- Nombre completo.
- Usuario.
- Contraseña.
- Rol.

Roles disponibles:
- Administrador.
- Vendedor.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Permite importar desde la raíz del proyecto.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from database.conexion import conectar_bd


class VentanaUsuarios(tk.Toplevel):
    """
    Ventana para registrar usuarios.

    Esta ventana puede abrirse desde el menú o desde el layout principal.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Registro de Usuarios")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#ecf0f1")

        self.crear_interfaz()
        self.cargar_usuarios()

    # ==============================
    # CREAR INTERFAZ
    # ==============================

    def crear_interfaz(self):
        """
        Crea todos los elementos visuales de la pantalla.
        """

        contenedor = tk.Frame(
            self,
            bg="white",
            padx=30,
            pady=30
        )
        contenedor.pack(fill="both", expand=True, padx=35, pady=35)

        titulo = tk.Label(
            contenedor,
            text="Registro de Usuario",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        titulo.pack(anchor="w", pady=(0, 20))

        # Nombre
        self.entry_nombre = self.crear_campo(
            contenedor,
            "Nombre completo:"
        )

        # Usuario
        self.entry_usuario = self.crear_campo(
            contenedor,
            "Nombre de usuario:"
        )

        # Contraseña
        self.entry_password = self.crear_campo(
            contenedor,
            "Contraseña:",
            password=True
        )

        # Rol
        lbl_rol = tk.Label(
            contenedor,
            text="Rol:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_rol.pack(anchor="w", pady=(8, 5))

        self.combo_rol = ttk.Combobox(
            contenedor,
            values=["Administrador", "Vendedor"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.combo_rol.pack(fill="x", ipady=5)
        self.combo_rol.set("Vendedor")

        # Botones
        frame_botones = tk.Frame(contenedor, bg="white")
        frame_botones.pack(fill="x", pady=20)

        btn_registrar = tk.Button(
            frame_botones,
            text="Registrar Usuario",
            bg="#e67e22",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.registrar_usuario
        )
        btn_registrar.pack(side="left", padx=(0, 10))

        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=12,
            height=2,
            command=self.limpiar_formulario
        )
        btn_limpiar.pack(side="left")

        # Tabla de usuarios
        lbl_lista = tk.Label(
            contenedor,
            text="Usuarios registrados",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_lista.pack(anchor="w", pady=(15, 8))

        columnas = ("id", "nombre", "usuario", "rol")

        self.tabla_usuarios = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=6
        )

        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("rol", text="Rol")

        self.tabla_usuarios.column("id", width=50, anchor="center")
        self.tabla_usuarios.column("nombre", width=180)
        self.tabla_usuarios.column("usuario", width=120)
        self.tabla_usuarios.column("rol", width=120)

        self.tabla_usuarios.pack(fill="both", expand=True)

    def crear_campo(self, parent, texto, password=False):
        """
        Crea una etiqueta y una caja de texto.

        parent: contenedor.
        texto: texto de la etiqueta.
        password: si es True, oculta lo escrito.
        """

        label = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        label.pack(anchor="w", pady=(8, 5))

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            show="*" if password else ""
        )
        entry.pack(fill="x", ipady=5)

        return entry

    # ==============================
    # REGISTRAR USUARIO
    # ==============================

    def registrar_usuario(self):
        """
        Registra un usuario nuevo en la base de datos.
        """

        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        rol = self.combo_rol.get().strip()

        if nombre == "" or usuario == "" or password == "" or rol == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Debes llenar todos los campos."
            )
            return

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuario (
                    nombre,
                    usuario,
                    password,
                    rol
                )
                VALUES (?, ?, ?, ?)
            """, (
                nombre,
                usuario,
                password,
                rol
            ))

            conexion.commit()
            conexion.close()

            messagebox.showinfo(
                "Éxito",
                "Usuario registrado correctamente."
            )

            self.limpiar_formulario()
            self.cargar_usuarios()

        except Exception as error:
            mensaje_error = str(error)

            if "UNIQUE" in mensaje_error or "unique" in mensaje_error:
                messagebox.showerror(
                    "Usuario duplicado",
                    "Ese nombre de usuario ya existe."
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo registrar el usuario.\n\nDetalle: {error}"
                )

    # ==============================
    # CARGAR USUARIOS
    # ==============================

    def cargar_usuarios(self):
        """
        Muestra los usuarios registrados en la tabla.
        """

        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

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
                ORDER BY id_usuario ASC
            """)

            usuarios = cursor.fetchall()
            conexion.close()

            for usuario in usuarios:
                self.tabla_usuarios.insert(
                    "",
                    "end",
                    values=usuario
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los usuarios.\n\nDetalle: {error}"
            )

    # ==============================
    # LIMPIAR FORMULARIO
    # ==============================

    def limpiar_formulario(self):
        """
        Limpia los campos del formulario.
        """

        self.entry_nombre.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_rol.set("Vendedor")


# ==============================
# FUNCIÓN PARA ABRIR USUARIOS
# ==============================

def abrir_usuarios(parent=None):
    """
    Abre la ventana de usuarios.
    """

    ventana = VentanaUsuarios(parent)
    ventana.grab_set()
    return ventana


# ==============================
# PRUEBA DIRECTA
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    VentanaUsuarios(root)
    root.mainloop()
    