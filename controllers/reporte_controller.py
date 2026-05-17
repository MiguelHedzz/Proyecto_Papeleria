# ==============================
# CONTROLADOR DE REPORTES
# ==============================

import sqlite3
from datetime import datetime
from database.conexion import conectar_bd
from models.reporte import Reporte


class ReporteController:
    """
    Esta clase contiene las funciones principales para generar reportes.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario quiere un reporte de inventario, este controller lo genera.
    - Si el usuario quiere un reporte de ventas, este controller lo genera.
    - Si el usuario quiere exportar un reporte, este controller lo exporta.
    """

    # ==============================
    # REPORTE DE INVENTARIO ACTUAL
    # ==============================

    def reporte_inventario_actual(self):
        """
        Esta funcion genera un reporte con todos los productos
        y su stock actual.
        """

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

            # Creamos el reporte
            reporte = Reporte(
                nombre="Reporte de Inventario Actual",
                tipo="inventario",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Agregamos los datos
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
            print("Error al generar reporte de inventario:", error)
            return None

    # ==============================
    # REPORTE DE PRODUCTOS CON STOCK BAJO
    # ==============================

    def reporte_stock_bajo(self):
        """
        Esta funcion genera un reporte solo con los productos
        que tienen stock por debajo del minimo.
        """

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

            # Creamos el reporte
            reporte = Reporte(
                nombre="Reporte de Productos con Stock Bajo",
                tipo="alertas",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Agregamos los datos
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
            print("Error al generar reporte de stock bajo:", error)
            return None

    # ==============================
    # REPORTE DE VENTAS POR PERIODO
    # ==============================

    def reporte_ventas_por_periodo(self, fecha_inicio=None, fecha_fin=None):
        """
        Esta funcion genera un reporte de ventas en un periodo de tiempo.

        Parametros:
        fecha_inicio: Fecha de inicio (formato YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato YYYY-MM-DD)
        """

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

            # Calculamos el total general
            total_general = sum(venta[2] for venta in ventas) if ventas else 0

            # Creamos el reporte
            reporte = Reporte(
                nombre="Reporte de Ventas",
                tipo="ventas",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Agregamos los datos
            for venta in ventas:
                reporte.agregar_datos({
                    "id_venta": venta[0],
                    "fecha": venta[1],
                    "total": venta[2],
                    "vendedor": venta[3],
                    "total_productos": venta[4]
                })

            # Agregamos el total general como metadato
            reporte.total_general = total_general

            return reporte

        except sqlite3.Error as error:
            print("Error al generar reporte de ventas:", error)
            return None

    # ==============================
    # REPORTE DE PRODUCTOS MAS VENDIDOS
    # ==============================

    def reporte_productos_mas_vendidos(self, limite=10):
        """
        Esta funcion genera un reporte de los productos mas vendidos.

        Parametro:
        limite: Cantidad de productos a mostrar (default 10).
        """

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

            # Creamos el reporte
            reporte = Reporte(
                nombre=f"Top {limite} Productos Mas Vendidos",
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
            print("Error al generar reporte de productos mas vendidos:", error)
            return None

    # ==============================
    # REPORTE DE MOVIMIENTOS
    # ==============================

    def reporte_movimientos(self, fecha_inicio=None, fecha_fin=None):
        """
        Esta funcion genera un reporte de movimientos (entradas y salidas).

        Nota:
        Las entradas no estan registradas en las tablas actuales,
        por lo que este reporte muestra principalmente ventas (salidas).
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Obtenemos las salidas (ventas con detalle)
            if fecha_inicio and fecha_fin:
                cursor.execute("""
                    SELECT
                        'SALIDA' AS tipo,
                        v.fecha,
                        p.nombre AS producto,
                        dv.cantidad,
                        dv.subtotal,
                        'Venta #' || v.id_venta AS referencia
                    FROM detalle_venta dv
                    INNER JOIN venta v ON dv.id_venta = v.id_venta
                    INNER JOIN producto p ON dv.id_producto = p.id_producto
                    WHERE date(v.fecha) BETWEEN ? AND ?
                    ORDER BY v.fecha DESC
                """, (fecha_inicio, fecha_fin))
            else:
                cursor.execute("""
                    SELECT
                        'SALIDA' AS tipo,
                        v.fecha,
                        p.nombre AS producto,
                        dv.cantidad,
                        dv.subtotal,
                        'Venta #' || v.id_venta AS referencia
                    FROM detalle_venta dv
                    INNER JOIN venta v ON dv.id_venta = v.id_venta
                    INNER JOIN producto p ON dv.id_producto = p.id_producto
                    ORDER BY v.fecha DESC
                    LIMIT 100
                """)

            movimientos = cursor.fetchall()
            conexion.close()

            # Creamos el reporte
            reporte = Reporte(
                nombre="Reporte de Movimientos",
                tipo="movimientos",
                fecha_generacion=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Agregamos los datos
            for movimiento in movimientos:
                reporte.agregar_datos({
                    "tipo": movimiento[0],
                    "fecha": movimiento[1],
                    "producto": movimiento[2],
                    "cantidad": movimiento[3],
                    "subtotal": movimiento[4],
                    "referencia": movimiento[5]
                })

            return reporte

        except sqlite3.Error as error:
            print("Error al generar reporte de movimientos:", error)
            return None

    # ==============================
    # EXPORTAR REPORTE A CSV
    # ==============================

    def exportar_reporte_csv(self, reporte, ruta_archivo):
        """
        Esta funcion exporta un reporte a un archivo CSV.

        Parametros:
        reporte: Objeto Reporte a exportar.
        ruta_archivo: Ruta donde se guardara el archivo.
        """

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
        """
        Esta funcion convierte un reporte a formato texto.

        Parametro:
        reporte: Objeto Reporte a convertir.

        Retorna el texto del reporte.
        """

        if reporte is None:
            return "No hay datos para mostrar."

        return reporte.exportar_texto()