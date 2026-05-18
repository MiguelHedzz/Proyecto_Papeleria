# ==============================
#  SERVICIO DE VENTAS
# ==============================

from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController
from controllers.inventario_controller import InventarioController
from controllers.alerta_controller import AlertaController
from datetime import datetime


class VentaService:
    """
    Servicio de ventas.

    Este servicio se encarga de la lógica de negocio relacionada
    con las ventas.

    Se encarga de:
    - Procesar una venta completa con múltiples productos
    - Calcular totales y subtotales
    - Verificar stock antes de vender
    - Actualizar inventario automáticamente
    - Generar alertas si hay productos con stock bajo
    - Registrar la venta y sus detalles

    Este servicio utiliza VentaController, ProductoController,
    InventarioController y AlertaController.
    """

    def __init__(self):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto VentaService.

        Crea las instancias de los controladores necesarios.
        """

        # Creamos las instancias de los controladores.
        self.venta_controller = VentaController()
        self.producto_controller = ProductoController()
        self.inventario_controller = InventarioController()
        self.alerta_controller = AlertaController()

    # ==============================
    # PROCESAR VENTA COMPLETA
    # ==============================

    def procesar_venta(self, carrito, metodo_pago, id_usuario):
        """
        Este método procesa una venta completa.

        Parámetros:
        carrito: Lista de diccionarios con productos del carrito.
                 Cada diccionario debe tener: id_producto, cantidad, precio
        metodo_pago: Método de pago (Efectivo, Tarjeta, Transferencia)
        id_usuario: Identificador del usuario que realiza la venta.

        Retorna:
        Tupla (éxito, mensaje, id_venta)
        """

        # Validamos que el carrito no esté vacío.
        if not carrito or len(carrito) == 0:
            return False, "El carrito está vacío", None

        # Validamos que haya un método de pago.
        if not metodo_pago:
            return False, "Debe seleccionar un método de pago", None

        try:
            # Variable para almacenar el total de la venta.
            total_venta = 0.0

            # Lista para guardar los detalles que se registrarán.
            detalles = []

            # ==============================
            # PRIMERO: VERIFICAR STOCK DE TODOS LOS PRODUCTOS
            # ==============================

            for item in carrito:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]

                # Verificamos stock disponible.
                stock_actual = self.inventario_controller.obtener_stock(id_producto)

                if stock_actual < cantidad:
                    # Obtenemos el nombre del producto para el mensaje.
                    producto = self.producto_controller.buscar_por_id(id_producto)
                    nombre_producto = producto.nombre if producto else f"ID {id_producto}"

                    return False, f"Stock insuficiente para '{nombre_producto}'. Disponible: {stock_actual}", None

            # ==============================
            # SEGUNDO: CALCULAR TOTAL Y PREPARAR DETALLES
            # ==============================

            for item in carrito:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]
                precio_unitario = item["precio"]
                subtotal = cantidad * precio_unitario

                total_venta += subtotal

                detalles.append({
                    "id_producto": id_producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal
                })

            # ==============================
            # TERCERO: REGISTRAR LA VENTA
            # ==============================

            # Preparamos los productos para el controlador (formato compatible).
            productos_venta = []

            for item in carrito:
                productos_venta.append({
                    "id_producto": item["id_producto"],
                    "cantidad": item["cantidad"],
                    "precio": item["precio"]
                })

            # Registramos la venta usando el controlador.
            exito = self.venta_controller.registrar_venta(productos_venta, total_venta)

            if not exito:
                return False, "Error al registrar la venta en la base de datos", None

            # Obtenemos el ID de la última venta (para mostrar al usuario).
            ultimas_ventas = self.venta_controller.obtener_ventas()
            id_venta = ultimas_ventas[0][0] if ultimas_ventas else None

            # ==============================
            # CUARTO: VERIFICAR ALERTAS DE STOCK BAJO
            # ==============================

            for item in carrito:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]

                # Obtenemos el stock actual después de la venta.
                stock_actual = self.inventario_controller.obtener_stock(id_producto)

                # Obtenemos el producto para conocer su stock mínimo.
                producto = self.producto_controller.buscar_por_id(id_producto)

                if producto and stock_actual <= producto.stock_minimo:
                    # Generamos mensaje de alerta.
                    if stock_actual <= 0:
                        mensaje = f"ATENCION: El producto '{producto.nombre}' no tiene existencia."
                    else:
                        mensaje = f"ALERTA: El producto '{producto.nombre}' tiene stock bajo. Quedan {stock_actual} unidades (Mínimo: {producto.stock_minimo})"

                    # Generamos la alerta.
                    self.alerta_controller.generar_alerta(id_producto, mensaje)

            return True, f"Venta registrada correctamente. Total: ${total_venta:.2f}", id_venta

        except Exception as e:
            return False, f"Error al procesar la venta: {e}", None

    # ==============================
    # CALCULAR TOTAL DEL CARRITO
    # ==============================

    def calcular_total_carrito(self, carrito):
        """
        Este método calcula el total de un carrito de compras.

        Parámetro:
        carrito: Lista de diccionarios con productos del carrito.

        Retorna:
        Total del carrito como float.
        """

        total = 0.0

        for item in carrito:
            cantidad = item.get("cantidad", 0)
            precio = item.get("precio", 0)
            subtotal = cantidad * precio
            total += subtotal

        return total

    # ==============================
    # OBTENER VENTAS POR USUARIO
    # ==============================

    def obtener_ventas_por_usuario(self, id_usuario):
        """
        Este método obtiene todas las ventas realizadas por un usuario.

        Parámetro:
        id_usuario: Identificador del usuario.

        Retorna:
        Lista de ventas del usuario.
        """

        try:
            todas_ventas = self.venta_controller.obtener_ventas()
            ventas_usuario = []

            for venta in todas_ventas:
                # Verificamos si la venta pertenece al usuario.
                if len(venta) > 3 and venta[3] == id_usuario:
                    ventas_usuario.append(venta)

            return ventas_usuario

        except Exception as e:
            print(f"Error al obtener ventas por usuario: {e}")
            return []

    # ==============================
    # OBTENER DETALLE DE VENTA
    # ==============================

    def obtener_detalle_venta(self, id_venta):
        """
        Este método obtiene el detalle de una venta específica.

        Parámetro:
        id_venta: Identificador de la venta.

        Retorna:
        Lista de detalles de la venta.
        """

        try:
            return self.venta_controller.obtener_detalle_venta(id_venta)

        except Exception as e:
            print(f"Error al obtener detalle de venta: {e}")
            return []

    # ==============================
    # OBTENER RESUMEN DE VENTAS DEL DÍA
    # ==============================

    def obtener_resumen_ventas_dia(self):
        """
        Este método obtiene un resumen de las ventas del día actual.

        Retorna:
        Diccionario con total de ventas, cantidad de ventas y total de productos vendidos.
        """

        try:
            todas_ventas = self.venta_controller.obtener_ventas()
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            total_ventas = 0.0
            cantidad_ventas = 0
            total_productos = 0

            for venta in todas_ventas:
                # Verificamos si la venta es de hoy.
                if len(venta) > 1 and venta[1].startswith(fecha_hoy):
                    total_ventas += venta[2]
                    cantidad_ventas += 1

                    # Obtenemos los detalles para contar productos.
                    detalles = self.venta_controller.obtener_detalle_venta(venta[0])
                    for detalle in detalles:
                        total_productos += detalle[2] if len(detalle) > 2 else 0

            return {
                "total_ventas": total_ventas,
                "cantidad_ventas": cantidad_ventas,
                "total_productos": total_productos
            }

        except Exception as e:
            print(f"Error al obtener resumen de ventas del día: {e}")
            return {
                "total_ventas": 0.0,
                "cantidad_ventas": 0,
                "total_productos": 0
            }