# ==============================
# SERVICIO DE VENTAS
# ==============================

"""
Este archivo contiene la lógica principal para procesar ventas.

El service se encarga de:
- Validar que la venta tenga productos.
- Validar cantidades.
- Validar precios.
- Verificar stock disponible.
- Calcular el total de la venta.
- Mandar la venta al controlador para guardarla en la base de datos.

Este archivo no dibuja pantallas.
Solo maneja lógica del sistema.
"""

import sqlite3

from database.conexion import conectar_bd
from controllers.venta_controller import VentaController
from controllers.inventario_controller import InventarioController
from utils.validaciones import es_numero, es_entero


class VentaService:
    """
    Servicio de ventas.

    Esta clase funciona como una capa intermedia entre la interfaz
    y el controlador de ventas.
    """

    def __init__(self):
        """
        Al iniciar el servicio, se crean los controladores necesarios.
        """

        self.venta_controller = VentaController()
        self.inventario_controller = InventarioController()

    # ==============================
    # OBTENER PRECIO DE PRODUCTO
    # ==============================

    def obtener_precio_producto(self, id_producto):
        """
        Obtiene el precio de un producto desde la base de datos.

        Parámetro:
        id_producto: ID del producto.

        Retorna:
        Precio del producto si existe.
        None si no se encuentra.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT precio
                FROM producto
                WHERE id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return resultado[0]

            return None

        except sqlite3.Error as error:
            print(f"Error al obtener precio del producto: {error}")
            return None

    # ==============================
    # NORMALIZAR PRODUCTOS
    # ==============================

    def normalizar_productos(self, productos):
        """
        Convierte la lista de productos a un formato estándar.

        Formato esperado por el sistema:

        {
            "id_producto": 1,
            "cantidad": 2,
            "precio": 45.50
        }

        También acepta "precio_unitario" por si otro archivo lo usa.
        """

        productos_normalizados = []

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")

            # Puede venir como precio o como precio_unitario.
            precio = producto.get("precio")

            if precio is None:
                precio = producto.get("precio_unitario")

            # Si no se recibió precio, lo buscamos en la base de datos.
            if precio is None and id_producto is not None:
                precio = self.obtener_precio_producto(id_producto)

            productos_normalizados.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio": precio
            })

        return productos_normalizados

    # ==============================
    # VALIDAR PRODUCTOS DE LA VENTA
    # ==============================

    def validar_productos(self, productos):
        """
        Valida que la venta tenga productos correctos.

        Revisa:
        - Que exista al menos un producto.
        - Que cada producto tenga ID.
        - Que la cantidad sea entera y mayor que cero.
        - Que el precio sea numérico y mayor que cero.
        - Que haya stock suficiente.
        """

        if not productos:
            return False, "La venta debe tener al menos un producto."

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio")

            if id_producto is None:
                return False, "Todos los productos deben tener un ID."

            if not es_entero(cantidad):
                return False, "La cantidad debe ser un número entero."

            cantidad = int(cantidad)

            if cantidad <= 0:
                return False, "La cantidad debe ser mayor que cero."

            if not es_numero(precio):
                return False, "El precio debe ser numérico."

            precio = float(precio)

            if precio <= 0:
                return False, "El precio debe ser mayor que cero."

            # Verificamos stock actual.
            stock_actual = self.inventario_controller.obtener_stock(id_producto)

            if cantidad > stock_actual:
                return False, f"No hay suficiente existencia para el producto con ID {id_producto}."

        return True, "Productos válidos."

    # ==============================
    # CALCULAR TOTAL
    # ==============================

    def calcular_total(self, productos):
        """
        Calcula el total de la venta.

        Multiplica cantidad por precio de cada producto
        y suma todos los subtotales.
        """

        total = 0

        for producto in productos:
            cantidad = int(producto.get("cantidad"))
            precio = float(producto.get("precio"))

            subtotal = cantidad * precio
            total += subtotal

        return total

    # ==============================
    # PROCESAR VENTA
    # ==============================

    def procesar_venta(self, productos, id_usuario=1):
        """
        Procesa una venta completa.

        Parámetros:
        productos: lista de productos vendidos.
        id_usuario: usuario que realiza la venta.
                    Por defecto se usa 1, que corresponde al admin de prueba.

        Flujo:
        1. Normaliza productos.
        2. Valida productos.
        3. Calcula total.
        4. Registra la venta con VentaController.
        """

        if id_usuario is None:
            return False, "Debe existir un usuario para registrar la venta."

        productos = self.normalizar_productos(productos)

        resultado, mensaje = self.validar_productos(productos)

        if not resultado:
            return False, mensaje

        total = self.calcular_total(productos)

        resultado_venta = self.venta_controller.registrar_venta(
            productos=productos,
            total=total,
            id_usuario=id_usuario
        )

        if resultado_venta:
            return True, f"Venta registrada correctamente. Total: ${total:.2f}"

        return False, "No se pudo registrar la venta."

    # ==============================
    # REGISTRAR VENTA
    # ==============================

    def registrar_venta(self, productos, id_usuario=1):
        """
        Método alternativo para registrar venta.

        Se deja para que otros archivos puedan llamar registrar_venta()
        en lugar de procesar_venta().
        """

        return self.procesar_venta(productos, id_usuario)

    # ==============================
    # OBTENER VENTAS
    # ==============================

    def obtener_ventas(self):
        """
        Obtiene todas las ventas registradas.
        """

        return self.venta_controller.obtener_ventas()

    # ==============================
    # LISTAR VENTAS
    # ==============================

    def listar_ventas(self):
        """
        Método alternativo para listar ventas.
        """

        return self.obtener_ventas()

    # ==============================
    # OBTENER DETALLE DE VENTA
    # ==============================

    def obtener_detalle_venta(self, venta_id):
        """
        Obtiene los productos incluidos en una venta.
        """

        if venta_id is None:
            return []

        return self.venta_controller.obtener_detalle_venta(venta_id)

    # ==============================
    # ELIMINAR VENTA
    # ==============================

    def eliminar_venta(self, venta_id):
        """
        Elimina una venta.

        Nota:
        En esta versión escolar, eliminar una venta no devuelve stock.
        """

        if venta_id is None:
            return False, "Debe seleccionar una venta."

        resultado = self.venta_controller.eliminar_venta(venta_id)

        if resultado:
            return True, "Venta eliminada correctamente."

        return False, "No se pudo eliminar la venta."


# ==============================
# PRUEBA DEL SERVICIO
# ==============================

if __name__ == "__main__":
    """
    Esta prueba permite verificar que el archivo no marque errores.

    No registra una venta automáticamente para evitar modificar datos
    sin intención.
    """

    servicio = VentaService()

    print("Ventas registradas:")
    ventas = servicio.obtener_ventas()

    for venta in ventas:
        print(venta)