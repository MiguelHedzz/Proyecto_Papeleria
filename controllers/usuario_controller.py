# ==============================
# CONTROLADOR DE USUARIOS
# ==============================

import sqlite3
from database.conexion import conectar_bd
from models.usuario import Usuario


class UsuarioController:
    """
    Esta clase contiene las funciones principales para manejar usuarios.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario inicia sesion, este controller valida sus credenciales.
    - Si el administrador registra un usuario, este controller lo guarda.
    - Si el administrador modifica un usuario, este controller actualiza la informacion.
    """

    # ==============================
    # VALIDAR LOGIN
    # ==============================

    def validar_login(self, nombre_usuario, password):
        """
        Esta funcion valida las credenciales de un usuario.

        Parametros:
        nombre_usuario: Nombre de usuario ingresado.
        password: Contraseña ingresada.

        Retorna un objeto Usuario si las credenciales son correctas.
        Retorna None si son incorrectas.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, password, rol
                FROM usuario
                WHERE usuario = ? AND password = ?
            """, (nombre_usuario, password))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    usuario=resultado[2],
                    password=resultado[3],
                    rol=resultado[4]
                )

            return None

        except sqlite3.Error as error:
            print("Error al validar login:", error)
            return None

    # ==============================
    # REGISTRAR USUARIO
    # ==============================

    def registrar_usuario(self, nombre, usuario, password, rol):
        """
        Esta funcion registra un nuevo usuario en la base de datos.

        Parametros:
        nombre: Nombre completo del usuario.
        usuario: Nombre de usuario para iniciar sesion.
        password: Contraseña del usuario.
        rol: Rol del usuario (Administrador o Vendedor).
        """

        # Validamos que los campos no esten vacios
        if nombre == "":
            return False, "El nombre es obligatorio."

        if usuario == "":
            return False, "El nombre de usuario es obligatorio."

        if password == "":
            return False, "La contraseña es obligatoria."

        if rol == "":
            return False, "El rol es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuario (nombre, usuario, password, rol)
                VALUES (?, ?, ?, ?)
            """, (nombre, usuario, password, rol))

            conexion.commit()
            id_usuario = cursor.lastrowid
            conexion.close()

            return True, f"Usuario registrado correctamente con ID {id_usuario}."

        except sqlite3.IntegrityError:
            return False, "El nombre de usuario ya existe."

        except sqlite3.Error as error:
            return False, f"Error al registrar usuario: {error}"

    # ==============================
    # LISTAR USUARIOS
    # ==============================

    def listar_usuarios(self):
        """
        Esta funcion consulta todos los usuarios registrados.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, rol
                FROM usuario
                ORDER BY nombre ASC
            """)

            usuarios = cursor.fetchall()
            conexion.close()

            return usuarios

        except sqlite3.Error as error:
            print("Error al listar usuarios:", error)
            return []

    # ==============================
    # BUSCAR USUARIO POR ID
    # ==============================

    def buscar_por_id(self, id_usuario):
        """
        Esta funcion busca un usuario usando su identificador.

        Parametro:
        id_usuario: Identificador del usuario.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, password, rol
                FROM usuario
                WHERE id_usuario = ?
            """, (id_usuario,))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    usuario=resultado[2],
                    password=resultado[3],
                    rol=resultado[4]
                )

            return None

        except sqlite3.Error as error:
            print("Error al buscar usuario:", error)
            return None

    # ==============================
    # BUSCAR USUARIO POR NOMBRE DE USUARIO
    # ==============================

    def buscar_por_nombre_usuario(self, nombre_usuario):
        """
        Esta funcion busca un usuario usando su nombre de usuario.

        Parametro:
        nombre_usuario: Nombre de usuario para login.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_usuario, nombre, usuario, password, rol
                FROM usuario
                WHERE usuario = ?
            """, (nombre_usuario,))

            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                return Usuario(
                    id_usuario=resultado[0],
                    nombre=resultado[1],
                    usuario=resultado[2],
                    password=resultado[3],
                    rol=resultado[4]
                )

            return None

        except sqlite3.Error as error:
            print("Error al buscar usuario por nombre:", error)
            return None

    # ==============================
    # ACTUALIZAR USUARIO
    # ==============================

    def actualizar_usuario(self, id_usuario, nombre, usuario, rol, nueva_password=None):
        """
        Esta funcion actualiza los datos de un usuario existente.

        Parametros:
        id_usuario: Identificador del usuario.
        nombre: Nuevo nombre completo.
        usuario: Nuevo nombre de usuario.
        rol: Nuevo rol.
        nueva_password: Nueva contraseña (opcional, si no se cambia se mantiene la actual).
        """

        if nombre == "":
            return False, "El nombre es obligatorio."

        if usuario == "":
            return False, "El nombre de usuario es obligatorio."

        if rol == "":
            return False, "El rol es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            if nueva_password:
                # Actualizar incluyendo la contraseña
                cursor.execute("""
                    UPDATE usuario
                    SET nombre = ?, usuario = ?, password = ?, rol = ?
                    WHERE id_usuario = ?
                """, (nombre, usuario, nueva_password, rol, id_usuario))
            else:
                # Actualizar sin cambiar la contraseña
                cursor.execute("""
                    UPDATE usuario
                    SET nombre = ?, usuario = ?, rol = ?
                    WHERE id_usuario = ?
                """, (nombre, usuario, rol, id_usuario))

            conexion.commit()
            conexion.close()

            return True, "Usuario actualizado correctamente."

        except sqlite3.IntegrityError:
            return False, "El nombre de usuario ya existe."

        except sqlite3.Error as error:
            return False, f"Error al actualizar usuario: {error}"

    # ==============================
    # ELIMINAR USUARIO
    # ==============================

    def eliminar_usuario(self, id_usuario):
        """
        Esta funcion elimina un usuario de la base de datos.

        Nota:
        No se puede eliminar el usuario administrador principal (id 1).
        """

        if id_usuario == 1:
            return False, "No se puede eliminar el usuario administrador principal."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificamos si el usuario tiene ventas asociadas
            cursor.execute("""
                SELECT COUNT(*) FROM venta
                WHERE id_usuario = ?
            """, (id_usuario,))

            count = cursor.fetchone()[0]

            if count > 0:
                conexion.close()
                return False, f"No se puede eliminar el usuario. Tiene {count} ventas registradas."

            # Eliminamos el usuario
            cursor.execute("""
                DELETE FROM usuario
                WHERE id_usuario = ?
            """, (id_usuario,))

            conexion.commit()
            conexion.close()

            return True, "Usuario eliminado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar usuario: {error}"