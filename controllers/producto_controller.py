# Importamos sqlite3 para poder manejar errores relacionados con la base de datos.
import sqlite3

# Importamos la conexión a la base de datos desde la carpeta database.
from database.conexion import conectar_bd


# ==============================
# CONTROLADOR DE PRODUCTOS
# ==============================

class ProductoController:
    """
    Esta clase contiene las funciones principales para manejar productos.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario registra un producto, este controller lo guarda.
    - Si el usuario busca un producto, este controller consulta la base de datos.
    - Si el usuario modifica un producto, este controller actualiza la información.
    """

    # ==============================
    # REGISTRAR PRODUCTO
    # ==============================

    def registrar_producto(
        self,
        nombre,
        codigo,
        precio,
        stock_minimo,
        id_categoria=None,
        id_proveedor=None,
        cantidad_inicial=0,
        ubicacion=""
    ):
        """
        Esta función registra un nuevo producto en la base de datos.

        También crea su registro inicial en la tabla inventario.

        Parámetros:
        nombre: Nombre del producto.
        codigo: Código único del producto.
        precio: Precio de venta.
        stock_minimo: Cantidad mínima antes de generar alerta.
        id_categoria: Categoría del producto.
        id_proveedor: Proveedor del producto.
        cantidad_inicial: Cantidad inicial en inventario.
        ubicacion: Lugar donde se encuentra el producto.
        """

        # Validamos que los campos principales no estén vacíos.
        if nombre == "" or codigo == "":
            return False, "El nombre y el código son obligatorios."

        # Validamos que el precio sea mayor a cero.
        if precio <= 0:
            return False, "El precio debe ser mayor a cero."

        # Validamos que el stock mínimo no sea negativo.
        if stock_minimo < 0:
            return False, "El stock mínimo no puede ser negativo."

        # Validamos que la cantidad inicial no sea negativa.
        if cantidad_inicial < 0:
            return False, "La cantidad inicial no puede ser negativa."

        try:
            # Abrimos conexión con la base de datos.
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Insertamos el producto en la tabla producto.
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

            # Obtenemos el id del producto recién registrado.
            id_producto = cursor.lastrowid

            # Creamos el registro de inventario para ese producto.
            cursor.execute("""
                INSERT INTO inventario (
                    id_producto,
                    cantidad_actual,
                    ubicacion
                )
                VALUES (?, ?, ?)
            """, (
                id_producto,
                cantidad_inicial,
                ubicacion
            ))

            # Guardamos los cambios.
            conexion.commit()

            # Cerramos la conexión.
            conexion.close()

            return True, "Producto registrado correctamente."

        except sqlite3.IntegrityError:
            # Este error ocurre si el código del producto ya existe.
            return False, "El código del producto ya existe."

        except sqlite3.Error as error:
            # Este error muestra cualquier otro problema de SQLite.
            return False, f"Error al registrar producto: {error}"

    # ==============================
    # LISTAR PRODUCTOS
    # ==============================

    def listar_productos(self):
        """
        Esta función consulta todos los productos registrados.

        También muestra la cantidad actual del inventario.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Consultamos los productos junto con su inventario.
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

            productos = cursor.fetchall()

            conexion.close()

            return productos

        except sqlite3.Error as error:
            print("Error al listar productos:", error)
            return []

    # ==============================
    # BUSCAR PRODUCTO POR CÓDIGO
    # ==============================

    def buscar_por_codigo(self, codigo):
        """
        Esta función busca un producto usando su código.

        Parámetro:
        codigo: Código único del producto.
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
                WHERE p.codigo = ?
            """, (codigo,))

            producto = cursor.fetchone()

            conexion.close()

            return producto

        except sqlite3.Error as error:
            print("Error al buscar producto:", error)
            return None

    # ==============================
    # ACTUALIZAR PRODUCTO
    # ==============================

    def actualizar_producto(
        self,
        id_producto,
        nombre,
        codigo,
        precio,
        stock_minimo,
        id_categoria=None,
        id_proveedor=None
    ):
        """
        Esta función actualiza los datos principales de un producto.

        No modifica la cantidad del inventario.
        La cantidad se maneja desde el módulo de inventario.
        """

        if nombre == "" or codigo == "":
            return False, "El nombre y el código son obligatorios."

        if precio <= 0:
            return False, "El precio debe ser mayor a cero."

        if stock_minimo < 0:
            return False, "El stock mínimo no puede ser negativo."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE producto
                SET
                    nombre = ?,
                    codigo = ?,
                    precio = ?,
                    stock_minimo = ?,
                    id_categoria = ?,
                    id_proveedor = ?
                WHERE id_producto = ?
            """, (
                nombre,
                codigo,
                precio,
                stock_minimo,
                id_categoria,
                id_proveedor,
                id_producto
            ))

            conexion.commit()
            conexion.close()

            return True, "Producto actualizado correctamente."

        except sqlite3.IntegrityError:
            return False, "El código del producto ya existe."

        except sqlite3.Error as error:
            return False, f"Error al actualizar producto: {error}"

    # ==============================
    # ELIMINAR PRODUCTO
    # ==============================

    def eliminar_producto(self, id_producto):
        """
        Esta función elimina un producto de la base de datos.

        Primero elimina su inventario y alertas relacionadas,
        después elimina el producto.

        Nota:
        En un sistema real, no siempre se eliminan productos con ventas,
        pero para esta tarea escolar se deja de forma sencilla.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Eliminamos alertas relacionadas con el producto.
            cursor.execute("""
                DELETE FROM alerta
                WHERE id_producto = ?
            """, (id_producto,))

            # Eliminamos el registro de inventario relacionado.
            cursor.execute("""
                DELETE FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            # Eliminamos el producto.
            cursor.execute("""
                DELETE FROM producto
                WHERE id_producto = ?
            """, (id_producto,))

            conexion.commit()
            conexion.close()

            return True, "Producto eliminado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar producto: {error}"

    # ==============================
    # ACTUALIZAR INVENTARIO DEL PRODUCTO
    # ==============================

    def actualizar_inventario(self, id_producto, nueva_cantidad, nueva_ubicacion=""):
        """
        Esta función actualiza la cantidad y ubicación de un producto.

        Parámetros:
        id_producto: Producto al que pertenece el inventario.
        nueva_cantidad: Nueva cantidad disponible.
        nueva_ubicacion: Nueva ubicación del producto.
        """

        if nueva_cantidad < 0:
            return False, "La cantidad no puede ser negativa."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE inventario
                SET
                    cantidad_actual = ?,
                    ubicacion = ?
                WHERE id_producto = ?
            """, (
                nueva_cantidad,
                nueva_ubicacion,
                id_producto
            ))

            conexion.commit()
            conexion.close()

            return True, "Inventario actualizado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al actualizar inventario: {error}"


# ==============================
# PRUEBA DEL CONTROLADOR
# ==============================

# Esta parte solo se ejecuta si abrimos este archivo directamente.
# Sirve para comprobar que el controller funciona.
if __name__ == "__main__":

    # Creamos un objeto del controlador.
    controlador = ProductoController()

    # Registramos un producto de prueba.
    resultado, mensaje = controlador.registrar_producto(
        nombre="Cuaderno profesional",
        codigo="CUA001",
        precio=45.50,
        stock_minimo=10,
        cantidad_inicial=25,
        ubicacion="Estante A1"
    )

    print(mensaje)

    # Mostramos todos los productos registrados.
    productos = controlador.listar_productos()

    print("Lista de productos:")
    for producto in productos:
        print(producto)