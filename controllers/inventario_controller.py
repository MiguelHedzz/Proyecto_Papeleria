from models.inventario import Inventario
from utils.mensajes import mostrar_error, mostrar_info


class InventarioController:
    def __init__(self):
        self.inventario_model = Inventario()

    def obtener_productos(self):
        """Obtiene todos los productos del inventario"""
        try:
            return self.inventario_model.obtener_todos()
        except Exception as e:
            mostrar_error(f"Error al obtener productos: {e}")
            return []

    def agregar_producto(self, nombre, categoria, precio, stock):
        """Agrega un producto nuevo al inventario"""
        try:
            if not nombre or not categoria:
                mostrar_error("Todos los campos son obligatorios")
                return False

            if stock < 0:
                mostrar_error("El stock no puede ser negativo")
                return False

            producto = {
                "nombre": nombre,
                "categoria": categoria,
                "precio": precio,
                "stock": stock
            }

            self.inventario_model.insertar(producto)
            mostrar_info("Producto agregado correctamente")
            return True

        except Exception as e:
            mostrar_error(f"Error al agregar producto: {e}")
            return False

    def actualizar_stock(self, producto_id, nuevo_stock):
        """Actualiza el stock de un producto"""
        try:
            if nuevo_stock < 0:
                mostrar_error("El stock no puede ser negativo")
                return False

            self.inventario_model.actualizar_stock(producto_id, nuevo_stock)
            mostrar_info("Stock actualizado correctamente")
            return True

        except Exception as e:
            mostrar_error(f"Error al actualizar stock: {e}")
            return False

    def eliminar_producto(self, producto_id):
        """Elimina un producto del inventario"""
        try:
            self.inventario_model.eliminar(producto_id)
            mostrar_info("Producto eliminado correctamente")
            return True

        except Exception as e:
            mostrar_error(f"Error al eliminar producto: {e}")
            return False