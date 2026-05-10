from models.venta import Venta
from models.detalle_venta import DetalleVentaModel
from models.inventario import InventarioModel


class VentaController:

    def __init__(self):
        self.venta_model = Venta()
        self.detalle_model = DetalleVentaModel()
        self.inventario_model = InventarioModel()

    def registrar_venta(self, productos, total):

        try:

            if len(productos) == 0:
                print("No hay productos en la venta")
                return False

            venta_id = self.venta_model.crear_venta(total)

            for producto in productos:

                id_producto = producto['id_producto']
                cantidad = producto['cantidad']
                precio = producto['precio']

                producto_actual = self.inventario_model.buscar_por_id(
                    id_producto
                )

                if not producto_actual:
                    print("Producto no encontrado")
                    return False

                if producto_actual['stock'] < cantidad:
                    print("Stock insuficiente")
                    return False

                self.detalle_model.insertar_detalle(
                    venta_id,
                    id_producto,
                    cantidad,
                    precio
                )

                nuevo_stock = (
                    producto_actual['stock'] - cantidad
                )

                self.inventario_model.actualizar_stock(
                    id_producto,
                    nuevo_stock
                )

            print("Venta registrada correctamente")
            return True

        except Exception as e:
            print(f"Error al registrar venta: {e}")
            return False

    def obtener_ventas(self):

        try:
            return self.venta_model.obtener_todas()

        except Exception as e:
            print(f"Error al obtener ventas: {e}")
            return []

    def obtener_detalle_venta(self, venta_id):

        try:
            return self.detalle_model.obtener_por_venta(
                venta_id
            )

        except Exception as e:
            print(f"Error al obtener detalle: {e}")
            return []