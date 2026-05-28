# Importamos sqlite3 para manejar posibles errores de base de datos.
import sqlite3

# Importamos la conexión a la base de datos.
from database.conexion import conectar_bd


# ==============================
# CONTROLADOR DE INVENTARIO
# ==============================

class InventarioController:
    """
    Esta clase se encarga de manejar las operaciones relacionadas
    con el inventario de productos.

    Aquí se controlan:
    - Entradas de artículos.
    - Salidas de artículos.
    - Consulta de existencias.
    - Actualización de ubicación.
    - Listado general del inventario.
    """

    # ==============================
    # LISTAR INVENTARIO
    # ==============================

    def listar_inventario(self):
        """
        Consulta todos los productos junto con su información de inventario.

        Retorna una lista con:
        id_producto, nombre, código, precio, stock mínimo,
        cantidad actual y ubicación.
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
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion
                FROM producto p
                LEFT JOIN inventario i
                ON p.id_producto = i.id_producto
                ORDER BY p.nombre ASC
            """)

            inventario = cursor.fetchall()
            conexion.close()

            return inventario

        except sqlite3.Error as error:
            print("Error al listar inventario:", error)
            return []

    # ==============================
    # OBTENER PRODUCTOS
    # ==============================

    def obtener_productos(self):
        """
        Método auxiliar para obtener productos con inventario.

        Se deja este nombre porque puede ser usado por otras partes
        del sistema o por las vistas.
        """

        return self.listar_inventario()

    # ==============================
    # OBTENER STOCK DE UN PRODUCTO
    # ==============================

    def obtener_stock(self, id_producto):
        """
        Consulta la cantidad actual de un producto.

        Parámetro:
        id_producto: identificador del producto.

        Retorna:
        cantidad actual si existe.
        0 si no tiene inventario registrado.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return resultado[0]

            return 0

        except sqlite3.Error as error:
            print("Error al obtener stock:", error)
            return 0

    # ==============================
    # REGISTRAR ENTRADA
    # ==============================

    def registrar_entrada(self, id_producto, cantidad, ubicacion=None):
        """
        Registra una entrada de artículos al inventario.

        Esto significa que llegaron productos nuevos
        y se deben sumar a la existencia actual.

        Parámetros:
        id_producto: producto al que se le sumará inventario.
        cantidad: cantidad recibida.
        ubicacion: ubicación física del producto, opcional.

        Retorna:
        True y mensaje si se registró correctamente.
        False y mensaje si hubo error.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if cantidad <= 0:
            return False, "La cantidad de entrada debe ser mayor que cero."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Primero revisamos si el producto ya tiene registro de inventario.
            cursor.execute("""
                SELECT id_inventario, cantidad_actual, ubicacion
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                # Si ya existe, sumamos la cantidad nueva.
                id_inventario = inventario[0]
                cantidad_actual = inventario[1]
                ubicacion_actual = inventario[2]

                nueva_cantidad = cantidad_actual + cantidad

                # Si no se manda una nueva ubicación, mantenemos la anterior.
                if ubicacion is None or ubicacion == "":
                    ubicacion = ubicacion_actual

                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?, ubicacion = ?
                    WHERE id_inventario = ?
                """, (
                    nueva_cantidad,
                    ubicacion,
                    id_inventario
                ))

            else:
                # Si no existe inventario para ese producto, lo creamos.
                if ubicacion is None:
                    ubicacion = ""

                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, ?)
                """, (
                    id_producto,
                    cantidad,
                    ubicacion
                ))

            conexion.commit()
            conexion.close()

            return True, "Entrada registrada correctamente."

        except sqlite3.Error as error:
            return False, f"Error al registrar entrada: {error}"

    # ==============================
    # REGISTRAR SALIDA
    # ==============================

    def registrar_salida(self, id_producto, cantidad):
        """
        Registra una salida de artículos del inventario.

        Esto se utiliza cuando se vende un producto o se retira
        del inventario.

        Parámetros:
        id_producto: producto al que se le descontará inventario.
        cantidad: cantidad que se descontará.

        Retorna:
        True y mensaje si se descontó correctamente.
        False y mensaje si hubo error.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if cantidad <= 0:
            return False, "La cantidad de salida debe ser mayor que cero."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Consultamos la existencia actual.
            cursor.execute("""
                SELECT id_inventario, cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if not inventario:
                conexion.close()
                return False, "El producto no tiene inventario registrado."

            id_inventario = inventario[0]
            cantidad_actual = inventario[1]

            # Validamos que haya suficiente existencia.
            if cantidad > cantidad_actual:
                conexion.close()
                return False, "No hay suficiente existencia disponible."

            nueva_cantidad = cantidad_actual - cantidad

            cursor.execute("""
                UPDATE inventario
                SET cantidad_actual = ?
                WHERE id_inventario = ?
            """, (
                nueva_cantidad,
                id_inventario
            ))

            conexion.commit()
            conexion.close()

            return True, "Salida registrada correctamente."

        except sqlite3.Error as error:
            return False, f"Error al registrar salida: {error}"

    # ==============================
    # ACTUALIZAR STOCK
    # ==============================

    def actualizar_stock(self, id_producto, nueva_cantidad):
        """
        Actualiza directamente la cantidad actual de un producto.

        Este método no suma ni resta, solamente reemplaza
        la cantidad actual por la nueva cantidad.

        Parámetros:
        id_producto: producto a modificar.
        nueva_cantidad: nueva existencia del producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if nueva_cantidad < 0:
            return False, "La cantidad no puede ser negativa."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificamos si ya existe registro de inventario.
            cursor.execute("""
                SELECT id_inventario
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?
                    WHERE id_producto = ?
                """, (
                    nueva_cantidad,
                    id_producto
                ))
            else:
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, ?)
                """, (
                    id_producto,
                    nueva_cantidad,
                    ""
                ))

            conexion.commit()
            conexion.close()

            return True, "Stock actualizado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al actualizar stock: {error}"

    # ==============================
    # ACTUALIZAR UBICACIÓN
    # ==============================

    def actualizar_ubicacion(self, id_producto, nueva_ubicacion):
        """
        Actualiza la ubicación física de un producto dentro del inventario.

        Parámetros:
        id_producto: producto a modificar.
        nueva_ubicacion: nueva ubicación del producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Revisamos si existe inventario para el producto.
            cursor.execute("""
                SELECT id_inventario
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                cursor.execute("""
                    UPDATE inventario
                    SET ubicacion = ?
                    WHERE id_producto = ?
                """, (
                    nueva_ubicacion,
                    id_producto
                ))
            else:
                # Si no existe inventario, se crea con cantidad 0.
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, ?)
                """, (
                    id_producto,
                    0,
                    nueva_ubicacion
                ))

            conexion.commit()
            conexion.close()

            return True, "Ubicación actualizada correctamente."

        except sqlite3.Error as error:
            return False, f"Error al actualizar ubicación: {error}"

    # ==============================
    # AGREGAR PRODUCTO DESDE INVENTARIO
    # ==============================

    def agregar_producto(
        self,
        nombre,
        codigo,
        precio,
        stock_minimo,
        cantidad_actual=0,
        ubicacion="",
        id_categoria=None,
        id_proveedor=None
    ):
        """
        Permite agregar un producto desde el módulo de inventario.

        Este método crea primero el producto en la tabla producto
        y después crea su inventario inicial.

        Nota:
        Este método puede servir para una pantalla sencilla de inventario.
        """

        if nombre == "" or codigo == "":
            return False, "El nombre y el código son obligatorios."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if stock_minimo < 0:
            return False, "El stock mínimo no puede ser negativo."

        if cantidad_actual < 0:
            return False, "La cantidad actual no puede ser negativa."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO producto (
                    nombre,
                    codigo,
                    precio,
                    stock_minimo,
                    id_categoria,
                    id_proveedor
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nombre,
                codigo,
                precio,
                stock_minimo,
                id_categoria,
                id_proveedor
            ))

            id_producto = cursor.lastrowid

            cursor.execute("""
                INSERT INTO inventario (
                    id_producto,
                    cantidad_actual,
                    ubicacion
                )
                VALUES (?, ?, ?)
            """, (
                id_producto,
                cantidad_actual,
                ubicacion
            ))

            conexion.commit()
            conexion.close()

            return True, "Producto agregado al inventario correctamente."

        except sqlite3.IntegrityError:
            return False, "El código del producto ya existe."

        except sqlite3.Error as error:
            return False, f"Error al agregar producto al inventario: {error}"

    # ==============================
    # ELIMINAR INVENTARIO DE PRODUCTO
    # ==============================

    def eliminar_producto(self, id_producto):
        """
        Elimina el registro de inventario de un producto.

        Importante:
        Este método NO elimina el producto del catálogo,
        solamente elimina su inventario.

        Para eliminar el producto completo se debe usar ProductoController.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            conexion.commit()
            conexion.close()

            return True, "Inventario eliminado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar inventario: {error}"

    # ==============================
    # VERIFICAR STOCK BAJO
    # ==============================

    def verificar_stock_bajo(self, id_producto):
        """
        Verifica si un producto llegó a su stock mínimo.

        Retorna:
        True si el stock actual es menor o igual al stock mínimo.
        False si todavía tiene suficiente existencia.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    p.stock_minimo,
                    IFNULL(i.cantidad_actual, 0)
                FROM producto p
                LEFT JOIN inventario i
                ON p.id_producto = i.id_producto
                WHERE p.id_producto = ?
            """, (id_producto,))

            resultado = cursor.fetchone()
            conexion.close()

            if not resultado:
                return False

            stock_minimo = resultado[0]
            cantidad_actual = resultado[1]

            if cantidad_actual <= stock_minimo:
                return True

            return False

        except sqlite3.Error as error:
            print("Error al verificar stock bajo:", error)
            return False


# ==============================
# PRUEBA DEL CONTROLADOR
# ==============================

if __name__ == "__main__":
    """
    Esta prueba solo se ejecuta si abrimos este archivo directamente.
    Sirve para revisar que el controlador no tenga errores básicos.
    """

    controlador = InventarioController()

    inventario = controlador.listar_inventario()

    print("Inventario actual:")
    for item in inventario:
        print(item)