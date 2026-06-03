# ==============================
# CONEXIÓN A LA BASE DE DATOS
# ==============================

import sqlite3


def conectar_bd():
    """
    Esta función crea y devuelve una conexión a la base de datos.

    El archivo de base de datos se llama 'inventario.db' y se encuentra
    en la carpeta 'database' del proyecto.

    Si el archivo no existe, SQLite lo crea automáticamente.
    Si ya existe, simplemente se conecta a esa base de datos.
    """

    # Conectamos a la base de datos ubicada en la carpeta database/
    conexion = sqlite3.connect("database/inventario.db")

    # Retornamos la conexión para poder usarla en otros archivos
    return conexion


def probar_conexion():
    """
    Esta función sirve únicamente para comprobar
    que la conexión con la base de datos funciona correctamente.
    """

    try:
        conexion = conectar_bd()
        print("Conexión exitosa a la base de datos.")
        conexion.close()
    except sqlite3.Error as error:
        print("Error al conectar con la base de datos:", error)


if __name__ == "__main__":
    probar_conexion()