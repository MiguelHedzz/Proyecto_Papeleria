# ==============================
# MODELO VENTA
# ==============================

class Venta:
    """
    Esta clase representa una venta realizada en el sistema.

    Una venta registra la transacción comercial entre la papelería
    y el cliente. Incluye la fecha, el total y el usuario que la realizó.

    Ejemplo:
    - Venta #001 del 25/04/2026 por $150.00
    - Venta #002 del 26/04/2026 por $75.50
    """

    def __init__(
        self,
        id_venta=None,
        fecha="",
        total=0.0,
        metodo_pago="",
        id_usuario=None
    ):
        """
        Este método se ejecuta automáticamente cuando se crea un objeto Venta.

        Parámetros:
        id_venta: Identificador único de la venta.
        fecha: Fecha y hora en que se realizó la venta.
        total: Monto total de la venta.
        metodo_pago: Forma de pago utilizada (Efectivo, Tarjeta, Transferencia).
        id_usuario: Identificador del usuario que realizó la venta.
        """

        # Guardamos el id de la venta.
        # Puede ser None si todavía no se guarda en la base de datos.
        self.id_venta = id_venta

        # Guardamos la fecha de la venta.
        self.fecha = fecha

        # Guardamos el total de la venta.
        self.total = total

        # Guardamos el método de pago utilizado.
        self.metodo_pago = metodo_pago

        # Guardamos el id del usuario que realizó la venta.
        self.id_usuario = id_usuario

    # ==============================
    # MOSTRAR INFORMACIÓN
    # ==============================

    def mostrar_informacion(self):
        """
        Este método devuelve la información de la venta
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "total": self.total,
            "metodo_pago": self.metodo_pago,
            "id_usuario": self.id_usuario
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este método revisa que los datos importantes de la venta
        estén completos.

        Retorna True si los datos son correctos.
        Retorna False si falta algún dato o si hay valores incorrectos.
        """

        # Validamos que la fecha no esté vacía.
        if self.fecha == "":
            return False

        # Validamos que el total sea mayor que cero.
        if self.total <= 0:
            return False

        # Validamos que el método de pago no esté vacío.
        if self.metodo_pago == "":
            return False

        # Validamos que exista un usuario relacionado.
        if self.id_usuario is None:
            return False

        return True

    # ==============================
    # CALCULAR TOTAL
    # ==============================

    def calcular_total(self, detalles):
        """
        Este método calcula el total de la venta sumando
        los subtotales de todos los detalles.

        Parámetro:
        detalles: Lista de objetos DetalleVenta relacionados.

        Retorna el total calculado.
        """

        total_calculado = 0.0

        for detalle in detalles:
            total_calculado += detalle.subtotal

        self.total = total_calculado
        return self.total

    # ==============================
    # ACTUALIZAR MÉTODO DE PAGO
    # ==============================

    def actualizar_metodo_pago(self, nuevo_metodo):
        """
        Este método permite cambiar el método de pago de la venta.

        Parámetro:
        nuevo_metodo: Nuevo método de pago (Efectivo, Tarjeta, Transferencia).
        """

        if nuevo_metodo != "":
            self.metodo_pago = nuevo_metodo
            return True

        return False

    # ==============================
    # OBTENER RESUMEN
    # ==============================

    def obtener_resumen(self):
        """
        Este método devuelve un resumen corto de la venta.

        Útil para mostrar en listados o tickets rápidos.
        """

        return f"Venta #{self.id_venta} - {self.fecha} - ${self.total:.2f}"