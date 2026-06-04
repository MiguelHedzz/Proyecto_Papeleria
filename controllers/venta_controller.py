# ==============================
# CONTROLADOR DE VENTAS
# ==============================

"""
Controlador de ventas.

Este archivo se encarga de guardar y consultar:
- Ventas.
- Detalles de venta.
- Método de pago.
- Precio unitario.
"""

import sqlite3
from datetime import datetime

from database.conexion import conectar_bd


class VentaController:
    """
    Controlador para las operaciones de ventas.
    """

    # ==============================
    # REGISTRAR VENTA
    # ==============================

    def registrar_venta(self, total, id_usuario=1, metodo_pago="Efectivo", fecha=None):
        """
        Registra una venta general en la tabla venta.

        Retorna:
            (True, mensaje, id_venta)
            (False, mensaje, None)
        """

        try:
            total = float(total)
        except (TypeError, ValueError):
            return False, "El total de la venta debe ser numérico.", None

        if total <= 0:
            return False, "El total de la venta debe ser mayor que cero.", None

        if id_usuario is None:
            id_usuario = 1

        if not metodo_pago:
            metodo_pago = "Efectivo"

        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

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
            conexion.commit()

            return True, "Venta registrada correctamente.", id_venta

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al registrar venta: {error}", None

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # REGISTRAR DETALLE DE VENTA
    # ==============================

    def registrar_detalle_venta(
        self,
        id_venta,
        id_producto,
        cantidad,
        subtotal,
        precio_unitario=None
    ):
        """
        Registra un producto vendido dentro de detalle_venta.

        Retorna:
            (True, mensaje)
            (False, mensaje)
        """

        if id_venta is None:
            return False, "Debe existir una venta."

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un número entero."

        try:
            subtotal = float(subtotal)
        except (TypeError, ValueError):
            return False, "El subtotal debe ser numérico."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor que cero."

        if subtotal <= 0:
            return False, "El subtotal debe ser mayor que cero."

        if precio_unitario is None:
            precio_unitario = subtotal / cantidad

        try:
            precio_unitario = float(precio_unitario)
        except (TypeError, ValueError):
            return False, "El precio unitario debe ser numérico."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

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
                precio_unitario,
                subtotal
            ))

            conexion.commit()

            return True, "Detalle de venta registrado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al registrar detalle de venta: {error}"

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # REGISTRAR VENTA COMPLETA
    # ==============================

    def registrar_venta_completa(
        self,
        id_usuario,
        productos,
        metodo_pago="Efectivo"
    ):
        """
        Registra una venta completa.

        productos debe ser una lista de diccionarios con:
        - id_producto
        - cantidad
        - precio o precio_unitario

        Este método solo registra venta y detalle.
        El descuento de inventario se controla en VentaService.
        """

        if not productos:
            return False, "La venta debe tener al menos un producto.", None

        total = 0

        productos_normalizados = []

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio", producto.get("precio_unitario"))

            try:
                cantidad = int(cantidad)
                precio = float(precio)
            except (TypeError, ValueError):
                return False, "Cantidad o precio inválido.", None

            if id_producto is None:
                return False, "Cada producto debe tener id_producto.", None

            if cantidad <= 0:
                return False, "La cantidad debe ser mayor que cero.", None

            if precio <= 0:
                return False, "El precio debe ser mayor que cero.", None

            subtotal = cantidad * precio
            total += subtotal

            productos_normalizados.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "subtotal": subtotal
            })

        resultado, mensaje, id_venta = self.registrar_venta(
            total=total,
            id_usuario=id_usuario,
            metodo_pago=metodo_pago
        )

        if not resultado:
            return False, mensaje, None

        for producto in productos_normalizados:
            resultado_detalle, mensaje_detalle = self.registrar_detalle_venta(
                id_venta=id_venta,
                id_producto=producto["id_producto"],
                cantidad=producto["cantidad"],
                precio_unitario=producto["precio_unitario"],
                subtotal=producto["subtotal"]
            )

            if not resultado_detalle:
                return False, mensaje_detalle, id_venta

        return True, "Venta completa registrada correctamente.", id_venta

    # ==============================
    # LISTAR VENTAS
    # ==============================

    def listar_ventas(self):
        """
        Lista las ventas registradas.

        Retorna:
        id_venta, fecha, total, metodo_pago, usuario
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    v.id_venta,
                    v.fecha,
                    v.total,
                    v.metodo_pago,
                    IFNULL(u.nombre, '') AS usuario
                FROM venta v
                LEFT JOIN usuario u
                ON v.id_usuario = u.id_usuario
                ORDER BY v.fecha DESC
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error al listar ventas: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    def obtener_ventas(self):
        """
        Alias para listar ventas.
        """

        return self.listar_ventas()

    # ==============================
    # OBTENER VENTA POR ID
    # ==============================

    def obtener_venta_por_id(self, id_venta):
        """
        Obtiene una venta específica.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    v.id_venta,
                    v.fecha,
                    v.total,
                    v.metodo_pago,
                    v.id_usuario,
                    IFNULL(u.nombre, '') AS usuario
                FROM venta v
                LEFT JOIN usuario u
                ON v.id_usuario = u.id_usuario
                WHERE v.id_venta = ?
            """, (id_venta,))

            return cursor.fetchone()

        except sqlite3.Error as error:
            print(f"Error al obtener venta: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # OBTENER DETALLE DE VENTA
    # ==============================

    def obtener_detalle_venta(self, id_venta):
        """
        Obtiene los productos incluidos en una venta.

        Retorna:
        id_detalle, producto, codigo, cantidad, precio_unitario, subtotal
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    dv.id_detalle,
                    p.nombre AS producto,
                    p.codigo,
                    dv.cantidad,
                    dv.precio_unitario,
                    dv.subtotal
                FROM detalle_venta dv
                INNER JOIN producto p
                ON dv.id_producto = p.id_producto
                WHERE dv.id_venta = ?
                ORDER BY dv.id_detalle ASC
            """, (id_venta,))

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error al obtener detalle de venta: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    def obtener_detalles(self, id_venta):
        """
        Alias para detalle de venta.
        """

        return self.obtener_detalle_venta(id_venta)

    # ==============================
    # ELIMINAR VENTA
    # ==============================

    def eliminar_venta(self, id_venta):
        """
        Elimina una venta y sus detalles.

        Nota:
        En esta versión escolar no se devuelve stock automáticamente.
        """

        if id_venta is None:
            return False, "Debe seleccionar una venta."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM detalle_venta
                WHERE id_venta = ?
            """, (id_venta,))

            cursor.execute("""
                DELETE FROM venta
                WHERE id_venta = ?
            """, (id_venta,))

            conexion.commit()

            return True, "Venta eliminada correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al eliminar venta: {error}"

        finally:
            if conexion:
                conexion.close()

    def crear_venta(self, total, id_usuario=1, metodo_pago="Efectivo"):
        """
        Alias de registrar_venta.
        """

        return self.registrar_venta(total, id_usuario, metodo_pago)


if __name__ == "__main__":
    controlador = VentaController()

    print("Ventas registradas:")
    for venta in controlador.listar_ventas():
        print(tuple(venta))
