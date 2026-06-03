# ==============================
# Vista MENU
# ==============================

import tkinter as tk
from tkinter import ttk, messagebox


class MenuView(tk.Toplevel):
    """
    Esta clase representa el menú principal del sistema.

    Muestra diferentes opciones según el rol del usuario:
    - Administrador: acceso a todas las funciones.
    - Vendedor: acceso limitado.

    Desde aquí se navega a las demás ventanas del sistema.
    """

    def __init__(self, parent, usuario):
        """
        parent: ventana principal.
        usuario: usuario autenticado.
        """

        super().__init__(parent)

        self.parent = parent
        self.usuario = usuario

        # Obtenemos nombre y rol de forma segura.
        self.nombre_usuario = self._obtener_nombre_usuario()
        self.rol_usuario = self._obtener_rol_usuario()

        self.title(f"Dunder Mifflin - Menú Principal ({self.rol_usuario})")
        self.geometry("900x600")
        self.configure(bg="#e8ecef")
        self.resizable(False, False)

        self._centrar_ventana()
        self._construir_interfaz()

    # ==============================
    # OBTENER DATOS DEL USUARIO
    # ==============================

    def _obtener_nombre_usuario(self):
        """
        Obtiene el nombre del usuario aunque venga como objeto,
        diccionario o tupla.
        """

        if hasattr(self.usuario, "nombre"):
            return self.usuario.nombre

        if isinstance(self.usuario, dict):
            return self.usuario.get("nombre", "Usuario")

        if isinstance(self.usuario, tuple) or isinstance(self.usuario, list):
            if len(self.usuario) > 1:
                return self.usuario[1]

        return "Usuario"

    def _obtener_rol_usuario(self):
        """
        Obtiene el rol del usuario aunque venga como objeto,
        diccionario o tupla.
        """

        if hasattr(self.usuario, "rol"):
            return self.usuario.rol

        if isinstance(self.usuario, dict):
            return self.usuario.get("rol", "Administrador")

        if isinstance(self.usuario, tuple) or isinstance(self.usuario, list):
            if len(self.usuario) > 3:
                return self.usuario[3]

        return "Administrador"

    # ==============================
    # MÉTODOS PRIVADOS
    # ==============================

    def _centrar_ventana(self):
        """
        Centra la ventana en la pantalla.
        """

        self.update_idletasks()

        ancho = 900
        alto = 600

        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _construir_interfaz(self):
        """
        Construye todos los elementos visuales del menú principal.
        """

        frame_principal = tk.Frame(self, bg="#e8ecef")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        lbl_bienvenida = tk.Label(
            frame_principal,
            text=f"Bienvenido, {self.nombre_usuario}",
            font=("Segoe UI", 24, "bold"),
            bg="#e8ecef",
            fg="#2c3e50"
        )
        lbl_bienvenida.pack(pady=(0, 5))

        lbl_rol = tk.Label(
            frame_principal,
            text=f"Rol: {self.rol_usuario}",
            font=("Segoe UI", 14),
            bg="#e8ecef",
            fg="#7f8c8d"
        )
        lbl_rol.pack(pady=(0, 30))

        separador = ttk.Separator(frame_principal, orient="horizontal")
        separador.pack(fill=tk.X, pady=10)

        frame_botones = tk.Frame(frame_principal, bg="#e8ecef")
        frame_botones.pack(pady=30)

        if self.rol_usuario == "Administrador":
            botones = [
                ("Administrar Productos", self._abrir_productos),
                ("Gestionar Categorías", self._abrir_categorias),
                ("Gestionar Proveedores", self._abrir_proveedores),
                ("Control de Inventario", self._abrir_inventario),
                ("Registrar Venta", self._abrir_ventas),
                ("Alertas de Stock", self._abrir_alertas),
                ("Generar Reportes", self._abrir_reportes),
                ("Administrar Usuarios", self._abrir_usuarios),
            ]
        else:
            botones = [
                ("Consultar Productos", self._abrir_productos),
                ("Registrar Venta", self._abrir_ventas),
                ("Alertas de Stock", self._abrir_alertas),
            ]

        for i, (texto, comando) in enumerate(botones):
            btn = tk.Button(
                frame_botones,
                text=texto,
                font=("Segoe UI", 11),
                bg="#e67e22",
                fg="white",
                activebackground="#d35400",
                activeforeground="white",
                cursor="hand2",
                relief=tk.FLAT,
                width=25,
                height=2,
                command=comando
            )
            btn.grid(row=i // 2, column=i % 2, padx=15, pady=15)

        btn_salir = tk.Button(
            frame_principal,
            text="Cerrar Sesión",
            font=("Segoe UI", 11),
            bg="#7f8c8d",
            fg="white",
            activebackground="#6c7a7d",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            width=20,
            command=self._cerrar_sesion
        )
        btn_salir.pack(pady=20)

    # ==============================
    # MÉTODOS PARA ABRIR VENTANAS
    # ==============================

    def _abrir_productos(self):
        """
        Abre la ventana real de productos.

        Esta ya debe existir en:
        views/productos_view.py
        """

        try:
            from views.productos_view import VentanaProductos

            ventana = VentanaProductos(self)
            ventana.focus_set()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir la ventana de productos.\n\nDetalle: {error}"
            )

    def _abrir_categorias(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Gestión de Categorías")

    def _abrir_proveedores(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Gestión de Proveedores")

    def _abrir_inventario(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Control de Inventario")

    def _abrir_ventas(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Registro de Ventas")

    def _abrir_alertas(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Alertas de Stock")

    def _abrir_reportes(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Reportes")

    def _abrir_usuarios(self):
        """
        Ventana pendiente.
        """

        self._mostrar_pendiente("Administración de Usuarios")

    def _mostrar_pendiente(self, modulo):
        """
        Muestra un aviso para módulos que todavía no tienen ventana lista.
        """

        messagebox.showinfo(
            "Módulo pendiente",
            f"El módulo '{modulo}' todavía no está conectado a una ventana funcional."
        )

    def _cerrar_sesion(self):
        """
        Cierra el menú y vuelve a mostrar la ventana principal si existe.
        """

        confirmar = messagebox.askyesno(
            "Cerrar sesión",
            "¿Seguro que deseas cerrar sesión?"
        )

        if not confirmar:
            return

        self.destroy()

        try:
            self.parent.deiconify()
        except Exception:
            pass

    # ==============================
    # MÉTODOS PÚBLICOS
    # ==============================

    def mostrar(self):
        """
        Muestra la ventana del menú.
        """

        self.wait_window()


# ==============================
# PRUEBA DIRECTA
# ==============================

if __name__ == "__main__":
    class UsuarioPrueba:
        def __init__(self):
            self.nombre = "Administrador"
            self.rol = "Administrador"

    root = tk.Tk()
    root.withdraw()

    menu = MenuView(root, UsuarioPrueba())
    menu.mainloop()