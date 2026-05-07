# ==============================
# MODELO INVENTARIO
# ==============================

class Inventario:
    """
    Esta clase representa el inventario de un producto.

    El inventario guarda la cantidad actual disponible
    de cada producto dentro de la papelería.

    Ejemplo:
    Producto: Cuaderno profesional
    Cantidad actual: 50
    Ubicación: Estante A1
    """

    def __init__(
        self,
        id_inventario=None,
        id_producto=None,
        cantidad_actual=0,
        ubicacion=""
    ):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Inventario.

        Parámetros:
        id_inventario: Identificador único del registro de inventario.
        id_producto: Identificador del producto relacionado.
        cantidad_actual: Cantidad disponible del producto.
        ubicacion: Lugar donde se encuentra físicamente el producto.
        """

        # Guardamos el id del inventario.
        # Puede ser None si todavía no se guarda en la base de datos.
        self.id_inventario = id_inventario

        # Guardamos el id del producto al que pertenece este inventario.
        self.id_producto = id_producto

        # Guardamos la cantidad actual disponible del producto.
        self.cantidad_actual = cantidad_actual

        # Guardamos la ubicación física del producto.
        self.ubicacion = ubicacion

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información del inventario
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_inventario": self.id_inventario,
            "id_producto": self.id_producto,
            "cantidad_actual": self.cantidad_actual,
            "ubicacion": self.ubicacion
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que los datos del inventario sean correctos.

        Retorna True si los datos son válidos.
        Retorna False si falta el producto o la cantidad es negativa.
        """

        # Validamos que exista un producto relacionado.
        if self.id_producto is None:
            return False

        # Validamos que la cantidad actual no sea negativa.
        if self.cantidad_actual < 0:
            return False

        return True

    # ==============================
    # AUMENTAR EXISTENCIA
    # ==============================

    def aumentar_existencia(self, cantidad):
        """
        Este método aumenta la cantidad actual del producto.

        Se usa cuando se registra una entrada de productos al inventario.

        Parámetro:
        cantidad: Número de piezas que se van a agregar.
        """

        # Verificamos que la cantidad a agregar sea mayor que cero.
        if cantidad > 0:
            self.cantidad_actual += cantidad
            return True

        return False

    # ==============================
    # DISMINUIR EXISTENCIA
    # ==============================

    def disminuir_existencia(self, cantidad):
        """
        Este método disminuye la cantidad actual del producto.

        Se usa cuando se realiza una venta.

        Parámetro:
        cantidad: Número de piezas que se van a descontar.
        """

        # Validamos que la cantidad sea mayor que cero.
        if cantidad <= 0:
            return False

        # Validamos que haya suficiente existencia para descontar.
        if cantidad > self.cantidad_actual:
            return False

        # Descontamos la cantidad vendida del inventario.
        self.cantidad_actual -= cantidad
        return True

    # ==============================
    # ACTUALIZAR UBICACIÓN
    # ==============================

    def actualizar_ubicacion(self, nueva_ubicacion):
        """
        Este método permite cambiar la ubicación física del producto.

        Parámetro:
        nueva_ubicacion: Nuevo lugar donde estará ubicado el producto.
        """

        # Guardamos la nueva ubicación.
        self.ubicacion = nueva_ubicacion
        return True

    # ==============================
    # VERIFICAR EXISTENCIA DISPONIBLE
    # ==============================

    def tiene_existencia(self, cantidad_solicitada):
        """
        Este método verifica si hay suficiente producto disponible.

        Parámetro:
        cantidad_solicitada: Cantidad que se quiere vender o retirar.

        Retorna True si hay suficiente existencia.
        Retorna False si no alcanza el inventario.
        """

        if self.cantidad_actual >= cantidad_solicitada:
            return True

        return False