# ==============================
# SERVICIO DE AUTENTICACION
# ==============================

from controllers.usuario_controller import UsuarioController


class AuthService:
    """
    Servicio de autenticación.

    Este servicio se encarga de la lógica de negocio relacionada
    con la autenticación de usuarios.

    Se encarga de:
    - Validar credenciales de inicio de sesión
    - Verificar roles de usuario
    - Manejar la sesión actual

    Este servicio utiliza UsuarioController para acceder a los datos.
    """

    def __init__(self):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto AuthService.

        Crea una instancia del controlador de usuarios para acceder a la base de datos.
        """

        # Creamos una instancia del controlador de usuarios.
        self.usuario_controller = UsuarioController()

        # Variable para almacenar el usuario actual (sesión).
        self.usuario_actual = None

    # ==============================
    # AUTENTICAR USUARIO
    # ==============================

    def autenticar(self, nombre_usuario, password):
        """
        Este método valida las credenciales de un usuario.

        Parámetros:
        nombre_usuario: Nombre de usuario ingresado en el login.
        password: Contraseña ingresada en el login.

        Retorna:
        Un objeto Usuario si las credenciales son correctas.
        None si son incorrectas o si los campos están vacíos.
        """

        # Validamos que los campos no estén vacíos.
        if not nombre_usuario or not password:
            return None

        # Llamamos al controlador para validar las credenciales.
        usuario = self.usuario_controller.validar_login(nombre_usuario, password)

        # Si la autenticación fue exitosa, guardamos el usuario en la sesión.
        if usuario:
            self.usuario_actual = usuario

        return usuario

    # ==============================
    # CERRAR SESIÓN
    # ==============================

    def cerrar_sesion(self):
        """
        Este método cierra la sesión actual del usuario.

        Elimina el usuario actual de la variable de sesión.
        """

        self.usuario_actual = None

    # ==============================
    # VERIFICAR SI ESTÁ AUTENTICADO
    # ==============================

    def esta_autenticado(self):
        """
        Este método verifica si hay un usuario con sesión activa.

        Retorna:
        True si hay un usuario autenticado.
        False si no hay sesión activa.
        """

        return self.usuario_actual is not None

    # ==============================
    # VERIFICAR ROL ADMINISTRADOR
    # ==============================

    def es_administrador(self):
        """
        Este método verifica si el usuario actual tiene rol de administrador.

        Retorna:
        True si el usuario actual es administrador.
        False si no es administrador o no hay sesión activa.
        """

        if self.usuario_actual and self.usuario_actual.rol == "Administrador":
            return True

        return False

    # ==============================
    # VERIFICAR ROL VENDEDOR
    # ==============================

    def es_vendedor(self):
        """
        Este método verifica si el usuario actual tiene rol de vendedor.

        Retorna:
        True si el usuario actual es vendedor.
        False si no es vendedor o no hay sesión activa.
        """

        if self.usuario_actual and self.usuario_actual.rol == "Vendedor":
            return True

        return False

    # ==============================
    # OBTENER USUARIO ACTUAL
    # ==============================

    def obtener_usuario_actual(self):
        """
        Este método retorna el usuario actualmente autenticado.

        Retorna:
        Objeto Usuario si hay sesión activa.
        None si no hay sesión activa.
        """

        return self.usuario_actual

    # ==============================
    # OBTENER NOMBRE DEL USUARIO ACTUAL
    # ==============================

    def obtener_nombre_usuario_actual(self):
        """
        Este método retorna el nombre del usuario actual.

        Retorna:
        String con el nombre del usuario.
        "Invitado" si no hay sesión activa.
        """

        if self.usuario_actual:
            return self.usuario_actual.nombre

        return "Invitado"

    # ==============================
    # OBTENER ROL DEL USUARIO ACTUAL
    # ==============================

    def obtener_rol_actual(self):
        """
        Este método retorna el rol del usuario actual.

        Retorna:
        String con el rol del usuario.
        "Sin rol" si no hay sesión activa.
        """

        if self.usuario_actual:
            return self.usuario_actual.rol

        return "Sin rol"