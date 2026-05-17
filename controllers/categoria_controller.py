# ==============================
# CONTROLADOR DE CATEGORIAS
# ==============================

import sqlite3
from database.conexion import conectar_bd
from models.categoria import Categoria


class CategoriaController:
    """
    Esta clase contiene las funciones principales para manejar categorias.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario registra una categoria, este controller la guarda.
    - Si el usuario busca una categoria, este controller consulta la base de datos.
    - Si el usuario modifica una categoria, este controller actualiza la informacion.
    """

    # ==============================
    # REGISTRAR CATEGORIA
    # ==============================

    def registrar_categoria(self, nombre, descripcion=""):
        """
        Esta funcion registra una nueva categoria en la base de datos.

        Parametros:
        nombre: Nombre de la categoria.
        descripcion: Descripcion breve de la categoria.
        """

        # Validamos que el nombre no este vacio.
        if nombre == "":
            return False, "El nombre de la categoria es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO categoria (nombre, descripcion)
                VALUES (?, ?)
            """, (nombre, descripcion))

            conexion.commit()
            conexion.close()

            return True, "Categoria registrada correctamente."

        except sqlite3.IntegrityError:
            return False, "El nombre de la categoria ya existe."

        except sqlite3.Error as error:
            return False, f"Error al registrar categoria: {error}"

    # ==============================
    # LISTAR CATEGORIAS
    # ==============================

    def listar_categorias(self):
        """
        Esta funcion consulta todas las categorias registradas.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_categoria, nombre, descripcion
                FROM categoria
                ORDER BY nombre ASC
            """)

            categorias = cursor.fetchall()
            conexion.close()

            return categorias

        except sqlite3.Error as error:
            print("Error al listar categorias:", error)
            return []

    # ==============================
    # BUSCAR CATEGORIA POR ID
    # ==============================

    def buscar_por_id(self, id_categoria):
        """
        Esta funcion busca una categoria usando su identificador.

        Parametro:
        id_categoria: Identificador de la categoria.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_categoria, nombre, descripcion
                FROM categoria
                WHERE id_categoria = ?
            """, (id_categoria,))

            categoria = cursor.fetchone()
            conexion.close()

            if categoria:
                return Categoria(
                    id_categoria=categoria[0],
                    nombre=categoria[1],
                    descripcion=categoria[2]
                )

            return None

        except sqlite3.Error as error:
            print("Error al buscar categoria:", error)
            return None

    # ==============================
    # BUSCAR CATEGORIA POR NOMBRE
    # ==============================

    def buscar_por_nombre(self, nombre):
        """
        Esta funcion busca una categoria usando su nombre.

        Parametro:
        nombre: Nombre de la categoria.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_categoria, nombre, descripcion
                FROM categoria
                WHERE nombre LIKE ?
            """, (f"%{nombre}%",))

            categorias = cursor.fetchall()
            conexion.close()

            return categorias

        except sqlite3.Error as error:
            print("Error al buscar categoria por nombre:", error)
            return []

    # ==============================
    # ACTUALIZAR CATEGORIA
    # ==============================

    def actualizar_categoria(self, id_categoria, nombre, descripcion=""):
        """
        Esta funcion actualiza los datos de una categoria existente.

        Parametros:
        id_categoria: Identificador de la categoria.
        nombre: Nuevo nombre de la categoria.
        descripcion: Nueva descripcion de la categoria.
        """

        if nombre == "":
            return False, "El nombre de la categoria es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE categoria
                SET nombre = ?, descripcion = ?
                WHERE id_categoria = ?
            """, (nombre, descripcion, id_categoria))

            conexion.commit()
            conexion.close()

            return True, "Categoria actualizada correctamente."

        except sqlite3.IntegrityError:
            return False, "El nombre de la categoria ya existe."

        except sqlite3.Error as error:
            return False, f"Error al actualizar categoria: {error}"

    # ==============================
    # ELIMINAR CATEGORIA
    # ==============================

    def eliminar_categoria(self, id_categoria):
        """
        Esta funcion elimina una categoria de la base de datos.

        Nota:
        Primero verifica que no tenga productos asociados.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificamos si hay productos usando esta categoria
            cursor.execute("""
                SELECT COUNT(*) FROM producto
                WHERE id_categoria = ?
            """, (id_categoria,))

            count = cursor.fetchone()[0]

            if count > 0:
                conexion.close()
                return False, f"No se puede eliminar la categoria. Tiene {count} productos asociados."

            # Eliminamos la categoria
            cursor.execute("""
                DELETE FROM categoria
                WHERE id_categoria = ?
            """, (id_categoria,))

            conexion.commit()
            conexion.close()

            return True, "Categoria eliminada correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar categoria: {error}"