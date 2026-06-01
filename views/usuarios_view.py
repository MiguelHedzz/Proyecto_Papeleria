# ==============================
# VISTA DE USUARIOS
# ==============================

"""
Esta pantalla permite administrar los usuarios del sistema.

Funciones principales:
- Registrar nuevo usuario.
- Listar usuarios.
- Buscar usuario por nombre.
- Editar usuario (nombre, usuario, rol, contraseña).
- Desactivar/Activar usuario.
- Eliminar usuario (solo si no tiene ventas asociadas).
- Cambiar contraseña.

Esta vista se conecta con:
controllers/usuario_controller.py

Solo accesible para usuarios con rol Administrador.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from controllers.usuario_controller import UsuarioController


class UsuariosView(tk.Toplevel):
    """Pantalla de administración de usuarios."""

    def __init__(self, parent, usuario=None):
        super().__init__(parent)

        self.title("Dunder Mifflin - Administrar Usuarios")
        self.geometry("1100x650")
        self.configure(bg="#e8ecef")
        self.resizable(True, True)

        self._centrar_ventana()
        self.usuario_actual = usuario
        self.usuario_controller = UsuarioController()

        self.id_usuario_seleccionado = None
        self._construir_interfaz()
        self.cargar_usuarios()

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

        rol_texto = self.usuario_actual.rol if self.usuario_actual else "Administrador"
        lbl_rol = tk.Label(frame_sidebar, text=f"Rol: {rol_texto}", font=("Segoe UI", 11), bg="#3a4f63", fg="#b0c0d0")
        lbl_rol.pack(pady=(0, 30))

        nav_items = [
            ("Productos", self._ir_a_productos),
            ("Inventario", self._ir_a_inventario),
            ("Ventas", self._ir_a_ventas),
            ("Reportes", self._ir_a_reportes),
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

        btn_usuarios = tk.Button(frame_acciones, text="Administrar Usuarios", font=("Segoe UI", 10, "bold"),
                                 bg="white", fg="#2c3e50", activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2")
        btn_usuarios.pack(side=tk.LEFT, padx=5)

        btn_soporte = tk.Button(frame_acciones, text="Soporte", font=("Segoe UI", 10), bg="white", fg="#2c3e50",
                                activebackground="#e8ecef", relief=tk.FLAT, cursor="hand2", command=self._ir_a_soporte)
        btn_soporte.pack(side=tk.LEFT, padx=5)

    def _crear_content(self, parent):
        frame_content = tk.Frame(parent, bg="#e8ecef")
        frame_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        card = tk.Frame(frame_content, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_titulo = tk.Label(card, text="Administrar Usuarios", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        lbl_advertencia = tk.Label(card, text="⚠️ Solo Administradores pueden gestionar usuarios",
                                   font=("Segoe UI", 10), bg="white", fg="#e74c3c")
        lbl_advertencia.pack(pady=(0, 10), padx=20, anchor="w")

        frame_contenido_card = tk.Frame(card, bg="white")
        frame_contenido_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Formulario
        self._crear_formulario(frame_contenido_card)

        # Botones de acción
        self._crear_botones_accion(frame_contenido_card)

        # Tabla de usuarios
        self._crear_tabla(frame_contenido_card)

    def _crear_formulario(self, parent):
        frame_campos = tk.Frame(parent, bg="white")
        frame_campos.pack(fill=tk.X, pady=10)

        # Nombre completo
        tk.Label(frame_campos, text="Nombre completo:", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_campos, width=35, font=("Segoe UI", 10))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Nombre de usuario
        tk.Label(frame_campos, text="Usuario:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_usuario = tk.Entry(frame_campos, width=35, font=("Segoe UI", 10))
        self.entry_usuario.grid(row=1, column=1, padx=5, pady=5)

        # Contraseña
        tk.Label(frame_campos, text="Contraseña:", bg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_password = tk.Entry(frame_campos, width=35, font=("Segoe UI", 10), show="•")
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)

        # Rol
        tk.Label(frame_campos, text="Rol:", bg="white", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_rol = ttk.Combobox(frame_campos, values=["Administrador", "Vendedor"], width=33, font=("Segoe UI", 10))
        self.combo_rol.current(1)
        self.combo_rol.grid(row=3, column=1, padx=5, pady=5)

        # Estado
        tk.Label(frame_campos, text="Estado:", bg="white", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.combo_estado = ttk.Combobox(frame_campos, values=["Activo", "Inactivo"], width=33, font=("Segoe UI", 10))
        self.combo_estado.current(0)
        self.combo_estado.grid(row=4, column=1, padx=5, pady=5)

    def _crear_botones_accion(self, parent):
        frame_botones = tk.Frame(parent, bg="white")
        frame_botones.pack(fill=tk.X, pady=15)

        btn_registrar = tk.Button(frame_botones, text="Registrar Usuario", font=("Segoe UI", 10, "bold"),
                                  bg="#27ae60", fg="white", activebackground="#219a52", cursor="hand2",
                                  relief=tk.FLAT, padx=15, command=self.registrar_usuario)
        btn_registrar.grid(row=0, column=0, padx=5, pady=5)

        btn_actualizar = tk.Button(frame_botones, text="Actualizar Usuario", font=("Segoe UI", 10, "bold"),
                                   bg="#e67e22", fg="white", activebackground="#d35400", cursor="hand2",
                                   relief=tk.FLAT, padx=15, command=self.actualizar_usuario)
        btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

        btn_cambiar_password = tk.Button(frame_botones, text="Cambiar Contraseña", font=("Segoe UI", 10),
                                         bg="#7f8c8d", fg="white", activebackground="#6c7a7d", cursor="hand2",
                                         relief=tk.FLAT, padx=15, command=self.cambiar_password)
        btn_cambiar_password.grid(row=0, column=2, padx=5, pady=5)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar", font=("Segoe UI", 10),
                                bg="#95a5a6", fg="white", activebackground="#7f8c8d", cursor="hand2",
                                relief=tk.FLAT, padx=15, command=self.limpiar_formulario)
        btn_limpiar.grid(row=0, column=3, padx=5, pady=5)

        # Fila 2: Búsqueda
        tk.Label(frame_botones, text="Buscar usuario:", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_buscar = tk.Entry(frame_botones, width=30, font=("Segoe UI", 10))
        self.entry_buscar.grid(row=1, column=1, padx=5, pady=5)

        btn_buscar = tk.Button(frame_botones, text="Buscar", font=("Segoe UI", 10), bg="#e67e22", fg="white",
                               activebackground="#d35400", cursor="hand2", relief=tk.FLAT, padx=10,
                               command=self.buscar_usuario)
        btn_buscar.grid(row=1, column=2, padx=5, pady=5)

        btn_mostrar_todos = tk.Button(frame_botones, text="Mostrar todos", font=("Segoe UI", 10), bg="#7f8c8d", fg="white",
                                      activebackground="#6c7a7d", cursor="hand2", relief=tk.FLAT,
                                      command=self.cargar_usuarios)
        btn_mostrar_todos.grid(row=1, column=3, padx=5, pady=5)

    def _crear_tabla(self, parent):
        frame_tabla = tk.LabelFrame(parent, text="Lista de Usuarios", font=("Segoe UI", 11, "bold"),
                                     bg="white", fg="#2c3e50", padx=10, pady=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

        columnas = ("id", "nombre", "usuario", "rol", "estado")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("nombre", text="Nombre Completo")
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("rol", text="Rol")
        self.tabla_usuarios.heading("estado", text="Estado")

        self.tabla_usuarios.column("id", width=50, anchor="center")
        self.tabla_usuarios.column("nombre", width=250)
        self.tabla_usuarios.column("usuario", width=150, anchor="center")
        self.tabla_usuarios.column("rol", width=120, anchor="center")
        self.tabla_usuarios.column("estado", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario)

    def cargar_usuarios(self):
        """Carga todos los usuarios en la tabla."""
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        usuarios = self.usuario_controller.listar_usuarios()

        for usuario in usuarios:
            # usuario: (id_usuario, nombre, usuario, rol)
            estado = "Activo"  # Por ahora, hasta que se agregue campo estado
            self.tabla_usuarios.insert("", "end", values=(
                usuario[0], usuario[1], usuario[2], usuario[3], estado
            ))

        self.entry_buscar.delete(0, tk.END)

    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario."""
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        rol = self.combo_rol.get()
        estado = self.combo_estado.get()
        return nombre, usuario, password, rol, estado

    def registrar_usuario(self):
        """Registra un nuevo usuario."""
        nombre, usuario, password, rol, estado = self.obtener_datos_formulario()

        if not nombre or not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Nombre, usuario y contraseña son obligatorios.")
            return

        resultado, mensaje = self.usuario_controller.registrar_usuario(nombre, usuario, password, rol)

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_usuario(self, event):
        """Carga el usuario seleccionado en el formulario."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        self.id_usuario_seleccionado = valores[0]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_usuario.delete(0, tk.END)
        self.entry_usuario.insert(0, valores[2])

        self.combo_rol.set(valores[3])

        # Estado (por ahora, hasta agregar campo)
        estado = valores[4] if len(valores) > 4 else "Activo"
        self.combo_estado.set(estado)

        self.entry_password.delete(0, tk.END)

    def actualizar_usuario(self):
        """Actualiza el usuario seleccionado."""
        if self.id_usuario_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla.")
            return

        nombre, usuario, password, rol, estado = self.obtener_datos_formulario()

        if not nombre or not usuario:
            messagebox.showwarning("Campos vacíos", "Nombre y usuario son obligatorios.")
            return

        # Si se ingresó nueva contraseña, actualizarla
        if password:
            resultado, mensaje = self.usuario_controller.actualizar_usuario(
                self.id_usuario_seleccionado, nombre, usuario, rol, password
            )
        else:
            resultado, mensaje = self.usuario_controller.actualizar_usuario(
                self.id_usuario_seleccionado, nombre, usuario, rol
            )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def cambiar_password(self):
        """Ventana para cambiar la contraseña de un usuario."""
        if self.id_usuario_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un usuario de la tabla.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text=f"Usuario: {self.entry_usuario.get()}", font=("Segoe UI", 11, "bold")).pack(pady=10)

        tk.Label(dialog, text="Nueva contraseña:", font=("Segoe UI", 10)).pack()
        entry_nueva = tk.Entry(dialog, font=("Segoe UI", 10), show="•", width=30)
        entry_nueva.pack(pady=5)

        tk.Label(dialog, text="Confirmar contraseña:", font=("Segoe UI", 10)).pack()
        entry_confirmar = tk.Entry(dialog, font=("Segoe UI", 10), show="•", width=30)
        entry_confirmar.pack(pady=5)

        def guardar_password():
            nueva = entry_nueva.get().strip()
            confirmar = entry_confirmar.get().strip()

            if not nueva:
                messagebox.showerror("Error", "Ingresa una contraseña")
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            resultado, mensaje = self.usuario_controller.actualizar_usuario(
                self.id_usuario_seleccionado,
                self.entry_nombre.get().strip(),
                self.entry_usuario.get().strip(),
                self.combo_rol.get(),
                nueva
            )

            if resultado:
                messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje)

        btn_guardar = tk.Button(dialog, text="Guardar", command=guardar_password, bg="#e67e22", fg="white", relief=tk.FLAT, padx=20)
        btn_guardar.pack(pady=15)

    def buscar_usuario(self):
        """Busca usuarios por nombre."""
        nombre = self.entry_buscar.get().strip()

        if not nombre:
            messagebox.showwarning("Aviso", "Ingresa un nombre para buscar")
            return

        usuarios = self.usuario_controller.buscar_por_nombre(nombre)

        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        for usuario in usuarios:
            self.tabla_usuarios.insert("", "end", values=(
                usuario[0], usuario[1], usuario[2], usuario[3], "Activo"
            ))

        if len(usuarios) == 0:
            messagebox.showinfo("Sin resultados", "No se encontraron usuarios con ese nombre")

    def limpiar_formulario(self):
        """Limpia el formulario."""
        self.id_usuario_seleccionado = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_rol.current(1)
        self.combo_estado.current(0)
        self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())

    # ==============================
    # MÉTODOS DE NAVEGACIÓN
    # ==============================

    def _ir_a_productos(self):
        from views.productos_view import ProductosView
        self.destroy()
        ventana = ProductosView(self.master, self.usuario_actual)
        ventana.focus_set()

    def _ir_a_inventario(self):
        from views.inventario_view import InventarioView
        self.destroy()
        ventana = InventarioView(self.master, self.usuario_actual)
        ventana.focus_set()

    def _ir_a_ventas(self):
        from views.ventas_view import VentasView
        self.destroy()
        ventana = VentasView(self.master, self.usuario_actual)
        ventana.focus_set()

    def _ir_a_reportes(self):
        from views.reportes_view import ReportesView
        self.destroy()
        ventana = ReportesView(self.master, self.usuario_actual)
        ventana.focus_set()

    def _ir_a_alertas(self):
        from views.alertas_view import AlertasView
        self.destroy()
        ventana = AlertasView(self.master, self.usuario_actual)
        ventana.focus_set()

    def _ir_a_soporte(self):
        messagebox.showinfo("Soporte", "Contacta al administrador del sistema")

    def _cerrar_sesion(self):
        from views.login_view import LoginView
        self.destroy()
        login = LoginView(self.master)
        login.focus_set()


def abrir_usuarios(parent=None, usuario=None):
    ventana = UsuariosView(parent, usuario)
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana = UsuariosView(root)
    ventana.mainloop()