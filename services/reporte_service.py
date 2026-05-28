# ==============================
# CONTROLADOR DE PRODUCTOS
# ==============================

"""
Este controlador maneja las operaciones relacionadas con productos.

Permite:
- Registrar productos.
- Listar productos.
- Buscar productos por código.
- Buscar productos por ID.
- Actualizar productos.
- Eliminar productos.
- Crear inventario inicial.
- Actualizar inventario relacionado con el producto.
"""

import sqlite3
from database.conexion import conectar_bd


class ProductoController:
    """
    Controlador de productos.

    Este archivo funciona como puente entre la base de datos
    y las futuras pantallas del sistema.
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
        Registra un nuevo producto en la base de datos.

        También crea su inventario inicial.

        Parámetros:
        nombre: Nombre del producto.
        codigo: Código único del producto.
        precio: Precio de venta.
        stock_minimo: Cantidad mínima antes de alerta.
        id_categoria: Categoría del producto.
        id_proveedor: Proveedor del producto.
        cantidad_inicial: Cantidad inicial en inventario.
        ubicacion: Lugar físico donde se encuentra.
        """

        if nombre == "" or codigo == "":
            return False, "El nombre y el código son obligatorios."

        try:
            precio = float(precio)
            stock_minimo = int(stock_minimo)
            cantidad_inicial = int(cantidad_inicial)
        except ValueError:
            return False, "Precio, stock mínimo y cantidad inicial deben ser numéricos."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if stock_minimo < 0:
            return False, "El stock mínimo no puede ser negativo."

        if cantidad_inicial < 0:
            return False, "La cantidad inicial no puede ser negativa."

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
                cantidad_inicial,
                ubicacion
            ))

            conexion.commit()
            conexion.close()

            return True, "Producto registrado correctamente."

        except sqlite3.IntegrityError:
            return False, "El código del producto ya existe."

        except sqlite3.Error as error:
            return False, f"Error al registrar producto: {error}"

    # ==============================
    # LISTAR PRODUCTOS
    # ==============================

    def listar_productos(self):
        """
        Lista todos los productos registrados.

        Incluye información del inventario si existe.
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
                    p.id_categoria,
                    p.id_proveedor,
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
            print(f"Error al listar productos: {error}")
            return []

    # ==============================
    # OBTENER PRODUCTOS
    # ==============================

    def obtener_productos(self):
        """
        Método alternativo para listar productos.

        Se deja para compatibilidad con otros archivos del proyecto.
        """

        return self.listar_productos()

    # ==============================
    # BUSCAR POR CÓDIGO
    # ==============================

    def buscar_por_codigo(self, codigo):
        """
        Busca un producto por su código.

        Parámetro:
        codigo: Código único del producto.
        """

        if codigo == "":
            return None

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
                    p.id_categoria,
                    p.id_proveedor,
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
            print(f"Error al buscar producto por código: {error}")
            return None

    # ==============================
    # BUSCAR POR ID
    # ==============================

    def buscar_por_id(self, id_producto):
        """
        Busca un producto por su ID.

        Este método es importante porque puede ser usado por ventas,
        inventario, reportes o pantallas del sistema.
        """

        if id_producto is None:
            return None

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
                    p.id_categoria,
                    p.id_proveedor,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion
                FROM producto p
                LEFT JOIN inventario i
                ON p.id_producto = i.id_producto
                WHERE p.id_producto = ?
            """, (id_producto,))

            producto = cursor.fetchone()
            conexion.close()

            return producto

        except sqlite3.Error as error:
            print(f"Error al buscar producto por ID: {error}")
            return None

    # ==============================
    # OBTENER PRODUCTO POR ID
    # ==============================

    def obtener_producto_por_id(self, id_producto):
        """
        Método alternativo para buscar producto por ID.

        Se deja para no romper archivos que usen este nombre.
        """

        return self.buscar_por_id(id_producto)

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
        Actualiza los datos principales de un producto.

        No actualiza cantidad de inventario.
        La cantidad se maneja desde inventario.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        if nombre == "" or codigo == "":
            return False, "El nombre y el código son obligatorios."

        try:
            precio = float(precio)
            stock_minimo = int(stock_minimo)
        except ValueError:
            return False, "Precio y stock mínimo deben ser numéricos."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

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
    # ACTUALIZAR INVENTARIO
    # ==============================

    def actualizar_inventario(self, id_producto, nueva_cantidad, nueva_ubicacion=""):
        """
        Actualiza la cantidad y ubicación del producto en inventario.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            nueva_cantidad = int(nueva_cantidad)
        except ValueError:
            return False, "La cantidad debe ser un número entero."

        if nueva_cantidad < 0:
            return False, "La cantidad no puede ser negativa."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_inventario
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?, ubicacion = ?
                    WHERE id_producto = ?
                """, (
                    nueva_cantidad,
                    nueva_ubicacion,
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
                    nueva_ubicacion
                ))

            conexion.commit()
            conexion.close()

            return True, "Inventario actualizado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al actualizar inventario: {error}"

    # ==============================
    # ELIMINAR PRODUCTO
    # ==============================

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto.

        Primero elimina registros relacionados en alerta e inventario.
        Después elimina el producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM alerta
                WHERE id_producto = ?
            """, (id_producto,))

            cursor.execute("""
                DELETE FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            cursor.execute("""
                DELETE FROM detalle_venta
                WHERE id_producto = ?
            """, (id_producto,))

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
    # BUSCAR PRODUCTOS POR NOMBRE
    # ==============================

    def buscar_por_nombre(self, nombre):
        """
        Busca productos que coincidan parcialmente con el nombre.
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
                WHERE p.nombre LIKE ?
                ORDER BY p.nombre ASC
            """, (f"%{nombre}%",))

            productos = cursor.fetchall()
            conexion.close()

            return productos

        except sqlite3.Error as error:
            print(f"Error al buscar productos por nombre: {error}")
            return []

    # ==============================
    # CONTAR PRODUCTOS
    # ==============================

    def contar_productos(self):
        """
        Cuenta cuántos productos hay registrados.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM producto
            """)

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return resultado[0]

            return 0

        except sqlite3.Error as error:
            print(f"Error al contar productos: {error}")
            return 0


# ==============================
# PRUEBA DEL CONTROLADOR
# ==============================

if __name__ == "__main__":
    controlador = ProductoController()

    print("Productos registrados:")
    productos = controlador.listar_productos()

    for producto in productos:
        print(producto)

    print("Total de productos:", controlador.contar_productos())