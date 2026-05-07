# ==============================
# MODELO USUARIO
# ==============================

class Usuario:
    """
    Esta clase representa a un usuario del sistema.

    Un usuario puede ser Administrador o Vendedor.
    El administrador tendrá más permisos dentro del sistema,
    mientras que el vendedor tendrá acceso principalmente a ventas
    y consultas de productos.
    """

    def __init__(self, id_usuario=None, nombre="", usuario="", password="", rol=""):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Usuario.

        Parámetros:
        id_usuario: Identificador único del usuario.
        nombre: Nombre completo del usuario.
        usuario: Nombre de usuario para iniciar sesión.
        password: Contraseña del usuario.
        rol: Tipo de usuario, por ejemplo Administrador o Vendedor.
        """

        # Guardamos el id del usuario.
        # Puede ser None cuando el usuario todavía no ha sido guardado en la base de datos.
        self.id_usuario = id_usuario

        # Guardamos el nombre completo del usuario.
        self.nombre = nombre

        # Guardamos el nombre de usuario que usará para iniciar sesión.
        self.usuario = usuario

        # Guardamos la contraseña del usuario.
        self.password = password

        # Guardamos el rol del usuario dentro del sistema.
        self.rol = rol

    # ==============================
    # MÉTODO PARA MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información básica del usuario.

        No muestra la contraseña por seguridad.
        """

        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "rol": self.rol
        }

    # ==============================
    # MÉTODO PARA VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que los datos principales del usuario
        no estén vacíos.

        Retorna True si los datos están completos.
        Retorna False si falta algún dato.
        """

        if self.nombre == "":
            return False

        if self.usuario == "":
            return False

        if self.password == "":
            return False

        if self.rol == "":
            return False

        return True

    # ==============================
    # MÉTODO PARA CAMBIAR CONTRASEÑA
    # ==============================

    def cambiar_password(self, nueva_password):
        """
        Este método permite cambiar la contraseña del usuario.

        Parámetro:
        nueva_password: Nueva contraseña que tendrá el usuario.
        """

        if nueva_password != "":
            self.password = nueva_password
            return True

        return False

    # ==============================
    # MÉTODO PARA CAMBIAR ROL
    # ==============================

    def cambiar_rol(self, nuevo_rol):
        """
        Este método permite cambiar el rol del usuario.

        Parámetro:
        nuevo_rol: Nuevo rol del usuario.
        """

        if nuevo_rol != "":
            self.rol = nuevo_rol
            return True

        return False