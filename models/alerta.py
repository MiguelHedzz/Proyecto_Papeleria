# ==============================
# MODELO CATEGORÍA
# ==============================

class Categoria:
    """
    Esta clase representa una categoría de productos.

    Las categorías sirven para organizar los productos
    dentro del sistema de inventario.

    Ejemplo:
    - Cuadernos
    - Plumas
    - Hojas
    - Material de oficina
    """

    def __init__(self, id_categoria=None, nombre="", descripcion=""):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Categoria.

        Parámetros:
        id_categoria: Identificador único de la categoría.
        nombre: Nombre de la categoría.
        descripcion: Breve descripción de la categoría.
        """

        # Guardamos el id de la categoría.
        # Puede ser None si todavía no se guarda en la base de datos.
        self.id_categoria = id_categoria

        # Guardamos el nombre de la categoría.
        self.nombre = nombre

        # Guardamos una descripción breve de la categoría.
        self.descripcion = descripcion

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información de la categoría
        en forma de diccionario.

        Sirve para mostrar los datos de forma ordenada.
        """

        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que la categoría tenga
        al menos un nombre registrado.

        Retorna True si el nombre está completo.
        Retorna False si el nombre está vacío.
        """

        # Validamos que el nombre no esté vacío.
        if self.nombre == "":
            return False

        return True

    # ==============================
    # ACTUALIZAR NOMBRE
    # ==============================

    def actualizar_nombre(self, nuevo_nombre):
        """
        Este método permite cambiar el nombre de la categoría.

        Parámetro:
        nuevo_nombre: Nuevo nombre que tendrá la categoría.
        """

        # Verificamos que el nuevo nombre no esté vacío.
        if nuevo_nombre != "":
            self.nombre = nuevo_nombre
            return True

        return False

    # ==============================
    # ACTUALIZAR DESCRIPCIÓN
    # ==============================

    def actualizar_descripcion(self, nueva_descripcion):
        """
        Este método permite cambiar la descripción de la categoría.

        Parámetro:
        nueva_descripcion: Nueva descripción de la categoría.
        """

        # Guardamos la nueva descripción.
        self.descripcion = nueva_descripcion
        return True