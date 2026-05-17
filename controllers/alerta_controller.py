# ==============================
# CONTROLADOR DE ALERTAS
# ==============================

from models.alerta import Alerta


class AlertaController:
    """
    Esta clase contiene las funciones principales para manejar alertas.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario quiere ver alertas pendientes, este controller las obtiene.
    - Si el usuario marca una alerta como leida, este controller la actualiza.
    """

    # ==============================
    # OBTENER ALERTAS PENDIENTES
    # ==============================

    def obtener_alertas_pendientes(self):
        """
        Esta funcion obtiene todas las alertas que aun no han sido atendidas.

        Retorna una lista de alertas pendientes.
        """

        try:
            alertas = Alerta.obtener_alertas_pendientes()
            return alertas

        except Exception as e:
            print(f"Error al obtener alertas pendientes: {e}")
            return []

    # ==============================
    # MARCAR ALERTA COMO LEIDA
    # ==============================

    def marcar_alerta_como_leida(self, id_alerta):
        """
        Esta funcion marca una alerta especifica como atendida.

        Parametro:
        id_alerta: Identificador de la alerta.
        """

        try:
            Alerta.marcar_como_leida(id_alerta)
            print(f"Alerta {id_alerta} marcada como leida.")
            return True

        except Exception as e:
            print(f"Error al marcar alerta como leida: {e}")
            return False

    # ==============================
    # GENERAR ALERTA
    # ==============================

    def generar_alerta(self, id_producto, mensaje):
        """
        Esta funcion genera una nueva alerta de stock bajo.

        Parametros:
        id_producto: Identificador del producto con stock bajo.
        mensaje: Mensaje descriptivo de la alerta.
        """

        try:
            Alerta.generar_alerta_stock_bajo(id_producto, mensaje)
            return True

        except Exception as e:
            print(f"Error al generar alerta: {e}")
            return False

    # ==============================
    # VERIFICAR Y GENERAR ALERTAS POR STOCK
    # ==============================

    def verificar_stock_y_generar_alertas(self, productos_con_stock):
        """
        Esta funcion recorre una lista de productos y genera alertas
        para aquellos que tienen stock por debajo del minimo.

        Parametro:
        productos_con_stock: Lista de tuplas (id_producto, nombre, stock_actual, stock_minimo)
        """

        alertas_generadas = 0

        for producto in productos_con_stock:
            id_producto = producto[0]
            nombre = producto[1]
            stock_actual = producto[2]
            stock_minimo = producto[3]

            if stock_actual <= stock_minimo:
                if stock_actual <= 0:
                    mensaje = f"ATENCION: El producto '{nombre}' no tiene existencia."
                else:
                    mensaje = f"ALERTA: El producto '{nombre}' tiene stock bajo. Quedan {stock_actual} unidades (Minimo: {stock_minimo})"

                self.generar_alerta(id_producto, mensaje)
                alertas_generadas += 1

        return alertas_generadas