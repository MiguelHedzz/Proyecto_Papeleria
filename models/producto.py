# ==============================
# MODELO PRODUCTO
# ==============================

class Producto:
    """
    Esta clase representa un producto dentro del sistema de inventario.

    Un producto puede ser un lápiz, cuaderno, pluma, hoja, marcador
    u otro artículo de papelería.

    Esta clase guarda los datos principales del producto.
    """

    def __init__(
        self,
        id_producto=None,
        nombre="",
        codigo="",
        precio=0.0,
        stock_minimo=0,
        id_categoria=None,
        id_proveedor=None
    ):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Producto.

        Parámetros:
        id_producto: Identificador único del producto.
        nombre: Nombre del producto.
        codigo: Código único del producto.
        precio: Precio de venta del producto.
        stock_minimo: Cantidad mínima permitida antes de generar alerta.
        id_categoria: Identificador de la categoría del producto.
        id_proveedor: Identificador del proveedor del producto.
        """

        # Guardamos el id del producto.
        # Puede ser None cuando el producto aún no se guarda en la base de datos.
        self.id_producto = id_producto

        # Guardamos el nombre del producto.
        self.nombre = nombre

        # Guardamos el código único del producto.
        # Este código sirve para buscarlo o evitar registros duplicados.
        self.codigo = codigo

        # Guardamos el precio del producto.
        self.precio = precio

        # Guardamos el stock mínimo.
        # Cuando la existencia llegue a esta cantidad, se puede generar una alerta.
        self.stock_minimo = stock_minimo

        # Guardamos el id de la categoría a la que pertenece el producto.
        self.id_categoria = id_categoria

        # Guardamos el id del proveedor que suministra el producto.
        self.id_proveedor = id_proveedor

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información del producto en forma de diccionario.

        Sirve para mostrar los datos del producto de manera ordenada.
        """

        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "precio": self.precio,
            "stock_minimo": self.stock_minimo,
            "id_categoria": self.id_categoria,
            "id_proveedor": self.id_proveedor
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que los datos importantes del producto estén completos.

        Retorna True si los datos son correctos.
        Retorna False si falta algún dato o si hay valores incorrectos.
        """

        # Validamos que el nombre no esté vacío.
        if self.nombre == "":
            return False

        # Validamos que el código no esté vacío.
        if self.codigo == "":
            return False

        # Validamos que el precio sea mayor que cero.
        if self.precio <= 0:
            return False

        # Validamos que el stock mínimo no sea negativo.
        if self.stock_minimo < 0:
            return False

        return True

    # ==============================
    # ACTUALIZAR PRECIO
    # ==============================

    def actualizar_precio(self, nuevo_precio):
        """
        Este método permite actualizar el precio del producto.

        Parámetro:
        nuevo_precio: Nuevo precio que tendrá el producto.
        """

        # Verificamos que el nuevo precio sea mayor que cero.
        if nuevo_precio > 0:
            self.precio = nuevo_precio
            return True

        return False

    # ==============================
    # ACTUALIZAR STOCK MÍNIMO
    # ==============================

    def actualizar_stock_minimo(self, nuevo_stock_minimo):
        """
        Este método permite cambiar el stock mínimo del producto.

        Parámetro:
        nuevo_stock_minimo: Nueva cantidad mínima permitida.
        """

        # Validamos que el stock mínimo no sea negativo.
        if nuevo_stock_minimo >= 0:
            self.stock_minimo = nuevo_stock_minimo
            return True

        return False

    # ==============================
    # VERIFICAR STOCK BAJO
    # ==============================

    def verificar_stock_bajo(self, cantidad_actual):
        """
        Este método verifica si la cantidad actual del producto
        es menor o igual al stock mínimo.

        Parámetro:
        cantidad_actual: Existencia actual del producto en inventario.

        Retorna True si el producto tiene stock bajo.
        Retorna False si todavía tiene suficiente existencia.
        """

        if cantidad_actual <= self.stock_minimo:
            return True

        return False