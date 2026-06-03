# ==============================
# MODELO RESPALDO
# ==============================

class Respaldo:
    """
    Esta clase representa una copia de seguridad (respaldo) del sistema.

    El respaldo guarda el registro de la fecha y la ubicación exacta 
    donde se guardó una copia de la base de datos de la papelería.

    """

    def __init__(
        self,
        id_respaldo=None,
        fecha=None,
        ruta_archivo=""
    ):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Respaldo.

        Parámetros:
        id_respaldo: Identificador único del registro de respaldo.
        fecha: Fecha y hora en la que se generó la copia.
        ruta_archivo: Ubicación física donde se guardó el archivo .db.
        """

        # Guardamos el id del respaldo.
        # Puede ser None si todavía no se guarda en la base de datos.
        self.id_respaldo = id_respaldo

        # Guardamos la fecha del respaldo.
        self.fecha = fecha

        # Guardamos la ruta del archivo.
        self.ruta_archivo = ruta_archivo

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información del respaldo
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_respaldo": self.id_respaldo,
            "fecha": self.fecha,
            "ruta_archivo": self.ruta_archivo
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que los datos del respaldo sean correctos.

        Retorna True si los datos son válidos.
        Retorna False si falta la fecha o la ruta del archivo.
        """

        # Validamos que exista una fecha.
        if not self.fecha or self.fecha.strip() == "":
            return False

        # Validamos que exista una ruta de archivo.
        if not self.ruta_archivo or self.ruta_archivo.strip() == "":
            return False

        return True