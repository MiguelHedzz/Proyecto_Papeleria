# ==============================
# SERVICIO DE REPORTES
# ==============================

"""
Servicio para consultar información de reportes.

Este archivo no dibuja pantallas.
Solo consulta y organiza datos para que layout_view.py los pueda mostrar.
"""

import sqlite3

from database.conexion import conectar_bd
from controllers.producto_controller import ProductoController
from controllers.inventario_controller import InventarioController
from controllers.venta_controller import VentaController


class ReporteService:
    """
    Servicio de reportes del sistema.
    """

    def __init__(self):
        self.producto_controller = ProductoController()
        self.inventario_controller = InventarioController()
        self.venta_controller = VentaController()

    # ==============================
    # REPORTES PRINCIPALES
    # ==============================

    def reporte_productos(self):
        """
        Retorna todos los productos registrados.
        """

        return self.producto_controller.listar_productos()

    def reporte_inventario(self):
        """
        Retorna el inventario actual.
        """

        return self.inventario_controller.listar_inventario()

    def reporte_ventas(self):
        """
        Retorna las ventas registradas.
        """

        if hasattr(self.venta_controller, "obtener_ventas"):
            return self.venta_controller.obtener_ventas()

        if hasattr(self.venta_controller, "listar_ventas"):
            return self.venta_controller.listar_ventas()

        return []

    def reporte_alertas(self):
        """
        Retorna las alertas registradas.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    a.id_alerta,
                    a.id_producto,
                    p.nombre,
                    a.mensaje,
                    a.atendida
                FROM alerta a
                INNER JOIN producto p
                ON a.id_producto = p.id_producto
                ORDER BY a.id_alerta DESC
            """)

            alertas = cursor.fetchall()
            conexion.close()

            return alertas

        except sqlite3.Error:
            return []

    def reporte_stock_bajo(self):
        """
        Retorna productos con cantidad actual menor o igual al stock mínimo.
        """

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
                LEFT JOIN inventario i
                ON p.id_producto = i.id_producto
                WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
                ORDER BY p.nombre ASC
            """)

            productos = cursor.fetchall()
            conexion.close()

            return productos

        except sqlite3.Error:
            return []

    # ==============================
    # TOTALES
    # ==============================

    def total_productos(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("SELECT COUNT(*) FROM producto")
            resultado = cursor.fetchone()

            conexion.close()

            return resultado[0] if resultado else 0

        except sqlite3.Error:
            return 0

    def total_ventas(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("SELECT COUNT(*) FROM venta")
            resultado = cursor.fetchone()

            conexion.close()

            return resultado[0] if resultado else 0

        except sqlite3.Error:
            return 0

    def total_ingresos(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("SELECT IFNULL(SUM(total), 0) FROM venta")
            resultado = cursor.fetchone()

            conexion.close()

            return resultado[0] if resultado else 0

        except sqlite3.Error:
            return 0

    def total_alertas_pendientes(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM alerta
                WHERE atendida = 0
            """)

            resultado = cursor.fetchone()
            conexion.close()

            return resultado[0] if resultado else 0

        except sqlite3.Error:
            return 0

    # ==============================
    # RESUMEN GENERAL
    # ==============================

    def resumen_general(self):
        """
        Retorna un resumen general del sistema.
        """

        return {
            "total_productos": self.total_productos(),
            "total_ventas": self.total_ventas(),
            "total_ingresos": self.total_ingresos(),
            "alertas_pendientes": self.total_alertas_pendientes(),
            "productos_stock_bajo": len(self.reporte_stock_bajo())
        }

    def obtener_reporte(self, tipo_reporte):
        """
        Retorna un reporte según el tipo solicitado.
        """

        if tipo_reporte == "productos":
            return self.reporte_productos()

        if tipo_reporte == "inventario":
            return self.reporte_inventario()

        if tipo_reporte == "ventas":
            return self.reporte_ventas()

        if tipo_reporte == "alertas":
            return self.reporte_alertas()

        if tipo_reporte == "stock_bajo":
            return self.reporte_stock_bajo()

        if tipo_reporte == "resumen":
            return self.resumen_general()

        return []


if __name__ == "__main__":
    servicio = ReporteService()

    print("Resumen general:")
    resumen = servicio.resumen_general()

    for clave, valor in resumen.items():
        print(f"{clave}: {valor}")
