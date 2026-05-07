# ==============================
# MODELO PROVEEDOR
# ==============================

class Proveedor:
    """
    Esta clase representa a un proveedor del sistema.

    Un proveedor es la persona o empresa que suministra productos
    a la papelería.

    Ejemplo:
    - Proveedor de cuadernos
    - Proveedor de plumas
    - Proveedor de hojas
    - Proveedor de material de oficina
    """

    def __init__(
        self,
        id_proveedor=None,
        nombre="",
        telefono="",
        correo="",
        direccion=""
    ):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Proveedor.

        Parámetros:
        id_proveedor: Identificador único del proveedor.
        nombre: Nombre del proveedor.
        telefono: Número telefónico del proveedor.
        correo: Correo electrónico del proveedor.
        direccion: Dirección física del proveedor.
        """

        # Guardamos el id del proveedor.
        # Puede ser None si todavía no se guarda en la base de datos.
        self.id_proveedor = id_proveedor

        # Guardamos el nombre del proveedor.
        self.nombre = nombre

        # Guardamos el teléfono del proveedor.
        self.telefono = telefono

        # Guardamos el correo electrónico del proveedor.
        self.correo = correo

        # Guardamos la dirección del proveedor.
        self.direccion = direccion

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información del proveedor
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_proveedor": self.id_proveedor,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo,
            "direccion": self.direccion
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que el proveedor tenga
        al menos el nombre registrado.

        Retorna True si el proveedor tiene nombre.
        Retorna False si el nombre está vacío.
        """

        # Validamos que el nombre no esté vacío.
        if self.nombre == "":
            return False

        return True

    # ==============================
    # ACTUALIZAR TELÉFONO
    # ==============================

    def actualizar_telefono(self, nuevo_telefono):
        """
        Este método permite cambiar el teléfono del proveedor.

        Parámetro:
        nuevo_telefono: Nuevo número telefónico del proveedor.
        """

        # Guardamos el nuevo teléfono.
        self.telefono = nuevo_telefono
        return True

    # ==============================
    # ACTUALIZAR CORREO
    # ==============================

    def actualizar_correo(self, nuevo_correo):
        """
        Este método permite cambiar el correo del proveedor.

        Parámetro:
        nuevo_correo: Nuevo correo electrónico del proveedor.
        """

        # Guardamos el nuevo correo.
        self.correo = nuevo_correo
        return True

    # ==============================
    # ACTUALIZAR DIRECCIÓN
    # ==============================

    def actualizar_direccion(self, nueva_direccion):
        """
        Este método permite cambiar la dirección del proveedor.

        Parámetro:
        nueva_direccion: Nueva dirección del proveedor.
        """

        # Guardamos la nueva dirección.
        self.direccion = nueva_direccion
        return True