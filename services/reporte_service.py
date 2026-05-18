# ==============================
# SERVICIO DE REPORTES
# ==============================

from controllers.reporte_controller import ReporteController
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from datetime import datetime
import os


class ReporteService:
    """
    Servicio de reportes.

    Este servicio se encarga de la lógica de negocio relacionada
    con la generación y exportación de reportes.

    Se encarga de:
    - Generar reportes de inventario actual
    - Generar reportes de productos con stock bajo
    - Generar reportes de ventas por período
    - Generar reportes de productos más vendidos
    - Exportar reportes a CSV y TXT
    - Guardar reportes en archivos

    Este servicio utiliza ReporteController, ProductoController y VentaController.
    """

    def __init__(self):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto ReporteService.

        Crea las instancias de los controladores necesarios.
        """

        # Creamos las instancias de los controladores.
        self.reporte_controller = ReporteController()
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()

    # ==============================
    # GENERAR REPORTE DE INVENTARIO ACTUAL
    # ==============================

    def generar_reporte_inventario(self):
        """
        Este método genera un reporte del inventario actual.

        Retorna:
        Objeto Reporte con los datos del inventario.
        None si hay error.
        """

        try:
            # Usamos el controlador para generar el reporte.
            reporte = self.reporte_controller.reporte_inventario_actual()

            return reporte

        except Exception as e:
            print(f"Error al generar reporte de inventario: {e}")
            return None

    # ==============================
    # GENERAR REPORTE DE STOCK BAJO
    # ==============================

    def generar_reporte_stock_bajo(self):
        """
        Este método genera un reporte de productos con stock bajo.

        Retorna:
        Objeto Reporte con los datos de productos con stock bajo.
        None si hay error.
        """

        try:
            # Usamos el controlador para generar el reporte.
            reporte = self.reporte_controller.reporte_stock_bajo()

            return reporte

        except Exception as e:
            print(f"Error al generar reporte de stock bajo: {e}")
            return None

    # ==============================
    # GENERAR REPORTE DE VENTAS POR PERÍODO
    # ==============================

    def generar_reporte_ventas(self, fecha_inicio=None, fecha_fin=None):
        """
        Este método genera un reporte de ventas en un período.

        Parámetros:
        fecha_inicio: Fecha de inicio (formato YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato YYYY-MM-DD)

        Retorna:
        Objeto Reporte con los datos de ventas.
        None si hay error.
        """

        try:
            # Usamos el controlador para generar el reporte.
            reporte = self.reporte_controller.reporte_ventas_por_periodo(fecha_inicio, fecha_fin)

            return reporte

        except Exception as e:
            print(f"Error al generar reporte de ventas: {e}")
            return None

    # ==============================
    # GENERAR REPORTE DE PRODUCTOS MÁS VENDIDOS
    # ==============================

    def generar_reporte_mas_vendidos(self, limite=10):
        """
        Este método genera un reporte de los productos más vendidos.

        Parámetro:
        limite: Cantidad de productos a mostrar.

        Retorna:
        Objeto Reporte con los datos de productos más vendidos.
        None si hay error.
        """

        try:
            # Usamos el controlador para generar el reporte.
            reporte = self.reporte_controller.reporte_productos_mas_vendidos(limite)

            return reporte

        except Exception as e:
            print(f"Error al generar reporte de productos más vendidos: {e}")
            return None

    # ==============================
    # GENERAR REPORTE DE MOVIMIENTOS
    # ==============================

    def generar_reporte_movimientos(self, fecha_inicio=None, fecha_fin=None):
        """
        Este método genera un reporte de movimientos (entradas y salidas).

        Parámetros:
        fecha_inicio: Fecha de inicio (formato YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato YYYY-MM-DD)

        Retorna:
        Objeto Reporte con los datos de movimientos.
        None si hay error.
        """

        try:
            # Usamos el controlador para generar el reporte.
            reporte = self.reporte_controller.reporte_movimientos(fecha_inicio, fecha_fin)

            return reporte

        except Exception as e:
            print(f"Error al generar reporte de movimientos: {e}")
            return None

    # ==============================
    # EXPORTAR REPORTE A CSV
    # ==============================

    def exportar_reporte_csv(self, reporte, nombre_archivo=None):
        """
        Este método exporta un reporte a un archivo CSV.

        Parámetros:
        reporte: Objeto Reporte a exportar.
        nombre_archivo: Nombre del archivo (opcional).

        Retorna:
        Tupla (éxito, ruta_del_archivo, mensaje)
        """

        if not reporte:
            return False, None, "No hay datos para exportar."

        try:
            # Si no se proporciona nombre, generamos uno automático.
            if not nombre_archivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"reporte_{reporte.tipo}_{timestamp}.csv"

            # Aseguramos que tenga extensión .csv.
            if not nombre_archivo.endswith('.csv'):
                nombre_archivo += '.csv'

            # Usamos el controlador para exportar.
            self.reporte_controller.exportar_reporte_csv(reporte, nombre_archivo)

            return True, nombre_archivo, f"Reporte exportado a {nombre_archivo}"

        except Exception as e:
            return False, None, f"Error al exportar reporte: {e}"

    # ==============================
    # EXPORTAR REPORTE A TEXTO
    # ==============================

    def exportar_reporte_texto(self, reporte, nombre_archivo=None):
        """
        Este método exporta un reporte a un archivo de texto.

        Parámetros:
        reporte: Objeto Reporte a exportar.
        nombre_archivo: Nombre del archivo (opcional).

        Retorna:
        Tupla (éxito, ruta_del_archivo, mensaje, contenido_texto)
        """

        if not reporte:
            return False, None, "No hay datos para exportar.", ""

        try:
            # Obtenemos el texto del reporte.
            texto_reporte = reporte.exportar_texto()

            # Si no se proporciona nombre, generamos uno automático.
            if not nombre_archivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"reporte_{reporte.tipo}_{timestamp}.txt"

            # Aseguramos que tenga extensión .txt.
            if not nombre_archivo.endswith('.txt'):
                nombre_archivo += '.txt'

            # Guardamos el archivo.
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(texto_reporte)

            return True, nombre_archivo, f"Reporte exportado a {nombre_archivo}", texto_reporte

        except Exception as e:
            return False, None, f"Error al exportar reporte: {e}", ""

    # ==============================
    # OBTENER REPORTE COMO TEXTO
    # ==============================

    def obtener_reporte_como_texto(self, reporte):
        """
        Este método convierte un reporte a texto sin guardarlo.

        Parámetro:
        reporte: Objeto Reporte a convertir.

        Retorna:
        String con el texto del reporte.
        """

        if not reporte:
            return "No hay datos para mostrar."

        return reporte.exportar_texto()

    # ==============================
    # GENERAR REPORTE COMPLETO DEL SISTEMA
    # ==============================

    def generar_reporte_completo(self):
        """
        Este método genera un reporte completo del sistema.

        Combina inventario actual, stock bajo y resumen de ventas.

        Retorna:
        Diccionario con todos los reportes.
        """

        try:
            reporte_inventario = self.generar_reporte_inventario()
            reporte_stock_bajo = self.generar_reporte_stock_bajo()
            reporte_ventas = self.generar_reporte_ventas()

            # Calculamos estadísticas adicionales.
            productos = self.producto_controller.listar_productos()
            total_productos = len(productos)

            # Contamos productos con stock bajo.
            productos_stock_bajo = 0
            for producto in productos:
                stock_actual = producto[5] if len(producto) > 5 else 0
                stock_minimo = producto[4]
                if stock_actual <= stock_minimo:
                    productos_stock_bajo += 1

            resultado = {
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_productos": total_productos,
                "productos_con_stock_bajo": productos_stock_bajo,
                "reporte_inventario": reporte_inventario,
                "reporte_stock_bajo": reporte_stock_bajo,
                "reporte_ventas": reporte_ventas
            }

            return resultado

        except Exception as e:
            print(f"Error al generar reporte completo: {e}")
            return None