# ==============================
# SERVICIO DE INVENTARIO
# ==============================

from controllers.inventario_controller import InventarioController
from controllers.producto_controller import ProductoController
from controllers.alerta_controller import AlertaController


class InventarioService:
    """
    Servicio de inventario.

    Este servicio se encarga de la lógica de negocio relacionada
    con el control de inventario.

    Se encarga de:
    - Registrar entradas de productos (compras)
    - Registrar salidas de productos (ventas)
    - Verificar stock disponible
    - Generar alertas automáticas cuando el stock es bajo
    - Calcular estadísticas de inventario

    Este servicio utiliza InventarioController, ProductoController y AlertaController.
    """

    def __init__(self):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto InventarioService.

        Crea las instancias de los controladores necesarios.
        """

        # Creamos las instancias de los controladores.
        self.inventario_controller = InventarioController()
        self.producto_controller = ProductoController()
        self.alerta_controller = AlertaController()

    # ==============================
    # REGISTRAR ENTRADA DE PRODUCTO
    # ==============================

    def registrar_entrada(self, id_producto, cantidad, ubicacion=""):
        """
        Este método registra una entrada de productos al inventario.

        Se usa cuando se recibe una compra de productos.

        Parámetros:
        id_producto: Identificador del producto.
        cantidad: Cantidad que ingresa al inventario (debe ser positiva).
        ubicacion: Ubicación física del producto (opcional).

        Retorna:
        Tupla (éxito, mensaje)
        """

        # Validamos que la cantidad sea positiva.
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero."

        try:
            # Obtenemos el producto para verificar que existe.
            producto = self.producto_controller.buscar_por_id(id_producto)

            if not producto:
                return False, "El producto no existe."

            # Obtenemos el stock actual.
            stock_actual = self.inventario_controller.obtener_stock(id_producto)

            # Calculamos el nuevo stock.
            nuevo_stock = stock_actual + cantidad

            # Actualizamos el inventario.
            self.inventario_controller.actualizar_stock(id_producto, nuevo_stock)

            # Si se proporcionó ubicación, la actualizamos.
            if ubicacion:
                self.inventario_controller.actualizar_ubicacion(id_producto, ubicacion)

            # Verificamos si después de la entrada hay que generar alertas.
            self._verificar_y_generar_alerta(id_producto, nuevo_stock, producto.stock_minimo)

            return True, f"Entrada registrada correctamente. Nuevo stock: {nuevo_stock}"

        except Exception as e:
            return False, f"Error al registrar entrada: {e}"

    # ==============================
    # REGISTRAR SALIDA DE PRODUCTO
    # ==============================

    def registrar_salida(self, id_producto, cantidad):
        """
        Este método registra una salida de productos del inventario.

        Se usa cuando se realiza una venta.

        Parámetros:
        id_producto: Identificador del producto.
        cantidad: Cantidad que sale del inventario (debe ser positiva).

        Retorna:
        Tupla (éxito, mensaje)
        """

        # Validamos que la cantidad sea positiva.
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero."

        try:
            # Obtenemos el producto para verificar que existe.
            producto = self.producto_controller.buscar_por_id(id_producto)

            if not producto:
                return False, "El producto no existe."

            # Obtenemos el stock actual.
            stock_actual = self.inventario_controller.obtener_stock(id_producto)

            # Verificamos que haya suficiente stock.
            if stock_actual < cantidad:
                return False, f"Stock insuficiente. Solo hay {stock_actual} unidades."

            # Calculamos el nuevo stock.
            nuevo_stock = stock_actual - cantidad

            # Actualizamos el inventario.
            self.inventario_controller.actualizar_stock(id_producto, nuevo_stock)

            # Verificamos si después de la salida hay que generar alertas.
            self._verificar_y_generar_alerta(id_producto, nuevo_stock, producto.stock_minimo)

            return True, f"Salida registrada correctamente. Nuevo stock: {nuevo_stock}"

        except Exception as e:
            return False, f"Error al registrar salida: {e}"

    # ==============================
    # VERIFICAR STOCK DISPONIBLE
    # ==============================

    def verificar_stock(self, id_producto, cantidad_solicitada):
        """
        Este método verifica si hay suficiente stock disponible.

        Parámetros:
        id_producto: Identificador del producto.
        cantidad_solicitada: Cantidad que se quiere vender o retirar.

        Retorna:
        True si hay suficiente stock.
        False si no hay suficiente stock o el producto no existe.
        """

        try:
            stock_actual = self.inventario_controller.obtener_stock(id_producto)
            return stock_actual >= cantidad_solicitada

        except Exception:
            return False

    # ==============================
    # OBTENER STOCK ACTUAL
    # ==============================

    def obtener_stock_actual(self, id_producto):
        """
        Este método obtiene la cantidad actual de un producto.

        Parámetro:
        id_producto: Identificador del producto.

        Retorna:
        Cantidad actual del producto.
        0 si el producto no existe o hay error.
        """

        try:
            return self.inventario_controller.obtener_stock(id_producto)

        except Exception:
            return 0

    # ==============================
    # VERIFICAR Y GENERAR ALERTA (PRIVADO)
    # ==============================

    def _verificar_y_generar_alerta(self, id_producto, stock_actual, stock_minimo):
        """
        Este método privado verifica si el stock está bajo y genera una alerta.

        Parámetros:
        id_producto: Identificador del producto.
        stock_actual: Cantidad actual disponible.
        stock_minimo: Cantidad mínima permitida.
        """

        # Si el stock actual es menor o igual al mínimo, generamos alerta.
        if stock_actual <= stock_minimo:
            # Obtenemos el nombre del producto.
            producto = self.producto_controller.buscar_por_id(id_producto)

            if producto:
                # Construimos el mensaje de alerta.
                if stock_actual <= 0:
                    mensaje = f"ATENCION: El producto '{producto.nombre}' no tiene existencia."
                else:
                    mensaje = f"ALERTA: El producto '{producto.nombre}' tiene stock bajo. Quedan {stock_actual} unidades (Minimo: {stock_minimo})"

                # Generamos la alerta.
                self.alerta_controller.generar_alerta(id_producto, mensaje)

    # ==============================
    # OBTENER PRODUCTOS CON STOCK BAJO
    # ==============================

    def obtener_productos_con_stock_bajo(self):
        """
        Este método obtiene todos los productos que tienen stock bajo.

        Retorna:
        Lista de productos con stock actual menor o igual al stock mínimo.
        """

        try:
            # Obtenemos todos los productos.
            productos = self.producto_controller.listar_productos()

            productos_stock_bajo = []

            for producto in productos:
                # Extraemos los datos de la tupla.
                id_producto = producto[0]
                nombre = producto[1]
                stock_minimo = producto[4]
                stock_actual = producto[5] if len(producto) > 5 else 0

                if stock_actual <= stock_minimo:
                    productos_stock_bajo.append({
                        "id_producto": id_producto,
                        "nombre": nombre,
                        "stock_actual": stock_actual,
                        "stock_minimo": stock_minimo,
                        "faltante": stock_minimo - stock_actual if stock_actual < stock_minimo else 0
                    })

            return productos_stock_bajo

        except Exception as e:
            print(f"Error al obtener productos con stock bajo: {e}")
            return []

    # ==============================
    # OBTENER VALOR TOTAL DEL INVENTARIO
    # ==============================

    def obtener_valor_total_inventario(self):
        """
        Este método calcula el valor total del inventario.

        Suma (precio * stock_actual) de todos los productos.

        Retorna:
        Valor total del inventario como float.
        """

        try:
            productos = self.producto_controller.listar_productos()
            valor_total = 0.0

            for producto in productos:
                # Extraemos los datos de la tupla.
                precio = producto[3]
                stock_actual = producto[5] if len(producto) > 5 else 0

                valor_total += precio * stock_actual

            return valor_total

        except Exception as e:
            print(f"Error al calcular valor total del inventario: {e}")
            return 0.0