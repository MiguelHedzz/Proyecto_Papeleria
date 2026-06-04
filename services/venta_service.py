# ==============================
# SERVICIO DE VENTAS
# ==============================

"""
Servicio de ventas.

Este archivo contiene la lógica completa para:
- Validar stock.
- Registrar venta con método de pago.
- Guardar precio_unitario en detalle_venta.
- Descontar inventario.
- Registrar movimiento de inventario.
- Generar alerta de stock bajo.
"""

import sqlite3
from datetime import datetime

from database.conexion import conectar_bd
from controllers.venta_controller import VentaController


class VentaService:
    """
    Servicio para procesar ventas.
    """

    def __init__(self):
        self.venta_controller = VentaController()

    # ==============================
    # NORMALIZAR PRODUCTOS
    # ==============================

    def normalizar_productos(self, productos):
        """
        Convierte los productos recibidos al formato estándar.

        Cada producto debe quedar con:
        - id_producto
        - cantidad
        - precio
        """

        productos_normalizados = []

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio", producto.get("precio_unitario"))

            try:
                cantidad = int(cantidad)
            except (TypeError, ValueError):
                raise ValueError("La cantidad debe ser un número entero.")

            if precio is None:
                precio = self.obtener_precio_producto(id_producto)

            try:
                precio = float(precio)
            except (TypeError, ValueError):
                raise ValueError("El precio debe ser numérico.")

            productos_normalizados.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio": precio
            })

        return productos_normalizados

    # ==============================
    # OBTENER PRECIO
    # ==============================

    def obtener_precio_producto(self, id_producto):
        """
        Obtiene el precio de un producto.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT precio
                FROM producto
                WHERE id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()

            if resultado:
                return float(resultado["precio"])

            return None

        except sqlite3.Error:
            return None

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # VALIDAR PRODUCTOS
    # ==============================

    def validar_productos(self, productos):
        """
        Valida que haya productos y stock suficiente.
        """

        if not productos:
            return False, "La venta debe tener al menos un producto."

        conexion = None

        try:
            productos = self.normalizar_productos(productos)

            conexion = conectar_bd()
            cursor = conexion.cursor()

            for producto in productos:
                id_producto = producto["id_producto"]
                cantidad = producto["cantidad"]
                precio = producto["precio"]

                if id_producto is None:
                    return False, "Cada producto debe tener id_producto."

                if cantidad <= 0:
                    return False, "La cantidad debe ser mayor que cero."

                if precio <= 0:
                    return False, "El precio debe ser mayor que cero."

                cursor.execute("""
                    SELECT
                        p.nombre,
                        IFNULL(i.cantidad_actual, 0) AS cantidad_actual
                    FROM producto p
                    LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                    WHERE p.id_producto = ?
                """, (id_producto,))

                resultado = cursor.fetchone()

                if not resultado:
                    return False, "Uno de los productos no existe."

                if cantidad > int(resultado["cantidad_actual"]):
                    return False, (
                        f"No hay stock suficiente para {resultado['nombre']}. "
                        f"Stock actual: {resultado['cantidad_actual']}."
                    )

            return True, "Productos válidos."

        except ValueError as error:
            return False, str(error)

        except sqlite3.Error as error:
            return False, f"Error al validar productos: {error}"

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # CALCULAR TOTAL
    # ==============================

    def calcular_total(self, productos):
        """
        Calcula el total de la venta.
        """

        productos = self.normalizar_productos(productos)
        total = 0

        for producto in productos:
            total += producto["cantidad"] * producto["precio"]

        return total

    # ==============================
    # GENERAR ALERTA
    # ==============================

    def generar_alerta_stock_bajo(self, cursor, id_producto, nombre_producto, cantidad_actual, stock_minimo):
        """
        Genera una alerta si el producto está en stock bajo y no tiene alerta pendiente.
        """

        if int(cantidad_actual) > int(stock_minimo):
            return

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM alerta
            WHERE id_producto = ? AND atendida = 0
        """, (id_producto,))

        existe = cursor.fetchone()["total"]

        if existe > 0:
            return

        mensaje = (
            f"Stock bajo: {nombre_producto}. "
            f"Quedan {cantidad_actual} unidades. "
            f"Mínimo permitido: {stock_minimo}."
        )

        cursor.execute("""
            INSERT INTO alerta (
                id_producto,
                mensaje,
                fecha,
                atendida
            )
            VALUES (?, ?, CURRENT_TIMESTAMP, 0)
        """, (
            id_producto,
            mensaje
        ))

    # ==============================
    # PROCESAR VENTA
    # ==============================

    def procesar_venta(self, productos, id_usuario=1, metodo_pago="Efectivo"):
        """
        Registra una venta completa.

        Retorna:
            (True, mensaje)
            (False, mensaje)
        """

        resultado, mensaje = self.validar_productos(productos)

        if not resultado:
            return False, mensaje

        try:
            productos = self.normalizar_productos(productos)
            total = self.calcular_total(productos)
        except ValueError as error:
            return False, str(error)

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO venta (
                    fecha,
                    total,
                    metodo_pago,
                    id_usuario
                )
                VALUES (?, ?, ?, ?)
            """, (
                fecha,
                total,
                metodo_pago,
                id_usuario
            ))

            id_venta = cursor.lastrowid

            for producto in productos:
                id_producto = producto["id_producto"]
                cantidad = producto["cantidad"]
                precio = producto["precio"]
                subtotal = cantidad * precio

                # Registrar detalle con precio unitario.
                cursor.execute("""
                    INSERT INTO detalle_venta (
                        id_venta,
                        id_producto,
                        cantidad,
                        precio_unitario,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    id_venta,
                    id_producto,
                    cantidad,
                    precio,
                    subtotal
                ))

                # Descontar inventario.
                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = cantidad_actual - ?
                    WHERE id_producto = ?
                """, (
                    cantidad,
                    id_producto
                ))

                # Registrar movimiento de inventario.
                cursor.execute("""
                    INSERT INTO movimiento_inventario (
                        id_producto,
                        tipo_movimiento,
                        cantidad,
                        fecha,
                        id_usuario,
                        motivo
                    )
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
                """, (
                    id_producto,
                    "SALIDA",
                    cantidad,
                    id_usuario,
                    f"Venta #{id_venta}"
                ))

                # Revisar stock bajo.
                cursor.execute("""
                    SELECT
                        p.nombre,
                        p.stock_minimo,
                        IFNULL(i.cantidad_actual, 0) AS cantidad_actual
                    FROM producto p
                    LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                    WHERE p.id_producto = ?
                """, (id_producto,))

                datos_stock = cursor.fetchone()

                if datos_stock:
                    self.generar_alerta_stock_bajo(
                        cursor=cursor,
                        id_producto=id_producto,
                        nombre_producto=datos_stock["nombre"],
                        cantidad_actual=datos_stock["cantidad_actual"],
                        stock_minimo=datos_stock["stock_minimo"]
                    )

            conexion.commit()

            return True, f"Venta registrada correctamente. Total: ${total:.2f}"

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al procesar venta: {error}"

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # ALIAS Y CONSULTAS
    # ==============================

    def registrar_venta(self, productos, id_usuario=1, metodo_pago="Efectivo"):
        """
        Alias para procesar venta.
        """

        return self.procesar_venta(productos, id_usuario, metodo_pago)

    def obtener_ventas(self):
        """
        Obtiene ventas registradas.
        """

        return self.venta_controller.obtener_ventas()

    def listar_ventas(self):
        """
        Lista ventas registradas.
        """

        return self.obtener_ventas()

    def obtener_detalle_venta(self, id_venta):
        """
        Obtiene detalle de una venta.
        """

        return self.venta_controller.obtener_detalle_venta(id_venta)

    def eliminar_venta(self, id_venta):
        """
        Elimina una venta.
        """

        return self.venta_controller.eliminar_venta(id_venta)


if __name__ == "__main__":
    servicio = VentaService()

    print("Ventas registradas:")
    for venta in servicio.obtener_ventas():
        print(tuple(venta))
