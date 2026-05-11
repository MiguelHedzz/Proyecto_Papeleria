# ==============================
# MODELO DETALLE VENTA
# ==============================

class DetalleVenta:
    """
    Esta clase representa el detalle de una venta.

    Cada detalle corresponde a un producto especifico vendido
    dentro de una venta. Guarda la cantidad, el precio unitario
    y el subtotal de ese producto.

    Ejemplo:
    - Producto: Cuaderno, Cantidad: 2, Precio: $25, Subtotal: $50
    - Producto: Pluma, Cantidad: 3, Precio: $5, Subtotal: $15
    """

    def __init__(
        self,
        id_detalle=None,
        id_venta=None,
        id_producto=None,
        cantidad=0,
        precio_unitario=0.0,
        subtotal=0.0,
        nombre_producto=""
    ):
        """
        Este metodo se ejecuta automaticamente cuando se crea un objeto DetalleVenta.

        Parametros:
        id_detalle: Identificador unico del detalle.
        id_venta: Identificador de la venta a la que pertenece.
        id_producto: Identificador del producto vendido.
        cantidad: Cantidad vendida del producto.
        precio_unitario: Precio del producto al momento de la venta.
        subtotal: Cantidad multiplicada por precio unitario.
        nombre_producto: Nombre del producto (para mostrar sin hacer otra consulta).
        """

        # Guardamos el id del detalle.
        # Puede ser None si todavia no se guarda en la base de datos.
        self.id_detalle = id_detalle

        # Guardamos el id de la venta a la que pertenece este detalle.
        self.id_venta = id_venta

        # Guardamos el id del producto que se vendio.
        self.id_producto = id_producto

        # Guardamos la cantidad vendida del producto.
        self.cantidad = cantidad

        # Guardamos el precio unitario del producto al momento de la venta.
        self.precio_unitario = precio_unitario

        # Guardamos el subtotal (cantidad * precio_unitario).
        self.subtotal = subtotal

        # Guardamos el nombre del producto para mostrar facilmente.
        self.nombre_producto = nombre_producto

    # ==============================
    # MOSTRAR INFORMACION
    # ==============================

    def mostrar_informacion(self):
        """
        Este metodo devuelve la informacion del detalle de venta
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_detalle": self.id_detalle,
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
            "nombre_producto": self.nombre_producto
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este metodo revisa que los datos importantes del detalle
        esten completos y sean validos.

        Retorna True si los datos son correctos.
        Retorna False si hay algun error.
        """

        # Validamos que exista una venta relacionada.
        if self.id_venta is None:
            return False

        # Validamos que exista un producto relacionado.
        if self.id_producto is None:
            return False

        # Validamos que la cantidad sea mayor que cero.
        if self.cantidad <= 0:
            return False

        # Validamos que el precio unitario sea mayor que cero.
        if self.precio_unitario <= 0:
            return False

        return True

    # ==============================
    # CALCULAR SUBTOTAL
    # ==============================

    def calcular_subtotal(self):
        """
        Este metodo calcula el subtotal del detalle
        multiplicando cantidad por precio unitario.

        Retorna el subtotal calculado.
        """

        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal

    # ==============================
    # ACTUALIZAR CANTIDAD
    # ==============================

    def actualizar_cantidad(self, nueva_cantidad):
        """
        Este metodo permite cambiar la cantidad vendida
        y recalcula automaticamente el subtotal.

        Parametro:
        nueva_cantidad: Nueva cantidad del producto en la venta.
        """

        if nueva_cantidad > 0:
            self.cantidad = nueva_cantidad
            self.calcular_subtotal()
            return True

        return False

    # ==============================
    # ACTUALIZAR PRECIO UNITARIO
    # ==============================

    def actualizar_precio_unitario(self, nuevo_precio):
        """
        Este metodo permite cambiar el precio unitario
        y recalcula automaticamente el subtotal.

        Parametro:
        nuevo_precio: Nuevo precio unitario del producto.
        """

        if nuevo_precio > 0:
            self.precio_unitario = nuevo_precio
            self.calcular_subtotal()
            return True

        return False

    # ==============================
    # OBTENER DESCRIPCION CORTA
    # ==============================

    def obtener_descripcion(self):
        """
        Este metodo devuelve una descripcion corta del detalle.

        Util para mostrar en tickets o listados.
        """

        producto = self.nombre_producto if self.nombre_producto else f"Producto #{self.id_producto}"
        return f"{producto} x{self.cantidad} = ${self.subtotal:.2f}"