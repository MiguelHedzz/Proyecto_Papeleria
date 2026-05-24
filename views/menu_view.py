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
        from views.ventana_productos import VentanaProductos
        ventana = VentanaProductos(self)
        ventana.focus_set()

    def _abrir_categorias(self):
        """Abre la ventana de gestión de categorías."""
        from views.ventana_categorias import VentanaCategorias
        ventana = VentanaCategorias(self)
        ventana.focus_set()

    def _abrir_proveedores(self):
        """Abre la ventana de gestión de proveedores."""
        from views.ventana_proveedores import VentanaProveedores
        ventana = VentanaProveedores(self)
        ventana.focus_set()

    def _abrir_inventario(self):
        """Abre la ventana de control de inventario."""
        from views.ventana_inventario import VentanaInventario
        ventana = VentanaInventario(self)
        ventana.focus_set()

    def _abrir_ventas(self):
        """Abre la ventana de registro de ventas."""
        from views.ventana_ventas import VentanaVentas
        ventana = VentanaVentas(self, self.usuario)
        ventana.focus_set()

    def _abrir_alertas(self):
        """Abre la ventana de alertas de stock bajo."""
        from views.ventana_alertas import VentanaAlertas
        ventana = VentanaAlertas(self)
        ventana.focus_set()

    def _abrir_reportes(self):
        """Abre la ventana de reportes."""
        from views.ventana_reportes import VentanaReportes
        ventana = VentanaReportes(self)
        ventana.focus_set()

    def _abrir_usuarios(self):
        """Abre la ventana de administración de usuarios."""
        from views.ventana_usuarios import VentanaUsuarios
        ventana = VentanaUsuarios(self)
        ventana.focus_set()

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
