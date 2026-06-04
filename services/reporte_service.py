# ==============================
# SERVICIO DE REPORTES
# ==============================

"""
Servicio para consultar reportes del sistema.

Incluye:
- Productos.
- Inventario.
- Stock bajo.
- Ventas.
- Movimientos de inventario.
- Productos mas vendidos.
- Resumen general.
"""

import sqlite3
from database.conexion import conectar_bd


class ReporteService:
    """
    Servicio de reportes.
    """

    def reporte_productos(self):
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
                    p.id_categoria,
                    p.id_proveedor,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion,
                    IFNULL(c.nombre, '') AS categoria,
                    IFNULL(pr.nombre, '') AS proveedor,
                    IFNULL(p.activo, 1) AS activo
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                LEFT JOIN categoria c ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedor pr ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.nombre ASC
            """)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error en reporte_productos: {error}")
            return []
        finally:
            if conexion:
                conexion.close()

    def reporte_inventario(self):
        return self.reporte_productos()

    def reporte_stock_bajo(self):
        conexion = None
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.codigo,
                    p.stock_minimo,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
                ORDER BY p.nombre ASC
            """)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error en reporte_stock_bajo: {error}")
            return []
        finally:
            if conexion:
                conexion.close()

    def reporte_ventas(self):
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
                LEFT JOIN usuario u ON v.id_usuario = u.id_usuario
                ORDER BY v.fecha DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error en reporte_ventas: {error}")
            return []
        finally:
            if conexion:
                conexion.close()

    def reporte_movimientos(self):
        conexion = None
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT
                    m.id_movimiento,
                    p.nombre AS producto,
                    p.codigo,
                    m.tipo_movimiento,
                    m.cantidad,
                    m.fecha,
                    IFNULL(u.nombre, '') AS usuario,
                    IFNULL(m.motivo, '') AS motivo
                FROM movimiento_inventario m
                INNER JOIN producto p ON m.id_producto = p.id_producto
                LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
                ORDER BY m.fecha DESC, m.id_movimiento DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error en reporte_movimientos: {error}")
            return []
        finally:
            if conexion:
                conexion.close()

    def reporte_productos_mas_vendidos(self):
        """
        Productos agrupados por cantidad vendida.
        """

        conexion = None
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.codigo,
                    p.nombre,
                    SUM(dv.cantidad) AS cantidad_vendida,
                    SUM(dv.subtotal) AS total_vendido
                FROM detalle_venta dv
                INNER JOIN producto p ON dv.id_producto = p.id_producto
                GROUP BY p.id_producto, p.codigo, p.nombre
                ORDER BY cantidad_vendida DESC, total_vendido DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error en reporte_productos_mas_vendidos: {error}")
            return []
        finally:
            if conexion:
                conexion.close()

    def total_productos(self):
        return self.obtener_total("SELECT COUNT(*) AS total FROM producto")

    def total_ventas(self):
        return self.obtener_total("SELECT COUNT(*) AS total FROM venta")

    def total_ingresos(self):
        return self.obtener_total("SELECT IFNULL(SUM(total), 0) AS total FROM venta")

    def total_stock_bajo(self):
        conexion = None
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
            """)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
        except sqlite3.Error:
            return 0
        finally:
            if conexion:
                conexion.close()

    def obtener_total(self, consulta):
        conexion = None
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
        except sqlite3.Error:
            return 0
        finally:
            if conexion:
                conexion.close()

    def resumen_general(self):
        return {
            "total_productos": self.total_productos(),
            "total_ventas": self.total_ventas(),
            "total_ingresos": self.total_ingresos(),
            "productos_stock_bajo": self.total_stock_bajo()
        }

    def obtener_reporte(self, tipo_reporte):
        if tipo_reporte == "productos":
            return self.reporte_productos()
        if tipo_reporte == "inventario":
            return self.reporte_inventario()
        if tipo_reporte == "stock_bajo":
            return self.reporte_stock_bajo()
        if tipo_reporte == "ventas":
            return self.reporte_ventas()
        if tipo_reporte == "movimientos":
            return self.reporte_movimientos()
        if tipo_reporte == "mas_vendidos":
            return self.reporte_productos_mas_vendidos()
        if tipo_reporte == "resumen":
            return self.resumen_general()
        return []


if __name__ == "__main__":
    servicio = ReporteService()
    print(servicio.resumen_general())
