# Importamos el controlador de inventario.
# Este controlador se encarga de comunicarse con la base de datos.
from controllers.inventario_controller import InventarioController

# Importamos validaciones para revisar datos antes de enviarlos al controlador.
from utils.validaciones import validar_cantidad, campo_vacio


# ==============================
# SERVICIO DE INVENTARIO
# ==============================

class InventarioService:
    """
    Esta clase contiene la lógica principal del inventario.

    Un service sirve para organizar reglas del sistema antes de llegar
    directamente a la base de datos.

    Por ejemplo:
    - Validar que la cantidad sea correcta.
    - Revisar si existe stock suficiente.
    - Registrar entradas.
    - Registrar salidas.
    - Verificar si un producto quedó en stock bajo.
    """

    def __init__(self):
        """
        Al crear el servicio, también creamos una instancia
        del controlador de inventario.
        """

        self.inventario_controller = InventarioController()

    # ==============================
    # LISTAR INVENTARIO
    # ==============================

    def listar_inventario(self):
        """
        Obtiene todos los productos con su información de inventario.

        Retorna:
        Lista de productos con inventario.
        """

        return self.inventario_controller.listar_inventario()

    # ==============================
    # OBTENER PRODUCTOS
    # ==============================

    def obtener_productos(self):
        """
        Obtiene los productos disponibles junto con su inventario.

        Este método puede ser utilizado por las pantallas para llenar
        tablas o listas desplegables.
        """

        return self.inventario_controller.obtener_productos()

    # ==============================
    # CONSULTAR STOCK
    # ==============================

    def consultar_stock(self, id_producto):
        """
        Consulta la cantidad actual de un producto.

        Parámetro:
        id_producto: identificador del producto.

        Retorna:
        Cantidad actual disponible.
        """

        if id_producto is None:
            return 0

        return self.inventario_controller.obtener_stock(id_producto)

    # ==============================
    # REGISTRAR ENTRADA
    # ==============================

    def registrar_entrada(self, id_producto, cantidad, ubicacion=None):
        """
        Registra una entrada de productos al inventario.

        Una entrada significa que llegaron productos nuevos
        y se suman a la existencia actual.

        Parámetros:
        id_producto: producto seleccionado.
        cantidad: cantidad que llegó.
        ubicacion: ubicación física del producto.
        """

        # Validamos que se haya seleccionado un producto.
        if id_producto is None:
            return False, "Debe seleccionar un producto."

        # Validamos que la cantidad sea correcta.
        resultado, mensaje = validar_cantidad(cantidad)

        if not resultado:
            return False, mensaje

        # Convertimos la cantidad a entero.
        cantidad = int(cantidad)

        # En una entrada, la cantidad debe ser mayor que cero.
        if cantidad <= 0:
            return False, "La cantidad de entrada debe ser mayor que cero."

        # Si la ubicación viene vacía, se manda como cadena vacía.
        if ubicacion is None:
            ubicacion = ""

        # Registramos la entrada usando el controlador.
        return self.inventario_controller.registrar_entrada(
            id_producto,
            cantidad,
            ubicacion
        )

    # ==============================
    # REGISTRAR SALIDA
    # ==============================

    def registrar_salida(self, id_producto, cantidad):
        """
        Registra una salida de productos del inventario.

        Una salida significa que se descuentan productos,
        por ejemplo por venta o ajuste de inventario.

        Parámetros:
        id_producto: producto seleccionado.
        cantidad: cantidad que saldrá.
        """

        # Validamos que se haya seleccionado un producto.
        if id_producto is None:
            return False, "Debe seleccionar un producto."

        # Validamos que la cantidad sea correcta.
        resultado, mensaje = validar_cantidad(cantidad)

        if not resultado:
            return False, mensaje

        # Convertimos a entero.
        cantidad = int(cantidad)

        # En una salida, la cantidad debe ser mayor que cero.
        if cantidad <= 0:
            return False, "La cantidad de salida debe ser mayor que cero."

        # Consultamos stock actual.
        stock_actual = self.inventario_controller.obtener_stock(id_producto)

        # Verificamos que haya suficiente existencia.
        if cantidad > stock_actual:
            return False, "No hay suficiente existencia disponible."

        # Registramos la salida.
        resultado, mensaje = self.inventario_controller.registrar_salida(
            id_producto,
            cantidad
        )

        # Si la salida fue correcta, revisamos si quedó en stock bajo.
        if resultado:
            stock_bajo = self.inventario_controller.verificar_stock_bajo(id_producto)

            if stock_bajo:
                return True, "Salida registrada correctamente. El producto quedó en stock bajo."

        return resultado, mensaje

    # ==============================
    # ACTUALIZAR STOCK DIRECTO
    # ==============================

    def actualizar_stock(self, id_producto, nueva_cantidad):
        """
        Actualiza directamente la cantidad actual del producto.

        Este método sirve para ajustes manuales de inventario.

        Parámetros:
        id_producto: producto seleccionado.
        nueva_cantidad: nueva cantidad que tendrá el producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        resultado, mensaje = validar_cantidad(nueva_cantidad)

        if not resultado:
            return False, mensaje

        nueva_cantidad = int(nueva_cantidad)

        return self.inventario_controller.actualizar_stock(
            id_producto,
            nueva_cantidad
        )

    # ==============================
    # ACTUALIZAR UBICACIÓN
    # ==============================

    def actualizar_ubicacion(self, id_producto, nueva_ubicacion):
        """
        Actualiza la ubicación física de un producto.

        Parámetros:
        id_producto: producto seleccionado.
        nueva_ubicacion: nueva ubicación del producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if campo_vacio(nueva_ubicacion):
            return False, "La ubicación no puede estar vacía."

        return self.inventario_controller.actualizar_ubicacion(
            id_producto,
            nueva_ubicacion
        )

    # ==============================
    # VERIFICAR STOCK BAJO
    # ==============================

    def verificar_stock_bajo(self, id_producto):
        """
        Verifica si un producto tiene stock bajo.

        Retorna:
        True si está bajo.
        False si no está bajo.
        """

        if id_producto is None:
            return False

        return self.inventario_controller.verificar_stock_bajo(id_producto)


# ==============================
# PRUEBA DEL SERVICIO
# ==============================

if __name__ == "__main__":
    """
    Esta prueba sirve para revisar que el servicio no marque errores.
    """

    servicio = InventarioService()

    print("Inventario actual:")
    inventario = servicio.listar_inventario()

    for item in inventario:
        print(item)