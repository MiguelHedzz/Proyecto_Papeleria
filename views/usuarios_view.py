# ==============================
# VISTA DE USUARIOS
# ==============================

"""
Pantalla para administrar usuarios.

Permite:
- Registrar usuario.
- Listar usuarios.
- Seleccionar usuario.
- Actualizar usuario.
- Cambiar rol.
- Activar/desactivar usuario.
- Ocultar contrasenas en la tabla.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.usuario_controller import UsuarioController


class VentanaUsuarios(tk.Toplevel):
    """
    Ventana para administrar usuarios.
    """

    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)

        self.title("Usuarios")
        self.geometry("900x650")
        self.minsize(820, 600)
        self.configure(bg="#ecf0f1")

        self.usuario_actual = usuario
        self.usuario_controller = UsuarioController()
        self.id_usuario_seleccionado = None

        self.crear_interfaz()
        self.cargar_usuarios()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Usuarios",
            font=("Segoe UI", 24, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_form = tk.LabelFrame(
            card,
            text="Datos del usuario",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(fill="x", pady=(0, 15))

        self.entry_nombre = self.crear_campo(frame_form, "Nombre completo:", 0, 0)
        self.entry_usuario = self.crear_campo(frame_form, "Usuario:", 0, 2)
        self.entry_password = self.crear_campo(frame_form, "Contrasena:", 1, 0, password=True)

        tk.Label(
            frame_form,
            text="Rol:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        ).grid(row=1, column=2, sticky="w", padx=(0, 8), pady=8)

        self.combo_rol = ttk.Combobox(
            frame_form,
            values=["Administrador", "Vendedor"],
            state="readonly",
            font=("Segoe UI", 10),
            width=24
        )
        self.combo_rol.grid(row=1, column=3, sticky="w", padx=(0, 20), pady=8, ipady=4)
        self.combo_rol.set("Vendedor")

        nota = tk.Label(
            frame_form,
            text="Nota: al actualizar, deja la contrasena vacia para conservar la actual.",
            bg="white",
            fg="#7f8c8d",
            font=("Segoe UI", 9)
        )
        nota.grid(row=2, column=0, columnspan=4, sticky="w", pady=(5, 0))

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Registrar", "#e67e22", self.registrar_usuario).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#e67e22", self.actualizar_usuario).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Desactivar", "#e74c3c", self.desactivar_usuario).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Activar", "#27ae60", self.activar_usuario).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Limpiar", "#95a5a6", self.limpiar_formulario).pack(side="left", padx=(0, 10))

        frame_tabla = tk.LabelFrame(
            card,
            text="Usuarios registrados",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "usuario", "rol", "estado")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("nombre", text="Nombre")
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("rol", text="Rol")
        self.tabla_usuarios.heading("estado", text="Estado")

        self.tabla_usuarios.column("id", width=60, anchor="center")
        self.tabla_usuarios.column("nombre", width=260)
        self.tabla_usuarios.column("usuario", width=180)
        self.tabla_usuarios.column("rol", width=150, anchor="center")
        self.tabla_usuarios.column("estado", width=120, anchor="center")

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario)

    def crear_campo(self, parent, texto, fila, columna, password=False):
        tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 8), pady=8)

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            show="*" if password else "",
            width=28
        )
        entry.grid(row=fila, column=columna + 1, sticky="w", padx=(0, 20), pady=8, ipady=4)
        return entry

    def crear_boton(self, parent, texto, color, comando):
        return tk.Button(
            parent,
            text=texto,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=14,
            height=2,
            command=comando
        )

    def cargar_usuarios(self):
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        usuarios = self.usuario_controller.listar_usuarios()

        for usuario in usuarios:
            estado = "Activo" if int(usuario[4]) == 1 else "Inactivo"
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(usuario[0], usuario[1], usuario[2], usuario[3], estado)
            )

    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        rol = self.combo_rol.get().strip()

        resultado, mensaje = self.usuario_controller.registrar_usuario(
            nombre=nombre,
            usuario=usuario,
            password=password,
            rol=rol
        )

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        self.id_usuario_seleccionado = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_usuario.delete(0, tk.END)
        self.entry_usuario.insert(0, valores[2])

        self.entry_password.delete(0, tk.END)
        self.combo_rol.set(valores[3])

    def actualizar_usuario(self):
        if self.id_usuario_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla.")
            return

        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        nueva_password = self.entry_password.get().strip()
        rol = self.combo_rol.get().strip()

        resultado, mensaje = self.usuario_controller.actualizar_usuario(
            id_usuario=self.id_usuario_seleccionado,
            nombre=nombre,
            usuario=usuario,
            rol=rol,
            nueva_password=nueva_password if nueva_password else None
        )

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def desactivar_usuario(self):
        if self.id_usuario_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que deseas desactivar este usuario?")
        if not confirmar:
            return

        resultado, mensaje = self.usuario_controller.desactivar_usuario(self.id_usuario_seleccionado)

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def activar_usuario(self):
        if self.id_usuario_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla.")
            return

        resultado, mensaje = self.usuario_controller.activar_usuario(self.id_usuario_seleccionado)

        if resultado:
            messagebox.showinfo("Exito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_usuario_seleccionado = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_rol.set("Vendedor")

        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            self.tabla_usuarios.selection_remove(seleccion)


def abrir_usuarios(parent=None, usuario=None):
    ventana = VentanaUsuarios(parent, usuario)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaUsuarios(root)
    root.mainloop()
