"""
Servicio de Autenticación.
Maneja la lógica de inicio de sesión, registro y validación de usuarios.
"""

from database.conexion import conectar_bd
from models.usuario import Usuario


def validar_login(usuario, password):
    """
    Valida las credenciales de un usuario.

    Args:
        usuario (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Returns:
        dict: Datos del usuario si las credenciales son válidas, None si no.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_usuario, nombre, usuario, rol
        FROM usuario
        WHERE usuario = ? AND password = ?
    """, (usuario, password))

    row = cursor.fetchone()
    conexion.close()

    return dict(row) if row else None


def registrar_usuario(usuario_obj):
    """
    Registra un nuevo usuario en el sistema.

    Args:
        usuario_obj (Usuario): Objeto Usuario con los datos a registrar.

    Returns:
        int: ID del usuario registrado, o None si el usuario ya existe.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuario (nombre, usuario, password, rol)
            VALUES (?, ?, ?, ?)
        """, (usuario_obj.nombre, usuario_obj.usuario,
              usuario_obj.password, usuario_obj.rol))

        id_usuario = cursor.lastrowid
        conexion.commit()
        return id_usuario

    except Exception:
        conexion.rollback()
        return None

    finally:
        conexion.close()


def listar_usuarios():
    """
    Obtiene todos los usuarios registrados.

    Returns:
        list: Lista de diccionarios con los datos de cada usuario.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_usuario, nombre, usuario, rol
        FROM usuario
        ORDER BY nombre
    """)

    usuarios = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    return usuarios


def actualizar_usuario(usuario_obj):
    """
    Actualiza los datos de un usuario existente.

    Args:
        usuario_obj (Usuario): Objeto Usuario con datos actualizados.

    Returns:
        bool: True si se actualizó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuario
        SET nombre = ?, usuario = ?, password = ?, rol = ?
        WHERE id_usuario = ?
    """, (usuario_obj.nombre, usuario_obj.usuario,
          usuario_obj.password, usuario_obj.rol,
          usuario_obj.id_usuario))

    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()

    return filas_afectadas > 0


def eliminar_usuario(id_usuario):
    """
    Elimina un usuario del sistema.

    Args:
        id_usuario (int): ID del usuario a eliminar.

    Returns:
        bool: True si se eliminó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
    conexion.commit()
    conexion.close()
    return True