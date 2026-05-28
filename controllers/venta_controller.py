# Importamos sqlite3 para manejar errores de base de datos.
import sqlite3

# Importamos datetime para registrar fecha y hora de la venta.
from datetime import datetime

# Importamos la conexión a la base de datos.
from database.conexion import conectar_bd


# ==============================
# CONTROLADOR DE VENTAS
# ==============================

class VentaController:
    """
    Esta clase controla las operaciones relacionadas con ventas.

    Una venta se guarda en dos partes:

    1. Tabla venta:
       Guarda la información general de la venta.
       Ejemplo: fecha, total, usuario.

    2. Tabla detalle_venta:
       Guarda los productos incluidos en esa venta.
       Ejemplo: producto, cantidad y subtotal.
    """

    # ==============================
    # VERIFICAR SI EXISTE UNA COLUMNA
    # ==============================

    def tabla_tiene_columna(self, nombre_tabla, nombre_columna):
        """
        Verifica si una tabla tiene una columna específica.

        Esto ayuda porque algunas versiones de la base de datos
        pueden tener campos como metodo_pago o precio_unitario,
        y otras versiones no.

        Retorna:
        True si la columna existe.
        False si no existe.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute(f"PRAGMA table_info({nombre_tabla})")
            columnas = cursor.fetchall()

            conexion.close()

            for columna in columnas:
                if columna[1] == nombre_columna:
                    return True

            return False

        except sqlite3.Error:
            return False

    # ==============================
    # REGISTRAR VENTA
    # ==============================

    def registrar_venta(self, total, id_usuario, metodo_pago="Efectivo", fecha=None):
        """
        Registra una venta en la tabla venta.

        Parámetros:
        total: total general de la venta.
        id_usuario: usuario que realizó la venta.
        metodo_pago: forma de pago utilizada.
        fecha: fecha de la venta. Si no se manda, se genera automáticamente.

        Retorna:
        True, mensaje e id_venta si se registró correctamente.
        False, mensaje y None si hubo error.
        """

        if total <= 0:
            return False, "El total de la venta debe ser mayor que cero.", None

        if id_usuario is None:
            return False, "Debe existir un usuario para registrar la venta.", None

        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Revisamos si la tabla venta tiene la columna metodo_pago.
            tiene_metodo_pago = self.tabla_tiene_columna("venta", "metodo_pago")

            if tiene_metodo_pago:
                cursor.execute("""
                    INSERT INTO venta (
                        fecha,
                        total,
                        metodo_pago,
                        id_usuario
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    fecha,
                    total,
                    metodo_pago,
                    id_usuario
                ))
            else:
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

            conexion.commit()
            conexion.close()

            return True, "Venta registrada correctamente.", id_venta

        except sqlite3.Error as error:
            return False, f"Error al registrar venta: {error}", None

    # ==============================
    # REGISTRAR DETALLE DE VENTA
    # ==============================

    def registrar_detalle_venta(
        self,
        id_venta,
        id_producto,
        cantidad,
        subtotal,
        precio_unitario=None
    ):
        """
        Registra un producto dentro del detalle de una venta.

        Parámetros:
        id_venta: venta a la que pertenece el producto.
        id_producto: producto vendido.
        cantidad: cantidad vendida.
        subtotal: subtotal de ese producto.
        precio_unitario: precio individual del producto.
        """

        if id_venta is None:
            return False, "Debe existir una venta."

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor que cero."

        if subtotal <= 0:
            return False, "El subtotal debe ser mayor que cero."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Revisamos si la tabla detalle_venta tiene precio_unitario.
            tiene_precio_unitario = self.tabla_tiene_columna(
                "detalle_venta",
                "precio_unitario"
            )

            if tiene_precio_unitario:
                if precio_unitario is None:
                    precio_unitario = subtotal / cantidad

                cursor.execute("""
                    INSERT INTO detalle_venta (
                        id_venta,
                        id_producto,
                        cantidad,
                        precio_unitario,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    id_venta,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal
                ))
            else:
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

            conexion.commit()
            conexion.close()

            return True, "Detalle de venta registrado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al registrar detalle de venta: {error}"

    # ==============================
    # REGISTRAR VENTA COMPLETA
    # ==============================

    def registrar_venta_completa(
        self,
        id_usuario,
        productos,
        metodo_pago="Efectivo"
    ):
        """
        Registra una venta completa con todos sus productos.

        Parámetros:
        id_usuario: usuario que realiza la venta.
        productos: lista de productos vendidos.

        Cada producto debe venir con esta estructura:

        {
            "id_producto": 1,
            "cantidad": 2,
            "precio_unitario": 45.50
        }

        Este método:
        1. Calcula el total.
        2. Registra la venta.
        3. Registra cada detalle de venta.
        """

        if not productos:
            return False, "La venta debe tener al menos un producto.", None

        total = 0

        # Calculamos el total general.
        for producto in productos:
            cantidad = producto.get("cantidad", 0)
            precio_unitario = producto.get("precio_unitario", 0)

            if cantidad <= 0:
                return False, "La cantidad de cada producto debe ser mayor que cero.", None

            if precio_unitario <= 0:
                return False, "El precio de cada producto debe ser mayor que cero.", None

            total += cantidad * precio_unitario

        # Registramos la venta principal.
        resultado, mensaje, id_venta = self.registrar_venta(
            total=total,
            id_usuario=id_usuario,
            metodo_pago=metodo_pago
        )

        if not resultado:
            return False, mensaje, None

        # Registramos los detalles.
        for producto in productos:
            id_producto = producto.get("id_producto")
            cantidad = producto.get("cantidad")
            precio_unitario = producto.get("precio_unitario")
            subtotal = cantidad * precio_unitario

            resultado_detalle, mensaje_detalle = self.registrar_detalle_venta(
                id_venta=id_venta,
                id_producto=id_producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )

            if not resultado_detalle:
                return False, mensaje_detalle, id_venta

        return True, "Venta completa registrada correctamente.", id_venta

    # ==============================
    # LISTAR VENTAS
    # ==============================

    def listar_ventas(self):
        """
        Consulta todas las ventas registradas.

        Retorna una lista de ventas.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            tiene_metodo_pago = self.tabla_tiene_columna("venta", "metodo_pago")

            if tiene_metodo_pago:
                cursor.execute("""
                    SELECT
                        v.id_venta,
                        v.fecha,
                        v.total,
                        v.metodo_pago,
                        u.nombre
                    FROM venta v
                    INNER JOIN usuario u
                    ON v.id_usuario = u.id_usuario
                    ORDER BY v.fecha DESC
                """)
            else:
                cursor.execute("""
                    SELECT
                        v.id_venta,
                        v.fecha,
                        v.total,
                        u.nombre
                    FROM venta v
                    INNER JOIN usuario u
                    ON v.id_usuario = u.id_usuario
                    ORDER BY v.fecha DESC
                """)

            ventas = cursor.fetchall()

            conexion.close()

            return ventas

        except sqlite3.Error as error:
            print("Error al listar ventas:", error)
            return []

    # ==============================
    # OBTENER VENTA POR ID
    # ==============================

    def obtener_venta_por_id(self, id_venta):
        """
        Busca una venta por su identificador.

        Parámetro:
        id_venta: identificador de la venta.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            tiene_metodo_pago = self.tabla_tiene_columna("venta", "metodo_pago")

            if tiene_metodo_pago:
                cursor.execute("""
                    SELECT
                        id_venta,
                        fecha,
                        total,
                        metodo_pago,
                        id_usuario
                    FROM venta
                    WHERE id_venta = ?
                """, (id_venta,))
            else:
                cursor.execute("""
                    SELECT
                        id_venta,
                        fecha,
                        total,
                        id_usuario
                    FROM venta
                    WHERE id_venta = ?
                """, (id_venta,))

            venta = cursor.fetchone()

            conexion.close()

            return venta

        except sqlite3.Error as error:
            print("Error al obtener venta:", error)
            return None

    # ==============================
    # OBTENER DETALLE DE VENTA
    # ==============================

    def obtener_detalle_venta(self, id_venta):
        """
        Consulta los productos vendidos dentro de una venta.

        Parámetro:
        id_venta: identificador de la venta.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            tiene_precio_unitario = self.tabla_tiene_columna(
                "detalle_venta",
                "precio_unitario"
            )

            if tiene_precio_unitario:
                cursor.execute("""
                    SELECT
                        dv.id_detalle,
                        p.nombre,
                        p.codigo,
                        dv.cantidad,
                        dv.precio_unitario,
                        dv.subtotal
                    FROM detalle_venta dv
                    INNER JOIN producto p
                    ON dv.id_producto = p.id_producto
                    WHERE dv.id_venta = ?
                """, (id_venta,))
            else:
                cursor.execute("""
                    SELECT
                        dv.id_detalle,
                        p.nombre,
                        p.codigo,
                        dv.cantidad,
                        dv.subtotal
                    FROM detalle_venta dv
                    INNER JOIN producto p
                    ON dv.id_producto = p.id_producto
                    WHERE dv.id_venta = ?
                """, (id_venta,))

            detalles = cursor.fetchall()

            conexion.close()

            return detalles

        except sqlite3.Error as error:
            print("Error al obtener detalle de venta:", error)
            return []

    # ==============================
    # ELIMINAR VENTA
    # ==============================

    def eliminar_venta(self, id_venta):
        """
        Elimina una venta y sus detalles.

        Nota:
        Este método no regresa el inventario.
        Para un sistema real habría que devolver el stock.
        Para esta tarea escolar queda como eliminación simple.
        """

        if id_venta is None:
            return False, "Debe seleccionar una venta."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM detalle_venta
                WHERE id_venta = ?
            """, (id_venta,))

            cursor.execute("""
                DELETE FROM venta
                WHERE id_venta = ?
            """, (id_venta,))

            conexion.commit()
            conexion.close()

            return True, "Venta eliminada correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar venta: {error}"

    # ==============================
    # MÉTODOS ALTERNATIVOS
    # ==============================

    def crear_venta(self, total, id_usuario, metodo_pago="Efectivo"):
        """
        Método alternativo para crear una venta.

        Se agrega por si otro archivo del proyecto usa el nombre crear_venta.
        """

        return self.registrar_venta(total, id_usuario, metodo_pago)

    def obtener_ventas(self):
        """
        Método alternativo para listar ventas.

        Se agrega por si otro archivo usa obtener_ventas.
        """

        return self.listar_ventas()

    def obtener_detalles(self, id_venta):
        """
        Método alternativo para obtener detalles.

        Se agrega por si otro archivo usa obtener_detalles.
        """

        return self.obtener_detalle_venta(id_venta)


# ==============================
# PRUEBA DEL CONTROLADOR
# ==============================

if __name__ == "__main__":
    """
    Esta prueba sirve para verificar que el controlador no marque errores.
    """

    controlador = VentaController()

    ventas = controlador.listar_ventas()

    print("Ventas registradas:")
    for venta in ventas:
        print(venta)