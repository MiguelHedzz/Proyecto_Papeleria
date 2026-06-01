# ==============================
# Vista de LOGIN (mejora de robustez)
# ==============================

import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService


class LoginView(tk.Toplevel):
    """
    Esta clase representa la pantalla de inicio de sesión del sistema.

    Permite al usuario ingresar sus credenciales (usuario y contraseña)
    y valida que sean correctas antes de abrir el menú principal.

    Si las credenciales son correctas, abre la ventana del menú principal
    según el rol del usuario (Administrador o Vendedor).
    """

    def __init__(self, parent=None):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto LoginView.

        Parámetros:
        parent: Widget padre (opcional). Si no se proporciona, se crea una raíz.
        """

        # Si no hay parent, creamos una ventana raíz.
        if parent is None:
            self.root = tk.Tk()
            super().__init__(self.root)
            self.root.title("Dunder Mifflin - Inicio de Sesión")
            self.parent_window = self.root
        else:
            super().__init__(parent)
            self.title("Dunder Mifflin - Inicio de Sesión")
            self.parent_window = parent

        # Configuramos la ventana.
        self.geometry("450x450")
        self.resizable(False, False)
        self.configure(bg="#e8ecef")

        # Centramos la ventana en la pantalla.
        self._centrar_ventana()

        # Creamos el servicio de autenticación.
        self.auth_service = AuthService()

        # Construimos la interfaz.
        self._construir_interfaz()

        # Hacemos la ventana modal.
        self.transient(self.parent_window)
        self.grab_set()

    # ==============================
    # MÉTODOS PRIVADOS
    # ==============================

    def _centrar_ventana(self):
        """
        Este método centra la ventana en la pantalla.

        Calcula la posición X e Y basándose en el ancho y alto de la pantalla.
        """

        # Actualizamos la ventana para obtener sus dimensiones reales.
        self.update_idletasks()

        # Obtenemos el ancho y alto de la pantalla.
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Obtenemos el ancho y alto de la ventana.
        ancho_ventana = self.winfo_width()
        alto_ventana = self.winfo_height()

        # Calculamos la posición centrada.
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Establecemos la posición.
        self.geometry(f"+{x}+{y}")

    def _construir_interfaz(self):
        """
        Este método construye todos los elementos visuales de la ventana.
        """

        # ==============================
        # FRAME PRINCIPAL
        # ==============================

        # Frame principal (card blanca centrada).
        frame_principal = tk.Frame(self, bg="white", highlightbackground="#d5d8dc", highlightthickness=1)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # ==============================
        # ENCABEZADO
        # ==============================

        # Logo / Título principal.
        lbl_titulo = tk.Label(
            frame_principal,
            text="🏪 Dunder Mifflin",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        lbl_titulo.pack(pady=(40, 5))

        # Subtítulo.
        lbl_subtitulo = tk.Label(
            frame_principal,
            text="Sistema de Inventario",
            font=("Segoe UI", 12),
            bg="white",
            fg="#7f8c8d"
        )
        lbl_subtitulo.pack(pady=(0, 30))

        # ==============================
        # SEPARADOR
        # ==============================

        separador = ttk.Separator(frame_principal, orient='horizontal')
        separador.pack(fill=tk.X, padx=20, pady=10)

        # ==============================
        # CAMPOS DEL FORMULARIO
        # ==============================

        # Frame para los campos (ayuda con el espaciado).
        frame_campos = tk.Frame(frame_principal, bg="white")
        frame_campos.pack(pady=20, padx=40, fill=tk.X)

        # Campo: Usuario
        lbl_usuario = tk.Label(
            frame_campos,
            text="Usuario",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w"
        )
        lbl_usuario.pack(fill=tk.X, pady=(0, 5))

        self.entry_usuario = tk.Entry(
            frame_campos,
            font=("Segoe UI", 11),
            bg="white",
            fg="#2c3e50",
            highlightbackground="#d5d8dc",
            highlightthickness=1,
            relief=tk.FLAT
        )
        self.entry_usuario.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Campo: Contraseña
        lbl_password = tk.Label(
            frame_campos,
            text="Contraseña",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w"
        )
        lbl_password.pack(fill=tk.X, pady=(0, 5))

        self.entry_password = tk.Entry(
            frame_campos,
            font=("Segoe UI", 11),
            bg="white",
            fg="#2c3e50",
            highlightbackground="#d5d8dc",
            highlightthickness=1,
            relief=tk.FLAT,
            show="•"
        )
        self.entry_password.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # ==============================
        # BOTÓN DE INICIO DE SESIÓN
        # ==============================

        btn_login = tk.Button(
            frame_campos,
            text="Iniciar Sesión",
            font=("Segoe UI", 11, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            command=self._iniciar_sesion
        )
        btn_login.pack(fill=tk.X, pady=(10, 20), ipady=10)

        # ==============================
        # AYUDA (CREDENCIALES DE PRUEBA)
        # ==============================

        lbl_ayuda = tk.Label(
            frame_principal,
            text="Usuario de prueba: admin | Contraseña: admin123",
            font=("Segoe UI", 9),
            bg="white",
            fg="#95a5a6"
        )
        lbl_ayuda.pack(pady=(0, 20))

        # ==============================
        # EVENTOS DEL TECLADO
        # ==============================

        # Permitir presionar Enter para iniciar sesión.
        self.entry_usuario.bind("<Return>", lambda event: self._iniciar_sesion())
        self.entry_password.bind("<Return>", lambda event: self._iniciar_sesion())

        # Foco inicial en el campo de usuario.
        self.entry_usuario.focus_set()

    def _iniciar_sesion(self):
        """
        Este método se ejecuta cuando el usuario hace clic en "Iniciar Sesión"
        o presiona la tecla Enter.

        Obtiene las credenciales, las valida y, si son correctas,
        abre el menú principal correspondiente al rol.
        """

        # Obtenemos las credenciales.
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        # Validamos que los campos no estén vacíos.
        if not usuario or not password:
            messagebox.showerror(
                "Campos vacíos",
                "Por favor, ingrese usuario y contraseña.",
                parent=self
            )
            return

        # Intentamos autenticar.
        usuario_autenticado = self.auth_service.autenticar(usuario, password)

        # Verificamos si la autenticación fue exitosa.
        if usuario_autenticado:
            # Guardamos la ventana padre antes de destruir
            parent_ventana = self.master if self.master else self.parent_window
            
            # Cerramos la ventana de login.
            self.destroy()

            # Importamos MenuView aquí para evitar importación circular.
            from views.menu_view import MenuView

            # Abrimos el menú principal con el usuario autenticado.
            menu = MenuView(parent_ventana, usuario_autenticado)
            menu.focus_set()

        else:
            # Credenciales incorrectas.
            messagebox.showerror(
                "Error de autenticación",
                "Usuario o contraseña incorrectos. Intente nuevamente.",
                parent=self
            )
            # Limpiamos el campo de contraseña y mantenemos el foco.
            self.entry_password.delete(0, tk.END)
            self.entry_usuario.focus_set()

    # ==============================
    # MÉTODOS PÚBLICOS
    # ==============================

    def mostrar(self):
        """
        Este método muestra la ventana de login.

        Si la ventana tiene una raíz propia (sin parent), ejecuta el mainloop.
        """

        self.wait_window()