
import sqlite3
from database.conexion import conectar_bd
from models.inventario import Inventario


def crear_inventario(inventario):
    """
    Crea un nuevo registro de inventario para un producto.

    Args:
        inventario (Inventario): Objeto Inventario a registrar.

    Returns:
        int: ID del inventario creado.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO inventario (id_producto, cantidad_actual, ubicacion)
        VALUES (?, ?, ?)
    """, (inventario.id_producto, inventario.cantidad_actual, inventario.ubicacion))

    id_inventario = cursor.lastrowid
    conexion.commit()
    conexion.close()

    return id_inventario


def listar_inventario():
    """
    Obtiene todo el inventario con información del producto.

    Returns:
        list: Lista de diccionarios con datos de inventario y producto.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            i.id_inventario,
            i.id_producto,
            p.nombre AS producto,
            p.codigo,
            i.cantidad_actual,
            p.stock_minimo,
            i.ubicacion,
            CASE 
                WHEN i.cantidad_actual <= p.stock_minimo THEN 'Bajo'
                ELSE 'Normal'
            END AS estado_stock
        FROM inventario i
        JOIN producto p ON i.id_producto = p.id_producto
        ORDER BY p.nombre
    """)

    inventario = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return inventario


def buscar_inventario_por_producto(id_producto):
    """
    Busca el registro de inventario de un producto específico.

    Args:
        id_producto (int): ID del producto a buscar.

    Returns:
        dict: Datos del inventario, o None si no existe.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            i.id_inventario,
            i.id_producto,
            p.nombre AS producto,
            p.codigo,
            i.cantidad_actual,
            p.stock_minimo,
            i.ubicacion
        FROM inventario i
        JOIN producto p ON i.id_producto = p.id_producto
        WHERE i.id_producto = ?
    """, (id_producto,))

    row = cursor.fetchone()
    conexion.close()

    return dict(row) if row else None


def actualizar_stock(id_producto, nueva_cantidad):
    """
    Actualiza la cantidad actual en inventario de un producto.

    Args:
        id_producto (int): ID del producto.
        nueva_cantidad (int): Nueva cantidad en stock.

    Returns:
        bool: True si se actualizó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE inventario
        SET cantidad_actual = ?
        WHERE id_producto = ?
    """, (nueva_cantidad, id_producto))

    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()

    return filas_afectadas > 0


def actualizar_ubicacion(id_producto, nueva_ubicacion):
    """
    Actualiza la ubicación física de un producto.

    Args:
        id_producto (int): ID del producto.
        nueva_ubicacion (str): Nueva ubicación.

    Returns:
        bool: True si se actualizó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE inventario
        SET ubicacion = ?
        WHERE id_producto = ?
    """, (nueva_ubicacion, id_producto))

    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()

    return filas_afectadas > 0


def registrar_entrada(id_producto, cantidad, ubicacion=None):
    """
    Registra una entrada de productos al inventario (suma stock).

    Args:
        id_producto (int): ID del producto.
        cantidad (int): Cantidad a agregar.
        ubicacion (str): Nueva ubicación opcional.

    Returns:
        bool: True si se registró correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_inventario, cantidad_actual, ubicacion
        FROM inventario
        WHERE id_producto = ?
    """, (id_producto,))

    row = cursor.fetchone()

    if row:
        nueva_cantidad = row["cantidad_actual"] + cantidad
        ubicacion_final = ubicacion if ubicacion else row["ubicacion"]

        cursor.execute("""
            UPDATE inventario
            SET cantidad_actual = ?, ubicacion = ?
            WHERE id_inventario = ?
        """, (nueva_cantidad, ubicacion_final, row["id_inventario"]))
    else:
        ubicacion_final = ubicacion if ubicacion else "Almacén"
        cursor.execute("""
            INSERT INTO inventario (id_producto, cantidad_actual, ubicacion)
            VALUES (?, ?, ?)
        """, (id_producto, cantidad, ubicacion_final))

    conexion.commit()
    conexion.close()
    return True


def registrar_salida(id_producto, cantidad):
    """
    Registra una salida de productos del inventario (resta stock).

    Args:
        id_producto (int): ID del producto.
        cantidad (int): Cantidad a restar.

    Returns:
        bool: True si se registró correctamente, False si no hay suficiente stock.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_inventario, cantidad_actual
        FROM inventario
        WHERE id_producto = ?
    """, (id_producto,))

    row = cursor.fetchone()

    if not row:
        conexion.close()
        return False

    stock_actual = row["cantidad_actual"]

    if cantidad > stock_actual:
        conexion.close()
        return False

    nueva_cantidad = stock_actual - cantidad

    cursor.execute("""
        UPDATE inventario
        SET cantidad_actual = ?
        WHERE id_inventario = ?
    """, (nueva_cantidad, row["id_inventario"]))

    conexion.commit()
    conexion.close()
    return True


def eliminar_inventario(id_inventario):
    """
    Elimina un registro de inventario.

    Args:
        id_inventario (int): ID del inventario a eliminar.

    Returns:
        bool: True si se eliminó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM inventario WHERE id_inventario = ?", (id_inventario,))

    conexion.commit()
    conexion.close()
    return True


def verificar_stock_bajo():
    """
    Verifica qué productos tienen stock igual o menor al mínimo.

    Returns:
        list: Lista de productos con stock bajo.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            p.id_producto,
            p.nombre,
            p.codigo,
            p.stock_minimo,
            i.cantidad_actual,
            i.ubicacion
        FROM producto p
        JOIN inventario i ON p.id_producto = i.id_producto
        WHERE i.cantidad_actual <= p.stock_minimo
        ORDER BY i.cantidad_actual ASC
    """)

    productos = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return productos