# ==============================
# CONTROLADOR DE INVENTARIO
# ==============================

"""
Controlador de inventario.

Maneja:
- Listado de inventario.
- Entradas.
- Salidas.
- Actualizaciones de stock.
- Ubicacion.
- Historial de movimientos.
- Alertas automaticas por stock bajo.
"""

import sqlite3
from database.conexion import conectar_bd


class InventarioController:
    """
    Controlador principal de inventario.
    """

    def listar_inventario(self):
        """
        Lista productos con cantidad actual y ubicacion.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.codigo,
                    p.precio,
                    p.stock_minimo,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion,
                    IFNULL(c.nombre, '') AS categoria,
                    IFNULL(pr.nombre, '') AS proveedor
                FROM producto p
                LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                LEFT JOIN categoria c
                    ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedor pr
                    ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.nombre ASC
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error al listar inventario: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    def obtener_productos(self):
        """
        Alias para listar inventario.
        """

        return self.listar_inventario()

    def obtener_stock(self, id_producto):
        """
        Obtiene cantidad actual de un producto.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT IFNULL(cantidad_actual, 0) AS cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()
            return int(resultado["cantidad_actual"]) if resultado else 0

        except sqlite3.Error as error:
            print(f"Error al obtener stock: {error}")
            return 0

        finally:
            if conexion:
                conexion.close()

    def registrar_entrada(self, id_producto, cantidad, ubicacion=None, id_usuario=None, motivo="Entrada manual"):
        """
        Registra una entrada al inventario y guarda movimiento.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un numero entero."

        if cantidad <= 0:
            return False, "La cantidad de entrada debe ser mayor que cero."

        ubicacion = "" if ubicacion is None else str(ubicacion).strip()
        motivo = "Entrada manual" if not motivo else str(motivo).strip()
        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_inventario, cantidad_actual, IFNULL(ubicacion, '') AS ubicacion
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                nueva_cantidad = int(inventario["cantidad_actual"]) + cantidad
                ubicacion_final = ubicacion if ubicacion else inventario["ubicacion"]

                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?, ubicacion = ?
                    WHERE id_producto = ?
                """, (nueva_cantidad, ubicacion_final, id_producto))
            else:
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, ?)
                """, (id_producto, cantidad, ubicacion))

            self.registrar_movimiento_cursor(
                cursor,
                id_producto=id_producto,
                tipo_movimiento="ENTRADA",
                cantidad=cantidad,
                id_usuario=id_usuario,
                motivo=motivo
            )

            # Si habia alerta pendiente y ahora subio el stock, no la cerramos automaticamente
            # para que el administrador decida si fue atendida.

            conexion.commit()
            return True, "Entrada registrada correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al registrar entrada: {error}"

        finally:
            if conexion:
                conexion.close()

    def registrar_salida(self, id_producto, cantidad, id_usuario=None, motivo="Salida manual"):
        """
        Registra una salida de inventario, guarda movimiento y genera alerta si aplica.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un numero entero."

        if cantidad <= 0:
            return False, "La cantidad de salida debe ser mayor que cero."

        motivo = "Salida manual" if not motivo else str(motivo).strip()
        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_inventario, cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if not inventario:
                return False, "El producto no tiene inventario registrado."

            cantidad_actual = int(inventario["cantidad_actual"])

            if cantidad > cantidad_actual:
                return False, "No hay suficiente existencia disponible."

            nueva_cantidad = cantidad_actual - cantidad

            cursor.execute("""
                UPDATE inventario
                SET cantidad_actual = ?
                WHERE id_producto = ?
            """, (nueva_cantidad, id_producto))

            self.registrar_movimiento_cursor(
                cursor,
                id_producto=id_producto,
                tipo_movimiento="SALIDA",
                cantidad=cantidad,
                id_usuario=id_usuario,
                motivo=motivo
            )

            self.generar_alerta_si_stock_bajo_cursor(cursor, id_producto)

            conexion.commit()
            return True, "Salida registrada correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al registrar salida: {error}"

        finally:
            if conexion:
                conexion.close()

    def actualizar_stock(self, id_producto, nueva_cantidad, id_usuario=None, motivo="Ajuste manual de stock"):
        """
        Reemplaza la cantidad actual y registra movimiento por diferencia.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            nueva_cantidad = int(nueva_cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser un numero entero."

        if nueva_cantidad < 0:
            return False, "La cantidad no puede ser negativa."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()
            cantidad_anterior = int(inventario["cantidad_actual"]) if inventario else 0

            if inventario:
                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?
                    WHERE id_producto = ?
                """, (nueva_cantidad, id_producto))
            else:
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, '')
                """, (id_producto, nueva_cantidad))

            diferencia = nueva_cantidad - cantidad_anterior

            if diferencia != 0:
                tipo = "ENTRADA" if diferencia > 0 else "SALIDA"
                self.registrar_movimiento_cursor(
                    cursor,
                    id_producto=id_producto,
                    tipo_movimiento=tipo,
                    cantidad=abs(diferencia),
                    id_usuario=id_usuario,
                    motivo=motivo
                )

            self.generar_alerta_si_stock_bajo_cursor(cursor, id_producto)

            conexion.commit()
            return True, "Stock actualizado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al actualizar stock: {error}"

        finally:
            if conexion:
                conexion.close()

    def actualizar_ubicacion(self, id_producto, nueva_ubicacion):
        """
        Actualiza ubicacion del producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        nueva_ubicacion = "" if nueva_ubicacion is None else str(nueva_ubicacion).strip()
        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_inventario
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                cursor.execute("""
                    UPDATE inventario
                    SET ubicacion = ?
                    WHERE id_producto = ?
                """, (nueva_ubicacion, id_producto))
            else:
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, 0, ?)
                """, (id_producto, nueva_ubicacion))

            conexion.commit()
            return True, "Ubicacion actualizada correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al actualizar ubicacion: {error}"

        finally:
            if conexion:
                conexion.close()

    def registrar_movimiento_cursor(self, cursor, id_producto, tipo_movimiento, cantidad, id_usuario=None, motivo=""):
        """
        Inserta movimiento usando un cursor existente.
        """

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
            tipo_movimiento,
            cantidad,
            id_usuario,
            motivo
        ))

    def generar_alerta_si_stock_bajo_cursor(self, cursor, id_producto):
        """
        Genera alerta pendiente si el stock queda bajo.
        """

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

        datos = cursor.fetchone()

        if not datos:
            return

        cantidad_actual = int(datos["cantidad_actual"])
        stock_minimo = int(datos["stock_minimo"])

        if cantidad_actual > stock_minimo:
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
            f"Stock bajo: {datos['nombre']}. "
            f"Quedan {cantidad_actual} unidades. "
            f"Minimo permitido: {stock_minimo}."
        )

        cursor.execute("""
            INSERT INTO alerta (
                id_producto,
                mensaje,
                fecha,
                atendida
            )
            VALUES (?, ?, CURRENT_TIMESTAMP, 0)
        """, (id_producto, mensaje))

    def verificar_stock_bajo(self, id_producto):
        """
        Retorna True si el producto esta en stock bajo.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    p.stock_minimo,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual
                FROM producto p
                LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                WHERE p.id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()

            if not resultado:
                return False

            return int(resultado["cantidad_actual"]) <= int(resultado["stock_minimo"])

        except sqlite3.Error as error:
            print(f"Error al verificar stock bajo: {error}")
            return False

        finally:
            if conexion:
                conexion.close()


inventario_controller = InventarioController()


if __name__ == "__main__":
    controlador = InventarioController()
    for item in controlador.listar_inventario():
        print(tuple(item))
