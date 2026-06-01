# ==============================
# Vista MENU 
# ==============================

import tkinter as tk
from tkinter import ttk, messagebox


class MenuView(tk.Toplevel):
    """
    Esta clase representa el menú principal del sistema.

    Muestra diferentes opciones según el rol del usuario:
    - Administrador: acceso a todas las funciones
    - Vendedor: acceso limitado (ventas, productos, alertas)

    Desde aquí se navega a todas las demás ventanas del sistema.
    """

    def __init__(self, parent, usuario):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto MenuView.

        Parámetros:
        parent: Widget padre.
        usuario: Objeto Usuario autenticado (contiene id, nombre, rol).
        """

        super().__init__(parent)
        self.parent = parent
        self.usuario = usuario

        # Configuramos la ventana.
        self.title(f"Dunder Mifflin - Menú Principal ({self.usuario.rol})")
        self.geometry("900x600")
        self.configure(bg="#e8ecef")

        # Centramos la ventana.
        self._centrar_ventana()

        # Construimos la interfaz.
        self._construir_interfaz()

    # ==============================
    # MÉTODOS PRIVADOS
    # ==============================

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"+{x}+{y}")

    def _construir_interfaz(self):
        """Construye todos los elementos visuales del menú principal."""

        # Frame principal con padding.
        frame_principal = tk.Frame(self, bg="#e8ecef")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Título de bienvenida.
        lbl_bienvenida = tk.Label(
            frame_principal,
            text=f"Bienvenido, {self.usuario.nombre}",
            font=("Segoe UI", 24, "bold"),
            bg="#e8ecef",
            fg="#2c3e50"
        )
        lbl_bienvenida.pack(pady=(0, 5))

        # Rol del usuario.
        lbl_rol = tk.Label(
            frame_principal,
            text=f"Rol: {self.usuario.rol}",
            font=("Segoe UI", 14),
            bg="#e8ecef",
            fg="#7f8c8d"
        )
        lbl_rol.pack(pady=(0, 30))

        # Separador.
        separador = ttk.Separator(frame_principal, orient='horizontal')
        separador.pack(fill=tk.X, pady=10)

        # Frame para los botones (grid de 2 columnas).
        frame_botones = tk.Frame(frame_principal, bg="#e8ecef")
        frame_botones.pack(pady=30)

        # Botones según el rol.
        if self.usuario.rol == "Administrador":
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

        # Creamos los botones en grid.
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

        # Botón de cerrar sesión.
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
        """Abre la ventana de administración de productos."""
        try:
            from views.productos_view import ProductosView
            ventana = ProductosView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de productos en construcción")

    def _abrir_categorias(self):
        """Abre la ventana de gestión de categorías."""
        try:
            from views.categorias_view import CategoriasView
            ventana = CategoriasView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de categorías en construcción")

    def _abrir_proveedores(self):
        """Abre la ventana de gestión de proveedores."""
        try:
            from views.proveedores_view import ProveedoresView
            ventana = ProveedoresView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de proveedores en construcción")

    def _abrir_inventario(self):
        """Abre la ventana de control de inventario."""
        try:
            from views.inventario_view import InventarioView
            ventana = InventarioView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de inventario en construcción")

    def _abrir_ventas(self):
        """Abre la ventana de registro de ventas."""
        try:
            from views.ventas_view import VentasView
            ventana = VentasView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de ventas en construcción")

    def _abrir_alertas(self):
        """Abre la ventana de alertas de stock bajo."""
        try:
            from views.alertas_view import AlertasView
            ventana = AlertasView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de alertas en construcción")

    def _abrir_reportes(self):
        """Abre la ventana de reportes."""
        try:
            from views.reportes_view import ReportesView
            ventana = ReportesView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de reportes en construcción")

    def _abrir_usuarios(self):
        """Abre la ventana de administración de usuarios."""
        try:
            from views.usuarios_view import UsuariosView
            ventana = UsuariosView(self, self.usuario)
            ventana.focus_set()
        except ImportError:
            messagebox.showinfo("En desarrollo", "Módulo de usuarios en construcción")

    def _cerrar_sesion(self):
        """Cierra la sesión y vuelve a la pantalla de login."""
        from views.login_view import LoginView

        # Destruimos el menú actual.
        self.destroy()

        # Abrimos nuevamente el login.
        login = LoginView(self.parent)
        login.focus_set()

    # ==============================
    # MÉTODOS PÚBLICOS
    # ==============================

    def mostrar(self):
        """Muestra la ventana del menú."""
        self.wait_window()