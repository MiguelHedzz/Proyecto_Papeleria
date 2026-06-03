# ==============================
# CONTROLADOR DE REPORTES
# ==============================

import sqlite3
from datetime import datetime
from database.conexion import conectar_bd
from models.reporte import Reporte


class ReporteController:
    """
    Controlador para generar reportes del sistema.
    """

    # ==============================
    # REPORTE DE INVENTARIO ACTUAL
    # ==============================

    def reporte_inventario_actual(self):
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
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                ORDER BY p.nombre ASC
            """)

            productos = cursor.fetchall()
            conexion.close()

            reporte = Reporte(
                nombre="Reporte de Inventario Actual",
                tipo="inventario",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            for producto in productos:
                reporte.agregar_datos({
                    "id_producto": producto[0],
                    "nombre": producto[1],
                    "codigo": producto[2],
                    "precio": producto[3],
                    "stock_minimo": producto[4],
                    "stock_actual": producto[5],
                    "estado": "Stock bajo" if producto[5] <= producto[4] else "Normal"
                })

            return reporte

        except sqlite3.Error as error:
            print(f"Error al generar reporte de inventario: {error}")
            return None

    # ==============================
    # REPORTE DE PRODUCTOS CON STOCK BAJO
    # ==============================

    def reporte_stock_bajo(self):
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
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
                ORDER BY (p.stock_minimo - IFNULL(i.cantidad_actual, 0)) DESC
            """)

            productos = cursor.fetchall()
            conexion.close()

            reporte = Reporte(
                nombre="Reporte de Productos con Stock Bajo",
                tipo="alertas",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            for producto in productos:
                stock_actual = producto[5]
                stock_minimo = producto[4]
                faltante = stock_minimo - stock_actual if stock_actual < stock_minimo else 0

                reporte.agregar_datos({
                    "id_producto": producto[0],
                    "nombre": producto[1],
                    "codigo": producto[2],
                    "precio": producto[3],
                    "stock_minimo": stock_minimo,
                    "stock_actual": stock_actual,
                    "faltante": faltante
                })

            return reporte

        except sqlite3.Error as error:
            print(f"Error al generar reporte de stock bajo: {error}")
            return None

    # ==============================
    # REPORTE DE VENTAS POR PERIODO
    # ==============================

    def reporte_ventas_por_periodo(self, fecha_inicio=None, fecha_fin=None):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            if fecha_inicio and fecha_fin:
                cursor.execute("""
                    SELECT
                        v.id_venta,
                        v.fecha,
                        v.total,
                        u.nombre AS vendedor,
                        COUNT(dv.id_detalle) AS total_productos
                    FROM venta v
                    INNER JOIN usuario u ON v.id_usuario = u.id_usuario
                    INNER JOIN detalle_venta dv ON v.id_venta = dv.id_venta
                    WHERE date(v.fecha) BETWEEN ? AND ?
                    GROUP BY v.id_venta
                    ORDER BY v.fecha DESC
                """, (fecha_inicio, fecha_fin))
            else:
                cursor.execute("""
                    SELECT
                        v.id_venta,
                        v.fecha,
                        v.total,
                        u.nombre AS vendedor,
                        COUNT(dv.id_detalle) AS total_productos
                    FROM venta v
                    INNER JOIN usuario u ON v.id_usuario = u.id_usuario
                    INNER JOIN detalle_venta dv ON v.id_venta = dv.id_venta
                    GROUP BY v.id_venta
                    ORDER BY v.fecha DESC
                    LIMIT 100
                """)

            ventas = cursor.fetchall()
            conexion.close()

            total_general = sum(venta[2] for venta in ventas) if ventas else 0

            reporte = Reporte(
                nombre="Reporte de Ventas",
                tipo="ventas",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            for venta in ventas:
                reporte.agregar_datos({
                    "id_venta": venta[0],
                    "fecha": venta[1],
                    "total": venta[2],
                    "vendedor": venta[3],
                    "total_productos": venta[4]
                })

            reporte.total_general = total_general

            return reporte

        except sqlite3.Error as error:
            print(f"Error al generar reporte de ventas: {error}")
            return None

    # ==============================
    # REPORTE DE PRODUCTOS MAS VENDIDOS
    # ==============================

    def reporte_productos_mas_vendidos(self, limite=10):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.codigo,
                    SUM(dv.cantidad) AS total_vendido,
                    SUM(dv.subtotal) AS total_generado
                FROM detalle_venta dv
                INNER JOIN producto p ON dv.id_producto = p.id_producto
                GROUP BY dv.id_producto
                ORDER BY total_vendido DESC
                LIMIT ?
            """, (limite,))

            productos = cursor.fetchall()
            conexion.close()

            reporte = Reporte(
                nombre=f"Top {limite} Productos Más Vendidos",
                tipo="ventas",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            for producto in productos:
                reporte.agregar_datos({
                    "id_producto": producto[0],
                    "nombre": producto[1],
                    "codigo": producto[2],
                    "total_vendido": producto[3],
                    "total_generado": producto[4]
                })

            return reporte

        except sqlite3.Error as error:
            print(f"Error al generar reporte de productos más vendidos: {error}")
            return None

    # ==============================
    # EXPORTAR REPORTE A CSV
    # ==============================

    def exportar_reporte_csv(self, reporte, ruta_archivo):
        if reporte is None:
            return False, "No hay datos para exportar."

        try:
            reporte.exportar_csv(ruta_archivo)
            return True, f"Reporte exportado a {ruta_archivo}"
        except Exception as e:
            return False, f"Error al exportar reporte: {e}"

    # ==============================
    # EXPORTAR REPORTE A TEXTO
    # ==============================

    def exportar_reporte_texto(self, reporte):
        if reporte is None:
            return "No hay datos para mostrar."
        return reporte.exportar_texto()