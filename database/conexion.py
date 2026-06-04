# ==============================
# CONEXIÓN A LA BASE DE DATOS
# ==============================

"""
Este archivo centraliza la conexión a SQLite.

Debe tener la variable RUTA_BD porque otros archivos la importan así:

from database.conexion import conectar_bd, RUTA_BD

La base de datos del proyecto se guarda en:
Proyecto_Papeleria/database/inventario.db
"""

import os
import sqlite3


# Ruta de la carpeta database/
RUTA_DATABASE = os.path.dirname(os.path.abspath(__file__))

# Ruta oficial de la base de datos del sistema.
RUTA_BD = os.path.join(RUTA_DATABASE, "inventario.db")


def conectar_bd():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    """

    conexion = sqlite3.connect(
        RUTA_BD,
        timeout=10
    )

    # Permite leer columnas por nombre:
    # fila["nombre_columna"]
    conexion.row_factory = sqlite3.Row

    # Activa relaciones entre tablas.
    conexion.execute("PRAGMA foreign_keys = ON")

    # Espera hasta 10 segundos si la base está ocupada.
    conexion.execute("PRAGMA busy_timeout = 10000")

    return conexion


def probar_conexion():
    """
    Prueba rápida de conexión.
    """

    try:
        conexion = conectar_bd()
        print("Conexión exitosa a la base de datos.")
        print("Ruta de la base de datos:", RUTA_BD)
        conexion.close()

    except sqlite3.Error as error:
        print("Error al conectar con la base de datos:", error)


if __name__ == "__main__":
    probar_conexion()
