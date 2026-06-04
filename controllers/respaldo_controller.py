# ==============================
# CONTROLADOR DE RESPALDOS
# ==============================

"""
Este controlador maneja las copias de seguridad de la base de datos.

Funciones principales:
- Verificar que exista la base de datos.
- Crear respaldo físico del archivo inventario.db.
- Registrar el respaldo en la tabla respaldo.
- Listar respaldos registrados.
- Eliminar registros de respaldo del historial.
- Restaurar una copia de seguridad.

La base de datos real se toma desde:
database/conexion.py
"""

import os
import shutil
import sqlite3
from datetime import datetime

from database.conexion import conectar_bd, RUTA_BD


class RespaldoController:
    """
    Controlador para manejar respaldos del sistema.
    """

    # ==============================
    # VERIFICAR BASE DE DATOS
    # ==============================

    def verificar_base_datos(self):
        """
        Verifica si existe la base de datos principal.

        Retorna:
            bool
        """

        return os.path.exists(RUTA_BD)

    # ==============================
    # CREAR RESPALDO
    # ==============================

    def crear_respaldo(self, directorio_destino=None):
        """
        Crea una copia física de la base de datos.

        Parámetro:
            directorio_destino:
                Carpeta donde se guardará el respaldo.
                Si no se manda una carpeta, se crea una carpeta llamada respaldos
                dentro de database/.

        Retorna:
            tuple: (bool, mensaje)
        """

        conexion = None

        try:
            if not self.verificar_base_datos():
                return False, f"No se encontró la base de datos:\n{RUTA_BD}"

            # Si no se selecciona carpeta, se usa database/respaldos.
            if directorio_destino is None or str(directorio_destino).strip() == "":
                directorio_destino = os.path.join(
                    os.path.dirname(RUTA_BD),
                    "respaldos"
                )

            os.makedirs(directorio_destino, exist_ok=True)

            fecha_actual = datetime.now()
            fecha_archivo = fecha_actual.strftime("%Y%m%d_%H%M%S")
            fecha_bd = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

            nombre_respaldo = f"respaldo_inventario_{fecha_archivo}.db"
            ruta_respaldo = os.path.join(directorio_destino, nombre_respaldo)

            # Copia física de la base de datos.
            shutil.copy2(RUTA_BD, ruta_respaldo)

            # Guardar registro en la tabla respaldo.
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO respaldo (
                    fecha,
                    ruta_archivo
                )
                VALUES (?, ?)
            """, (
                fecha_bd,
                ruta_respaldo
            ))

            conexion.commit()

            return True, f"Respaldo creado correctamente:\n{ruta_respaldo}"

        except Exception as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al crear respaldo: {error}"

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # LISTAR RESPALDOS
    # ==============================

    def listar_respaldos(self):
        """
        Lista los respaldos registrados.

        Retorna:
            list
        """

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_respaldo,
                    fecha,
                    ruta_archivo
                FROM respaldo
                ORDER BY fecha DESC
            """)

            respaldos = cursor.fetchall()

            return respaldos

        except sqlite3.Error as error:
            print(f"Error al listar respaldos: {error}")
            return []

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # ELIMINAR REGISTRO DE RESPALDO
    # ==============================

    def eliminar_respaldo(self, id_respaldo, eliminar_archivo=False):
        """
        Elimina un respaldo del historial.

        Parámetros:
            id_respaldo:
                ID del respaldo en la base de datos.

            eliminar_archivo:
                Si es True, también intenta eliminar el archivo físico.
                Si es False, solo elimina el registro de la tabla respaldo.

        Retorna:
            tuple: (bool, mensaje)
        """

        if id_respaldo is None:
            return False, "Debes seleccionar un respaldo."

        conexion = None

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT ruta_archivo
                FROM respaldo
                WHERE id_respaldo = ?
            """, (id_respaldo,))

            respaldo = cursor.fetchone()

            if not respaldo:
                return False, "No se encontró el respaldo seleccionado."

            ruta_archivo = respaldo["ruta_archivo"]

            cursor.execute("""
                DELETE FROM respaldo
                WHERE id_respaldo = ?
            """, (id_respaldo,))

            conexion.commit()

            if eliminar_archivo and ruta_archivo and os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)

            return True, "Respaldo eliminado del historial correctamente."

        except Exception as error:
            if conexion:
                conexion.rollback()

            return False, f"Error al eliminar respaldo: {error}"

        finally:
            if conexion:
                conexion.close()

    # ==============================
    # RESTAURAR RESPALDO
    # ==============================

    def restaurar_respaldo(self, ruta_respaldo):
        """
        Restaura una base de datos desde un archivo de respaldo.

        Advertencia:
        Esta función reemplaza la base de datos actual por la copia seleccionada.

        Retorna:
            tuple: (bool, mensaje)
        """

        try:
            if not ruta_respaldo or str(ruta_respaldo).strip() == "":
                return False, "Debes seleccionar un archivo de respaldo."

            if not os.path.exists(ruta_respaldo):
                return False, "El archivo de respaldo no existe."

            if not ruta_respaldo.endswith(".db"):
                return False, "El archivo seleccionado debe ser una base de datos .db."

            # Crear copia de seguridad de la base actual antes de restaurar.
            if os.path.exists(RUTA_BD):
                carpeta_seguridad = os.path.join(
                    os.path.dirname(RUTA_BD),
                    "respaldos"
                )
                os.makedirs(carpeta_seguridad, exist_ok=True)

                fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
                copia_actual = os.path.join(
                    carpeta_seguridad,
                    f"copia_antes_restaurar_{fecha_archivo}.db"
                )

                shutil.copy2(RUTA_BD, copia_actual)

            # Reemplazar base actual.
            shutil.copy2(ruta_respaldo, RUTA_BD)

            return True, "Base de datos restaurada correctamente."

        except Exception as error:
            return False, f"Error al restaurar respaldo: {error}"

    # ==============================
    # OBTENER RUTA DE BASE DE DATOS
    # ==============================

    def obtener_ruta_base_datos(self):
        """
        Devuelve la ruta de la base de datos principal.
        """

        return RUTA_BD


# ============================================================
# FUNCIONES DE COMPATIBILIDAD
# ============================================================

def crear_respaldo(directorio_destino=None):
    return RespaldoController().crear_respaldo(directorio_destino)


def listar_respaldos():
    return RespaldoController().listar_respaldos()


def eliminar_respaldo(id_respaldo, eliminar_archivo=False):
    return RespaldoController().eliminar_respaldo(id_respaldo, eliminar_archivo)


def restaurar_respaldo(ruta_respaldo):
    return RespaldoController().restaurar_respaldo(ruta_respaldo)


# ==============================
# PRUEBA DIRECTA
# ==============================

if __name__ == "__main__":
    controlador = RespaldoController()

    print("Ruta de base de datos:")
    print(controlador.obtener_ruta_base_datos())

    if controlador.verificar_base_datos():
        print("La base de datos existe.")
    else:
        print("No se encontró la base de datos.")

    print("\nRespaldos registrados:")
    respaldos = controlador.listar_respaldos()

    if not respaldos:
        print("No hay respaldos registrados.")
    else:
        for respaldo in respaldos:
            print(tuple(respaldo))