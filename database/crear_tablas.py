# ==============================
# CREACIÓN DE TABLAS
# ==============================

"""
Este archivo crea las tablas principales del sistema de inventario.

Debe contener la función crear_tablas(), porque main.py la importa así:

from database.crear_tablas import crear_tablas

Tablas:
- usuario
- categoria
- proveedor
- producto
- inventario
- venta
- detalle_venta
- alerta
- respaldo
- movimiento_inventario
"""

import sqlite3

try:
    from .conexion import conectar_bd
except ImportError:
    from database.conexion import conectar_bd


def crear_tablas():
    """
    Crea todas las tablas necesarias del sistema.

    Esta función es llamada desde main.py antes de abrir el login.
    """

    conexion = None

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # ==============================
        # TABLA USUARIO
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rol TEXT NOT NULL,
                activo INTEGER NOT NULL DEFAULT 1
            )
        """)

        # ==============================
        # TABLA CATEGORÍA
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT
            )
        """)

        # ==============================
        # TABLA PROVEEDOR
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proveedor (
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                correo TEXT
            )
        """)

        # ==============================
        # TABLA PRODUCTO
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                codigo TEXT NOT NULL UNIQUE,
                precio REAL NOT NULL,
                stock_minimo INTEGER NOT NULL DEFAULT 0,
                id_categoria INTEGER,
                id_proveedor INTEGER,
                activo INTEGER NOT NULL DEFAULT 1,

                FOREIGN KEY (id_categoria)
                    REFERENCES categoria(id_categoria)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL,

                FOREIGN KEY (id_proveedor)
                    REFERENCES proveedor(id_proveedor)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            )
        """)

        # ==============================
        # TABLA INVENTARIO
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL UNIQUE,
                cantidad_actual INTEGER NOT NULL DEFAULT 0,
                ubicacion TEXT,

                FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
        """)

        # ==============================
        # TABLA VENTA
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS venta (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                metodo_pago TEXT NOT NULL DEFAULT 'Efectivo',
                id_usuario INTEGER NOT NULL,

                FOREIGN KEY (id_usuario)
                    REFERENCES usuario(id_usuario)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        # ==============================
        # TABLA DETALLE_VENTA
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL DEFAULT 0,
                subtotal REAL NOT NULL,

                FOREIGN KEY (id_venta)
                    REFERENCES venta(id_venta)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,

                FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        # ==============================
        # TABLA ALERTA
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerta (
                id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                mensaje TEXT NOT NULL,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atendida INTEGER NOT NULL DEFAULT 0,

                FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
        """)

        # ==============================
        # TABLA RESPALDO
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS respaldo (
                id_respaldo INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ruta_archivo TEXT NOT NULL
            )
        """)

        # ==============================
        # TABLA MOVIMIENTO_INVENTARIO
        # ==============================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimiento_inventario (
                id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                tipo_movimiento TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                id_usuario INTEGER,
                motivo TEXT,

                FOREIGN KEY (id_producto)
                    REFERENCES producto(id_producto)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,

                FOREIGN KEY (id_usuario)
                    REFERENCES usuario(id_usuario)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            )
        """)

        # ==============================
        # USUARIO ADMINISTRADOR POR DEFECTO
        # ==============================
        cursor.execute("""
            INSERT OR IGNORE INTO usuario (
                id_usuario,
                nombre,
                usuario,
                password,
                rol,
                activo
            )
            VALUES (
                1,
                'Administrador',
                'admin',
                'admin123',
                'Administrador',
                1
            )
        """)

        conexion.commit()
        print("Tablas creadas correctamente.")

    except sqlite3.Error as error:
        if conexion:
            conexion.rollback()

        print(f"Error al crear las tablas: {error}")

    finally:
        if conexion:
            conexion.close()


# Alias por si algún archivo anterior intenta llamar inicializar_bd().
def inicializar_bd():
    """
    Alias de compatibilidad.
    """
    crear_tablas()


if __name__ == "__main__":
    crear_tablas()
