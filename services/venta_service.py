# ==============================
# SERVICIO DE VENTAS
# ==============================

"""
Este archivo contiene la lógica principal para procesar ventas.

Funcionalidades:
- Validar stock disponible antes de vender
- Registrar venta con método de pago (Efectivo/Tarjeta)
- Descontar inventario automáticamente
- Generar alertas de stock bajo
- Calcular totales
"""

import sqlite3
from datetime import datetime
from database.conexion import conectar_bd
from controllers.venta_controller import VentaController
from controllers.inventario_controller import InventarioController
from utils.validaciones import es_numero, es_entero


class VentaService:
    """
    Servicio de ventas.

    Esta clase contiene toda la lógica de negocio para procesar ventas:
    - Validación de productos y stock
    - Registro de ventas en la base de datos
    - Descuento de inventario
    - Generación automática de alertas de stock bajo
    """

    def __init__(self):
        """
        Inicializa el servicio de ventas.

        Crea instancias de los controladores necesarios:
        - VentaController: Para operaciones CRUD de ventas
        - InventarioController: Para consultar y actualizar stock
        """
        self.venta_controller = VentaController()
        self.inventario_controller = InventarioController()

    # ==============================
    # OBTENER PRECIO DE PRODUCTO
    # ==============================

    def obtener_precio_producto(self, id_producto):
        """
        Obtiene el precio de un producto desde la base de datos.

        Parámetros:
        id_producto: Identificador único del producto.

        Retorna:
        El precio del producto como float, o None si no se encuentra.
        """
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT precio FROM producto WHERE id_producto = ?", (id_producto,))
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado else None
        except sqlite3.Error:
            return None

    # ==============================
    # NORMALIZAR PRODUCTOS
    # ==============================

    def normalizar_productos(self, productos):
        """
        Convierte la lista de productos a un formato estándar.

        Parámetros:
        productos: Lista de diccionarios con datos de productos.

        Retorna:
        Lista de productos normalizados con id_producto, cantidad y precio.
        """
        productos_normalizados = []

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio")

            if precio is None:
                precio = producto.get("precio_unitario")

            if precio is None and id_producto is not None:
                precio = self.obtener_precio_producto(id_producto)

            productos_normalizados.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio": precio
            })

        return productos_normalizados

    # ==============================
    # VALIDAR PRODUCTOS
    # ==============================

    def validar_productos(self, productos):
        """
        Valida que los productos de una venta sean correctos.

        Validaciones:
        1. La venta debe tener al menos un producto
        2. Cada producto debe tener ID válido
        3. Cantidad debe ser entero positivo
        4. Precio debe ser número positivo
        5. Stock disponible debe ser suficiente

        Parámetros:
        productos: Lista de productos normalizados.

        Retorna:
        Tupla (bool, str): True y mensaje si es válido, False y error si no.
        """
        if not productos:
            return False, "La venta debe tener al menos un producto."

        cantidades_por_producto = {}

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio")

            if id_producto is None:
                return False, "Todos los productos deben tener un ID."

            if not es_entero(cantidad):
                return False, "La cantidad debe ser un número entero."

            cantidad = int(cantidad)

            if cantidad <= 0:
                return False, "La cantidad debe ser mayor que cero."

            if not es_numero(precio):
                return False, "El precio debe ser numérico."

            precio = float(precio)

            if precio <= 0:
                return False, "El precio debe ser mayor que cero."

            cantidades_por_producto[id_producto] = cantidades_por_producto.get(id_producto, 0) + cantidad

        for id_producto, cantidad_total in cantidades_por_producto.items():
            stock_actual = self.inventario_controller.obtener_stock(id_producto)

            if cantidad_total > stock_actual:
                return False, f"No hay suficiente existencia. Stock disponible: {stock_actual}"

        return True, "Productos válidos."

    # ==============================
    # CALCULAR TOTAL
    # ==============================

    def calcular_total(self, productos):
        """
        Calcula el total de la venta.

        Parámetros:
        productos: Lista de productos normalizados.

        Retorna:
        El total de la venta como float.
        """
        total = 0.0

        for producto in productos:
            cantidad = int(producto.get("cantidad"))
            precio = float(producto.get("precio"))
            total += cantidad * precio

        return total

    # ==============================
    # PROCESAR VENTA COMPLETA
    # ==============================

    def procesar_venta(self, productos, id_usuario=1, metodo_pago="Efectivo"):
        """
        Procesa una venta completa.

        Flujo completo:
        1. Normaliza los productos
        2. Valida productos y stock
        3. Calcula el total
        4. Registra la venta
        5. Registra los detalles
        6. Descuenta el inventario
        7. Genera alertas de stock bajo

        Parámetros:
        productos: Lista de productos vendidos
        id_usuario: ID del usuario que realiza la venta
        metodo_pago: Forma de pago (Efectivo o Tarjeta)

        Retorna:
        Tupla (bool, str): True y mensaje de éxito, False y mensaje de error.
        """
        if id_usuario is None:
            return False, "Debe existir un usuario para registrar la venta."

        productos = self.normalizar_productos(productos)
        resultado, mensaje = self.validar_productos(productos)

        if not resultado:
            return False, mensaje

        total = self.calcular_total(productos)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificar si la columna metodo_pago existe
            cursor.execute("PRAGMA table_info(venta)")
            columnas = [col[1] for col in cursor.fetchall()]

            if 'metodo_pago' in columnas:
                cursor.execute("""
                    INSERT INTO venta (fecha, total, id_usuario, metodo_pago)
                    VALUES (?, ?, ?, ?)
                """, (fecha, total, id_usuario, metodo_pago))
            else:
                cursor.execute("""
                    INSERT INTO venta (fecha, total, id_usuario)
                    VALUES (?, ?, ?)
                """, (fecha, total, id_usuario))

            id_venta = cursor.lastrowid

            for producto in productos:
                id_producto = producto.get("id_producto")
                cantidad = int(producto.get("cantidad"))
                precio = float(producto.get("precio"))
                subtotal = cantidad * precio

                # Registrar detalle de venta
                cursor.execute("""
                    INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal)
                    VALUES (?, ?, ?, ?)
                """, (id_venta, id_producto, cantidad, subtotal))

                # Descontar stock
                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = cantidad_actual - ?
                    WHERE id_producto = ?
                """, (cantidad, id_producto))

                # Obtener nombre del producto para la alerta
                cursor.execute("SELECT nombre FROM producto WHERE id_producto = ?", (id_producto,))
                nombre_producto = cursor.fetchone()[0]

                # Verificar stock bajo después de descontar
                cursor.execute("""
                    SELECT cantidad_actual, stock_minimo
                    FROM inventario i
                    JOIN producto p ON i.id_producto = p.id_producto
                    WHERE i.id_producto = ?
                """, (id_producto,))
                resultado_stock = cursor.fetchone()

                if resultado_stock:
                    cantidad_actual = resultado_stock[0]
                    stock_minimo = resultado_stock[1]

                    if cantidad_actual <= stock_minimo:
                        # Verificar si ya existe una alerta pendiente
                        cursor.execute("""
                            SELECT COUNT(*) FROM alerta
                            WHERE id_producto = ? AND atendida = 0
                        """, (id_producto,))
                        existe_alerta = cursor.fetchone()[0]

                        if existe_alerta == 0:
                            mensaje_alerta = f"STOCK BAJO: {nombre_producto}. Quedan {cantidad_actual} unidades (Minimo: {stock_minimo})"
                            cursor.execute("""
                                INSERT INTO alerta (id_producto, mensaje, atendida)
                                VALUES (?, ?, 0)
                            """, (id_producto, mensaje_alerta))

            conexion.commit()
            conexion.close()
            return True, f"Venta registrada correctamente. Total: ${total:.2f}"

        except sqlite3.Error as error:
            return False, f"Error al registrar venta: {error}"

    # ==============================
    # REGISTRAR VENTA (ALIAS)
    # ==============================

    def registrar_venta(self, productos, id_usuario=1, metodo_pago="Efectivo"):
        """
        Método alternativo para registrar una venta.
        Es un alias de procesar_venta() para mantener compatibilidad.
        """
        return self.procesar_venta(productos, id_usuario, metodo_pago)

    # ==============================
    # OBTENER VENTAS
    # ==============================

    def obtener_ventas(self):
        """Obtiene todas las ventas registradas."""
        return self.venta_controller.obtener_ventas()

    def listar_ventas(self):
        """Método alternativo para listar ventas."""
        return self.obtener_ventas()

    # ==============================
    # OBTENER DETALLE DE VENTA
    # ==============================

    def obtener_detalle_venta(self, venta_id):
        """Obtiene los productos incluidos en una venta específica."""
        if venta_id is None:
            return []
        return self.venta_controller.obtener_detalle_venta(venta_id)

    # ==============================
    # ELIMINAR VENTA
    # ==============================

    def eliminar_venta(self, venta_id):
        """
        Elimina una venta y sus detalles.

        Nota: En esta versión escolar, eliminar una venta NO devuelve el stock.
        """
        if venta_id is None:
            return False, "Debe seleccionar una venta."

        resultado = self.venta_controller.eliminar_venta(venta_id)

        if isinstance(resultado, tuple):
            return resultado

        if resultado:
            return True, "Venta eliminada correctamente."

        return False, "No se pudo eliminar la venta."


if __name__ == "__main__":
    servicio = VentaService()
    print("Ventas registradas:")
    for venta in servicio.obtener_ventas():
        print(venta)