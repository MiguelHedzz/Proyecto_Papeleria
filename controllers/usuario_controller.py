# ==============================
# CONTROLADOR DE USUARIOS
# ==============================

"""
Controlador de usuarios.

Maneja:
- Login.
- Registro de usuarios.
- Listado.
- Actualizacion.
- Activar/desactivar usuarios.
"""

import sqlite3
from database.conexion import conectar_bd
from models.usuario import Usuario


class UsuarioController:
    """
    Controlador para administrar usuarios.
    """

    def validar_login(self, nombre_usuario, password):
        """
        Valida usuario y contrasena.
        Solo permite usuarios activos.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    usuario,
                    password,
                    rol,
                    IFNULL(activo, 1) AS activo
                FROM usuario
                WHERE usuario = ? AND password = ?
            """, (nombre_usuario, password))

            resultado = cursor.fetchone()

            if not resultado:
                return None

            if int(resultado["activo"]) != 1:
                return None

            return Usuario(
                id_usuario=resultado["id_usuario"],
                nombre=resultado["nombre"],
                usuario=resultado["usuario"],
                password=resultado["password"],
                rol=resultado["rol"]
            )

        except sqlite3.Error as error:
            print(f"Error al validar login: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    def registrar_usuario(self, nombre, usuario, password, rol="Vendedor"):
        """
        Registra un usuario nuevo.
        """

        nombre = str(nombre).strip()
        usuario = str(usuario).strip()
        password = str(password).strip()
        rol = str(rol).strip()

        if nombre == "":
            return False, "El nombre es obligatorio."

        if usuario == "":
            return False, "El usuario es obligatorio."

        if password == "":
            return False, "La contrasena es obligatoria."

        if rol == "":
            return False, "El rol es obligatorio."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuario (
                    nombre,
                    usuario,
                    password,
                    rol,
                    activo
                )
                VALUES (?, ?, ?, ?, 1)
            """, (nombre, usuario, password, rol))

            conexion.commit()
            return True, "Usuario registrado correctamente."

        except sqlite3.IntegrityError:
            if conexion:
                conexion.rollback()
            return False, "El nombre de usuario ya existe."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al registrar usuario: {error}"

        finally:
            if conexion:
                conexion.close()

    def listar_usuarios(self):
        """
        Lista usuarios con estado.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    usuario,
                    rol,
                    IFNULL(activo, 1) AS activo
                FROM usuario
                ORDER BY id_usuario ASC
            """)

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error al listar usuarios: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    def buscar_por_id(self, id_usuario):
        """
        Busca usuario por ID.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    usuario,
                    password,
                    rol,
                    IFNULL(activo, 1) AS activo
                FROM usuario
                WHERE id_usuario = ?
            """, (id_usuario,))

            resultado = cursor.fetchone()

            if not resultado:
                return None

            return Usuario(
                id_usuario=resultado["id_usuario"],
                nombre=resultado["nombre"],
                usuario=resultado["usuario"],
                password=resultado["password"],
                rol=resultado["rol"]
            )

        except sqlite3.Error as error:
            print(f"Error al buscar usuario: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    def buscar_por_nombre_usuario(self, nombre_usuario):
        """
        Busca usuario por nombre de acceso.
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    usuario,
                    password,
                    rol,
                    IFNULL(activo, 1) AS activo
                FROM usuario
                WHERE usuario = ?
            """, (nombre_usuario,))

            resultado = cursor.fetchone()

            if not resultado:
                return None

            return Usuario(
                id_usuario=resultado["id_usuario"],
                nombre=resultado["nombre"],
                usuario=resultado["usuario"],
                password=resultado["password"],
                rol=resultado["rol"]
            )

        except sqlite3.Error as error:
            print(f"Error al buscar usuario por nombre: {error}")
            return None

        finally:
            if conexion:
                conexion.close()

    def actualizar_usuario(self, id_usuario, nombre, usuario, rol, nueva_password=None):
        """
        Actualiza datos del usuario.
        Si nueva_password queda vacia, conserva la contrasena actual.
        """

        if id_usuario is None:
            return False, "Debe seleccionar un usuario."

        nombre = str(nombre).strip()
        usuario = str(usuario).strip()
        rol = str(rol).strip()
        nueva_password = "" if nueva_password is None else str(nueva_password).strip()

        if nombre == "":
            return False, "El nombre es obligatorio."

        if usuario == "":
            return False, "El usuario es obligatorio."

        if rol == "":
            return False, "El rol es obligatorio."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            if nueva_password:
                cursor.execute("""
                    UPDATE usuario
                    SET nombre = ?, usuario = ?, password = ?, rol = ?
                    WHERE id_usuario = ?
                """, (nombre, usuario, nueva_password, rol, id_usuario))
            else:
                cursor.execute("""
                    UPDATE usuario
                    SET nombre = ?, usuario = ?, rol = ?
                    WHERE id_usuario = ?
                """, (nombre, usuario, rol, id_usuario))

            conexion.commit()
            return True, "Usuario actualizado correctamente."

        except sqlite3.IntegrityError:
            if conexion:
                conexion.rollback()
            return False, "El nombre de usuario ya existe."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al actualizar usuario: {error}"

        finally:
            if conexion:
                conexion.close()

    def cambiar_estado_usuario(self, id_usuario, activo):
        """
        Activa o desactiva usuario.
        """

        if id_usuario is None:
            return False, "Debe seleccionar un usuario."

        if int(id_usuario) == 1 and int(activo) == 0:
            return False, "No se puede desactivar el usuario administrador principal."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE usuario
                SET activo = ?
                WHERE id_usuario = ?
            """, (activo, id_usuario))

            conexion.commit()

            if int(activo) == 1:
                return True, "Usuario activado correctamente."

            return True, "Usuario desactivado correctamente."

        except sqlite3.Error as error:
            if conexion:
                conexion.rollback()
            return False, f"Error al cambiar estado del usuario: {error}"

        finally:
            if conexion:
                conexion.close()

    def desactivar_usuario(self, id_usuario):
        """
        Desactiva usuario.
        """

        return self.cambiar_estado_usuario(id_usuario, 0)

    def activar_usuario(self, id_usuario):
        """
        Activa usuario.
        """

        return self.cambiar_estado_usuario(id_usuario, 1)

    def eliminar_usuario(self, id_usuario):
        """
        Para no perder historial, aqui se desactiva en lugar de borrar.
        """

        return self.desactivar_usuario(id_usuario)
