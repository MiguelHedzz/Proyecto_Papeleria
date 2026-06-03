# ==============================
# SERVICIO DE VENTAS
# ==============================

"""
Este archivo contiene la lógica principal para procesar ventas.

Corrige la integración entre la pantalla Nueva Venta y la base de datos.

Qué hace:
- Valida que la venta tenga productos.
- Valida cantidades y precios.
- Verifica que exista stock suficiente.
- Calcula el total.
- Registra la venta en la tabla venta.
- Registra el detalle en detalle_venta.
- Descuenta inventario.

Este archivo no dibuja pantallas. Solo maneja la lógica de ventas.
"""

import sqlite3
from datetime import datetime

from database.conexion import conectar_bd
from controllers.venta_controller import VentaController
from controllers.inventario_controller import InventarioController
from utils.validaciones import es_numero, es_entero


class VentaService:
    """
    Servicio de ventas.

    Esta clase funciona como intermediaria entre la interfaz gráfica
    y la base de datos.
    """

    def __init__(self):
        self.venta_controller = VentaController()
        self.inventario_controller = InventarioController()

    # ==============================
    # OBTENER PRECIO DE PRODUCTO
    # ==============================

    def obtener_precio_producto(self, id_producto):
        """
        Obtiene el precio de un producto desde la base de datos.
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

        Formato usado:
        {
            "id_producto": 1,
            "cantidad": 2,
            "precio": 45.50
        }

        También acepta "precio_unitario" por compatibilidad.
        """

        productos_normalizados = []

        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio = producto.get("precio")

            if precio is None:
                precio = producto.get("precio_unitario")

            if precio is None and id_producto is not None:
                precio = self.obtener_precio_producto(id_producto)

            productos_normalizados.append({
                "id_producto": id_producto,
                "cantidad": cantidad,
                "precio": precio
            })

        return productos_normalizados

    # ==============================
    # VALIDAR PRODUCTOS
    # ==============================

    def validar_productos(self, productos):
        """
        Valida los productos de una venta.

        Revisa:
        - Que haya al menos un producto.
        - Que cada producto tenga ID.
        - Que la cantidad sea entera y mayor que cero.
        - Que el precio sea numérico y mayor que cero.
        - Que haya stock suficiente.
        """

        if not productos:
            return False, "La venta debe tener al menos un producto."

        cantidades_por_producto = {}

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

            cantidades_por_producto[id_producto] = cantidades_por_producto.get(id_producto, 0) + cantidad

        # Validamos stock acumulado por producto.
        for id_producto, cantidad_total in cantidades_por_producto.items():
            stock_actual = self.inventario_controller.obtener_stock(id_producto)

            if cantidad_total > stock_actual:
                return False, f"No hay suficiente existencia para el producto con ID {id_producto}."

        return True, "Productos válidos."

    # ==============================
    # CALCULAR TOTAL
    # ==============================

    def calcular_total(self, productos):
        """
        Calcula el total de la venta.
        """

        total = 0.0

        for producto in productos:
            cantidad = int(producto.get("cantidad"))
            precio = float(producto.get("precio"))
            total += cantidad * precio

        return total

    # ==============================
    # PROCESAR VENTA
    # ==============================

    def procesar_venta(self, productos, id_usuario=1, metodo_pago="Efectivo"):
        """
        Procesa una venta completa.

        Flujo:
        1. Normaliza productos.
        2. Valida productos.
        3. Calcula total.
        4. Guarda venta.
        5. Guarda detalle.
        6. Descuenta inventario.
        """

        if id_usuario is None:
            return False, "Debe existir un usuario para registrar la venta."

        productos = self.normalizar_productos(productos)

        resultado, mensaje = self.validar_productos(productos)
        if not resultado:
            return False, mensaje

        total = self.calcular_total(productos)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO venta (
                    fecha,
                    total,
                    id_usuario
                )
                VALUES (?, ?, ?)
            """, (
                fecha,
                total,
                id_usuario
            ))

            id_venta = cursor.lastrowid

            for producto in productos:
                id_producto = producto.get("id_producto")
                cantidad = int(producto.get("cantidad"))
                precio = float(producto.get("precio"))
                subtotal = cantidad * precio

                cursor.execute("""
                    INSERT INTO detalle_venta (
                        id_venta,
                        id_producto,
                        cantidad,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    id_venta,
                    id_producto,
                    cantidad,
                    subtotal
                ))

                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = cantidad_actual - ?
                    WHERE id_producto = ?
                """, (
                    cantidad,
                    id_producto
                ))

            conexion.commit()
            conexion.close()

            return True, f"Venta registrada correctamente. Total: ${total:.2f}"

        except sqlite3.Error as error:
            return False, f"Error al registrar venta: {error}"

    # ==============================
    # MÉTODOS AUXILIARES
    # ==============================

    def registrar_venta(self, productos, id_usuario=1):
        """
        Método alternativo para registrar venta.
        """

        return self.procesar_venta(productos, id_usuario)

    def obtener_ventas(self):
        """
        Obtiene todas las ventas registradas.
        """

        return self.venta_controller.obtener_ventas()

    def listar_ventas(self):
        """
        Método alternativo para listar ventas.
        """

        return self.obtener_ventas()

    def obtener_detalle_venta(self, venta_id):
        """
        Obtiene los productos incluidos en una venta.
        """

        if venta_id is None:
            return []

        return self.venta_controller.obtener_detalle_venta(venta_id)

    def eliminar_venta(self, venta_id):
        """
        Elimina una venta.

        En esta versión escolar, eliminar una venta no devuelve stock.
        """

        if venta_id is None:
            return False, "Debe seleccionar una venta."

        resultado = self.venta_controller.eliminar_venta(venta_id)

        if isinstance(resultado, tuple):
            return resultado

        if resultado:
            return True, "Venta eliminada correctamente."

        return False, "No se pudo eliminar la venta."


if __name__ == "__main__":
    servicio = VentaService()

    print("Ventas registradas:")
    for venta in servicio.obtener_ventas():
        print(venta)
