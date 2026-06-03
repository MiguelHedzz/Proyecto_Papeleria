# ==============================
# SERVICIO DE AUTENTICACION
# ==============================

class AuthService:
    """
    Servicio de autenticación.

    Este servicio se encarga de la lógica de negocio relacionada
    con la autenticación de usuarios.

    Se encarga de:
    - Validar credenciales de inicio de sesión
    - Verificar roles de usuario
    - Manejar la sesión actual
    """

    def __init__(self):
        """
        Inicializa el servicio de autenticación.
        """
        self._usuario_controller = None
        self.usuario_actual = None

    def _get_controller(self):
        """
        Obtiene o crea el controlador de usuarios.
        Esto evita importación circular.
        """
        if self._usuario_controller is None:
            from controllers.usuario_controller import UsuarioController
            self._usuario_controller = UsuarioController()
        return self._usuario_controller

    # ==============================
    # AUTENTICAR USUARIO
    # ==============================

    def autenticar(self, nombre_usuario, password):
        """
        Valida las credenciales de un usuario.

        Parámetros:
        nombre_usuario: Nombre de usuario ingresado en el login.
        password: Contraseña ingresada en el login.

        Retorna:
        Un objeto Usuario si las credenciales son correctas.
        None si son incorrectas o si los campos están vacíos.
        """
        if not nombre_usuario or not password:
            return None

        controller = self._get_controller()
        usuario = controller.validar_login(nombre_usuario, password)

        if usuario:
            self.usuario_actual = usuario

        return usuario

    # ==============================
    # CERRAR SESIÓN
    # ==============================

    def cerrar_sesion(self):
        """
        Cierra la sesión actual del usuario.
        """
        self.usuario_actual = None

    # ==============================
    # VERIFICAR SI ESTÁ AUTENTICADO
    # ==============================

    def esta_autenticado(self):
        """
        Verifica si hay un usuario con sesión activa.

        Retorna True si hay un usuario autenticado.
        """
        return self.usuario_actual is not None

    # ==============================
    # VERIFICAR ROL ADMINISTRADOR
    # ==============================

    def es_administrador(self):
        """
        Verifica si el usuario actual tiene rol de administrador.
        """
        if self.usuario_actual and self.usuario_actual.rol == "Administrador":
            return True
        return False

    # ==============================
    # VERIFICAR ROL VENDEDOR
    # ==============================

    def es_vendedor(self):
        """
        Verifica si el usuario actual tiene rol de vendedor.
        """
        if self.usuario_actual and self.usuario_actual.rol == "Vendedor":
            return True
        return False

    # ==============================
    # OBTENER USUARIO ACTUAL
    # ==============================

    def obtener_usuario_actual(self):
        """
        Retorna el usuario actualmente autenticado.
        """
        return self.usuario_actual

    # ==============================
    # OBTENER NOMBRE DEL USUARIO ACTUAL
    # ==============================

    def obtener_nombre_usuario_actual(self):
        """
        Retorna el nombre del usuario actual.
        """
        if self.usuario_actual:
            return self.usuario_actual.nombre
        return "Invitado"

    # ==============================
    # OBTENER ROL DEL USUARIO ACTUAL
    # ==============================

    def obtener_rol_actual(self):
        """
        Retorna el rol del usuario actual.
        """
        if self.usuario_actual:
            return self.usuario_actual.rol
        return "Sin rol"