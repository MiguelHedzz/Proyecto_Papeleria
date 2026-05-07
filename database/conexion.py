# Importamos sqlite3, que es la librería incluida en Python
# para trabajar con bases de datos SQLite.
import sqlite3


# ==============================
# CONEXIÓN A LA BASE DE DATOS
# ==============================

def conectar_bd():
    """
    Esta función crea y devuelve una conexión a la base de datos.

    Si el archivo 'inventario_papeleria.db' no existe,
    SQLite lo crea automáticamente en la carpeta del proyecto.

    Si ya existe, simplemente se conecta a esa base de datos.
    """

    # Creamos la conexión con la base de datos.
    # El nombre del archivo será inventario_papeleria.db.
    conexion = sqlite3.connect("inventario_papeleria.db")

    # Retornamos la conexión para poder usarla en otros archivos.
    return conexion


# ==============================
# PRUEBA DE CONEXIÓN
# ==============================

def probar_conexion():
    """
    Esta función sirve únicamente para comprobar
    que la conexión con la base de datos funciona correctamente.
    """

    try:
        # Intentamos conectarnos a la base de datos.
        conexion = conectar_bd()

        # Si la conexión fue exitosa, mostramos este mensaje.
        print("Conexión exitosa a la base de datos.")

        # Cerramos la conexión para liberar recursos.
        conexion.close()

    except sqlite3.Error as error:
        # Si ocurre algún error, se muestra en pantalla.
        print("Error al conectar con la base de datos:", error)


# ==============================
# EJECUCIÓN DE PRUEBA
# ==============================

# Esta parte solo se ejecuta si abrimos directamente este archivo.
# No se ejecuta cuando lo importamos desde otro archivo.
if __name__ == "__main__":
    probar_conexion()