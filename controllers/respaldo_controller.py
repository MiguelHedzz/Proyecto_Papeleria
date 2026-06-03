import os
import shutil
from datetime import datetime
import sqlite3
from database.conexion import conectar_bd
from models.respaldo import Respaldo

def crear_respaldo(directorio_destino):
    """
    Crea una copia física del archivo de la base de datos y registra el respaldo.

    Args:
        directorio_destino (str): Carpeta donde el usuario quiere guardar la copia.

    Returns:
        tuple: (bool, str) True y mensaje de éxito, o False y mensaje de error.
    """
    try:
        # 1. Definir la ruta absoluta de la base de datos original (inventario.db)
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_bd_original = os.path.join(ruta_base, "database", "inventario.db")

        if not os.path.exists(ruta_bd_original):
            return False, "No se encontró el archivo de la base de datos original."

        # 2. Generar nombre de archivo con fecha y hora
        fecha_actual = datetime.now()
        fecha_archivo = fecha_actual.strftime("%Y%m%d_%H%M%S")
        fecha_bd = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        
        nombre_archivo = f"respaldo_dunder_mifflin_{fecha_archivo}.db"
        ruta_completa_destino = os.path.join(directorio_destino, nombre_archivo)

        # 3. Copiar el archivo físicamente
        shutil.copy2(ruta_bd_original, ruta_completa_destino)

        # 4. Guardar el registro en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO respaldo (fecha, ruta_archivo)
            VALUES (?, ?)
        """, (fecha_bd, ruta_completa_destino))

        conexion.commit()
        conexion.close()

        return True, f"Respaldo creado exitosamente en:\n{ruta_completa_destino}"

    except Exception as e:
        return False, f"Error al crear el respaldo: {str(e)}"


def listar_respaldos():
    """
    Obtiene todo el historial de respaldos registrados.

    Returns:
        list: Lista de diccionarios con la información de los respaldos.
    """
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

    # Convertimos los resultados a diccionarios
    respaldos = [dict(row) for row in cursor.fetchall()]
    conexion.close()
    
    return respaldos


def eliminar_respaldo(id_respaldo):
    """
    Elimina un registro de respaldo del historial de la base de datos.
    (Nota: No elimina el archivo físico de la computadora).

    Args:
        id_respaldo (int): ID del respaldo a eliminar.

    Returns:
        bool: True si se eliminó correctamente.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM respaldo WHERE id_respaldo = ?", (id_respaldo,))

    filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()

    return filas_afectadas > 0