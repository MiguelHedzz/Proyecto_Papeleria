# ==============================
# CONTROLADOR DE PRODUCTOS
# ==============================

"""
Controlador de productos.

Maneja:
- Registrar productos.
- Listar productos con inventario, categoria y proveedor.
- Buscar productos.
- Actualizar productos.
- Actualizar inventario relacionado.
- Eliminar productos de forma segura.
"""

import sqlite3
from database.conexion import conectar_bd


class ProductoController:
    """
    Controlador para administrar productos del catalogo.
    """

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
        Registra un producto y crea su inventario inicial.
        """

        nombre = str(nombre).strip()
        codigo = str(codigo).strip()
        ubicacion = str(ubicacion).strip()

        if nombre == "" or codigo == "":
            return False, "El nombre y el codigo son obligatorios."

        try:
            precio = float(precio)
            stock_minimo = int(stock_minimo)
            cantidad_inicial = int(cantidad_inicial)
        except (TypeError, ValueError):
            return False, "Precio, stock minimo y cantidad inicial deben ser numericos."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if stock_minimo < 0:
            return False, "El stock minimo no puede ser negativo."

        if cantidad_inicial < 0:
            return False, "La cantidad inicial no puede ser negativa."

        id_categoria = self.normalizar_id(id_categoria)
        id_proveedor = self.normalizar_id(id_proveedor)

        conexion = None

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
                    id_proveedor,
                    activo
                )
                VALUES (?, ?, ?, ?, ?, ?, 1)
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

            if cantidad_inicial > 0:
                cursor.execute("""
                    INSERT INTO movimiento_inventario (
                        id_producto,
                        tipo_movimiento,
                        cantidad,
                        fecha,
                        id_usuario,
                        motivo
                    )
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP, NULL, ?)
                """, (
                    id_producto,
                    "ENTRADA",
                    cantidad_inicial,
                    "Inventario inicial"
                ))

            conexion.commit()
            return True, "Producto registrado correctamente."

        except sqlite3.IntegrityError:
            if conexion:
                conexion.rollback()
            return False, "El codigo del producto ya existe."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al registrar producto: {error}"

        finally:
            if conexion:
                conexion.close()

    def listar_productos(self, solo_activos=False):
        """
        Lista productos con informacion de inventario, categoria y proveedor.

        Estructura:
        0 id_producto
        1 nombre
        2 codigo
        3 precio
        4 stock_minimo
        5 id_categoria
        6 id_proveedor
        7 cantidad_actual
        8 ubicacion
        9 categoria_nombre
        10 proveedor_nombre
        11 activo
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            filtro = "WHERE p.activo = 1" if solo_activos else ""

            cursor.execute(f"""
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.codigo,
                    p.precio,
                    p.stock_minimo,
                    p.id_categoria,
                    p.id_proveedor,
                    IFNULL(i.cantidad_actual, 0) AS cantidad_actual,
                    IFNULL(i.ubicacion, '') AS ubicacion,
                    IFNULL(c.nombre, '') AS categoria_nombre,
                    IFNULL(pr.nombre, '') AS proveedor_nombre,
                    IFNULL(p.activo, 1) AS activo
                FROM producto p
                LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                LEFT JOIN categoria c
                    ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedor pr
                    ON p.id_proveedor = pr.id_proveedor
                {filtro}
                ORDER BY p.nombre ASC
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error al listar productos: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    def obtener_productos(self):
        """
        Alias para compatibilidad.
        """

        return self.listar_productos()

    def buscar_por_codigo(self, codigo):
        """
        Busca un producto por codigo.
        """

        codigo = str(codigo).strip()

        if codigo == "":
            return None

        conexion = None

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
                    IFNULL(i.ubicacion, '') AS ubicacion,
                    IFNULL(c.nombre, '') AS categoria_nombre,
                    IFNULL(pr.nombre, '') AS proveedor_nombre,
                    IFNULL(p.activo, 1) AS activo
                FROM producto p
                LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                LEFT JOIN categoria c
                    ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedor pr
                    ON p.id_proveedor = pr.id_proveedor
                WHERE p.codigo = ?
            """, (codigo,))

            return cursor.fetchone()

        except sqlite3.Error as error:
            print(f"Error al buscar producto por codigo: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    def buscar_por_id(self, id_producto):
        """
        Busca un producto por ID.
        """

        if id_producto is None:
            return None

        conexion = None

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
                    IFNULL(i.ubicacion, '') AS ubicacion,
                    IFNULL(c.nombre, '') AS categoria_nombre,
                    IFNULL(pr.nombre, '') AS proveedor_nombre,
                    IFNULL(p.activo, 1) AS activo
                FROM producto p
                LEFT JOIN inventario i
                    ON p.id_producto = i.id_producto
                LEFT JOIN categoria c
                    ON p.id_categoria = c.id_categoria
                LEFT JOIN proveedor pr
                    ON p.id_proveedor = pr.id_proveedor
                WHERE p.id_producto = ?
            """, (id_producto,))

            return cursor.fetchone()

        except sqlite3.Error as error:
            print(f"Error al buscar producto por ID: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    def obtener_producto_por_id(self, id_producto):
        """
        Alias para compatibilidad.
        """

        return self.buscar_por_id(id_producto)

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
        Actualiza datos principales de un producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        nombre = str(nombre).strip()
        codigo = str(codigo).strip()

        if nombre == "" or codigo == "":
            return False, "El nombre y el codigo son obligatorios."

        try:
            precio = float(precio)
            stock_minimo = int(stock_minimo)
        except (TypeError, ValueError):
            return False, "Precio y stock minimo deben ser numericos."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if stock_minimo < 0:
            return False, "El stock minimo no puede ser negativo."

        id_categoria = self.normalizar_id(id_categoria)
        id_proveedor = self.normalizar_id(id_proveedor)

        conexion = None

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
            return True, "Producto actualizado correctamente."

        except sqlite3.IntegrityError:
            if conexion:
                conexion.rollback()
            return False, "El codigo del producto ya existe."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al actualizar producto: {error}"

        finally:
            if conexion:
                conexion.close()

    def actualizar_inventario(self, id_producto, nueva_cantidad, nueva_ubicacion=""):
        """
        Actualiza cantidad y ubicacion del inventario de un producto.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        try:
            nueva_cantidad = int(nueva_cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad debe ser numerica."

        if nueva_cantidad < 0:
            return False, "La cantidad no puede ser negativa."

        nueva_ubicacion = str(nueva_ubicacion).strip()
        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT cantidad_actual
                FROM inventario
                WHERE id_producto = ?
            """, (id_producto,))

            inventario = cursor.fetchone()

            if inventario:
                cantidad_anterior = int(inventario["cantidad_actual"])

                cursor.execute("""
                    UPDATE inventario
                    SET cantidad_actual = ?, ubicacion = ?
                    WHERE id_producto = ?
                """, (nueva_cantidad, nueva_ubicacion, id_producto))

                diferencia = nueva_cantidad - cantidad_anterior
                if diferencia != 0:
                    tipo = "ENTRADA" if diferencia > 0 else "SALIDA"
                    cursor.execute("""
                        INSERT INTO movimiento_inventario (
                            id_producto,
                            tipo_movimiento,
                            cantidad,
                            fecha,
                            id_usuario,
                            motivo
                        )
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP, NULL, ?)
                    """, (
                        id_producto,
                        tipo,
                        abs(diferencia),
                        "Ajuste desde productos"
                    ))
            else:
                cursor.execute("""
                    INSERT INTO inventario (
                        id_producto,
                        cantidad_actual,
                        ubicacion
                    )
                    VALUES (?, ?, ?)
                """, (id_producto, nueva_cantidad, nueva_ubicacion))

                if nueva_cantidad > 0:
                    cursor.execute("""
                        INSERT INTO movimiento_inventario (
                            id_producto,
                            tipo_movimiento,
                            cantidad,
                            fecha,
                            id_usuario,
                            motivo
                        )
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP, NULL, ?)
                    """, (
                        id_producto,
                        "ENTRADA",
                        nueva_cantidad,
                        "Inventario creado desde productos"
                    ))

            conexion.commit()
            return True, "Inventario actualizado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al actualizar inventario: {error}"

        finally:
            if conexion:
                conexion.close()

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto solo si no tiene ventas relacionadas.
        """

        if id_producto is None:
            return False, "Debe seleccionar un producto."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM detalle_venta
                WHERE id_producto = ?
            """, (id_producto,))

            ventas = cursor.fetchone()["total"]

            if ventas > 0:
                return False, (
                    "No se puede eliminar este producto porque ya tiene ventas registradas. "
                    "Puedes dejarlo sin uso o cambiar sus datos, pero no borrarlo."
                )

            cursor.execute("DELETE FROM inventario WHERE id_producto = ?", (id_producto,))
            cursor.execute("DELETE FROM alerta WHERE id_producto = ?", (id_producto,))
            cursor.execute("DELETE FROM producto WHERE id_producto = ?", (id_producto,))

            conexion.commit()
            return True, "Producto eliminado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al eliminar producto: {error}"

        finally:
            if conexion:
                conexion.close()

    def desactivar_producto(self, id_producto):
        """
        Marca producto como inactivo.
        """

        return self.cambiar_estado_producto(id_producto, 0)

    def activar_producto(self, id_producto):
        """
        Marca producto como activo.
        """

        return self.cambiar_estado_producto(id_producto, 1)

    def cambiar_estado_producto(self, id_producto, activo):
        """
        Cambia el estado activo/inactivo del producto.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE producto
                SET activo = ?
                WHERE id_producto = ?
            """, (activo, id_producto))

            conexion.commit()
            return True, "Estado del producto actualizado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al cambiar estado del producto: {error}"

        finally:
            if conexion:
                conexion.close()

    def normalizar_id(self, valor):
        """
        Convierte valores vacios en None y valores validos en int.
        """

        if valor is None:
            return None

        if str(valor).strip() == "":
            return None

        try:
            return int(valor)
        except (TypeError, ValueError):
            return None
