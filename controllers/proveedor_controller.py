# ==============================
# CONTROLADOR DE PROVEEDORES
# ==============================

import sqlite3
from database.conexion import conectar_bd
from models.proveedor import Proveedor


class ProveedorController:
    """
    Esta clase contiene las funciones principales para manejar proveedores.

    Un controller sirve como intermediario entre la interfaz del usuario
    y la base de datos.

    Por ejemplo:
    - Si el usuario registra un proveedor, este controller lo guarda.
    - Si el usuario busca un proveedor, este controller consulta la base de datos.
    - Si el usuario modifica un proveedor, este controller actualiza la informacion.
    """

    # ==============================
    # REGISTRAR PROVEEDOR
    # ==============================

    def registrar_proveedor(self, nombre, telefono="", correo="", direccion=""):
        """
        Esta funcion registra un nuevo proveedor en la base de datos.

        Parametros:
        nombre: Nombre del proveedor.
        telefono: Numero telefonico del proveedor.
        correo: Correo electronico del proveedor.
        direccion: Direccion fisica del proveedor.
        """

        # Validamos que el nombre no este vacio.
        if nombre == "":
            return False, "El nombre del proveedor es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO proveedor (nombre, telefono, correo)
                VALUES (?, ?, ?)
            """, (nombre, telefono, correo))

            # Nota: direccion no esta en la tabla de la base de datos,
            # pero la mantenemos en el modelo para futuras expansiones.

            conexion.commit()
            id_proveedor = cursor.lastrowid
            conexion.close()

            return True, f"Proveedor registrado correctamente con ID {id_proveedor}."

        except sqlite3.Error as error:
            return False, f"Error al registrar proveedor: {error}"

    # ==============================
    # LISTAR PROVEEDORES
    # ==============================

    def listar_proveedores(self):
        """
        Esta funcion consulta todos los proveedores registrados.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_proveedor, nombre, telefono, correo
                FROM proveedor
                ORDER BY nombre ASC
            """)

            proveedores = cursor.fetchall()
            conexion.close()

            return proveedores

        except sqlite3.Error as error:
            print("Error al listar proveedores:", error)
            return []

    # ==============================
    # BUSCAR PROVEEDOR POR ID
    # ==============================

    def buscar_por_id(self, id_proveedor):
        """
        Esta funcion busca un proveedor usando su identificador.

        Parametro:
        id_proveedor: Identificador del proveedor.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_proveedor, nombre, telefono, correo
                FROM proveedor
                WHERE id_proveedor = ?
            """, (id_proveedor,))

            proveedor = cursor.fetchone()
            conexion.close()

            if proveedor:
                return Proveedor(
                    id_proveedor=proveedor[0],
                    nombre=proveedor[1],
                    telefono=proveedor[2],
                    correo=proveedor[3],
                    direccion=""
                )

            return None

        except sqlite3.Error as error:
            print("Error al buscar proveedor:", error)
            return None

    # ==============================
    # BUSCAR PROVEEDOR POR NOMBRE
    # ==============================

    def buscar_por_nombre(self, nombre):
        """
        Esta funcion busca proveedores usando su nombre.

        Parametro:
        nombre: Nombre del proveedor (busqueda parcial).
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_proveedor, nombre, telefono, correo
                FROM proveedor
                WHERE nombre LIKE ?
                ORDER BY nombre ASC
            """, (f"%{nombre}%",))

            proveedores = cursor.fetchall()
            conexion.close()

            return proveedores

        except sqlite3.Error as error:
            print("Error al buscar proveedor por nombre:", error)
            return []

    # ==============================
    # ACTUALIZAR PROVEEDOR
    # ==============================

    def actualizar_proveedor(self, id_proveedor, nombre, telefono="", correo=""):
        """
        Esta funcion actualiza los datos de un proveedor existente.

        Parametros:
        id_proveedor: Identificador del proveedor.
        nombre: Nuevo nombre del proveedor.
        telefono: Nuevo telefono del proveedor.
        correo: Nuevo correo del proveedor.
        """

        if nombre == "":
            return False, "El nombre del proveedor es obligatorio."

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE proveedor
                SET nombre = ?, telefono = ?, correo = ?
                WHERE id_proveedor = ?
            """, (nombre, telefono, correo, id_proveedor))

            conexion.commit()
            conexion.close()

            return True, "Proveedor actualizado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al actualizar proveedor: {error}"

    # ==============================
    # ELIMINAR PROVEEDOR
    # ==============================

    def eliminar_proveedor(self, id_proveedor):
        """
        Esta funcion elimina un proveedor de la base de datos.

        Nota:
        Primero verifica que no tenga productos asociados.
        """

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificamos si hay productos usando este proveedor
            cursor.execute("""
                SELECT COUNT(*) FROM producto
                WHERE id_proveedor = ?
            """, (id_proveedor,))

            count = cursor.fetchone()[0]

            if count > 0:
                conexion.close()
                return False, f"No se puede eliminar el proveedor. Tiene {count} productos asociados."

            # Eliminamos el proveedor
            cursor.execute("""
                DELETE FROM proveedor
                WHERE id_proveedor = ?
            """, (id_proveedor,))

            conexion.commit()
            conexion.close()

            return True, "Proveedor eliminado correctamente."

        except sqlite3.Error as error:
            return False, f"Error al eliminar proveedor: {error}"