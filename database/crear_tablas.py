# ==============================
# CREACIÓN DE TABLAS
# ==============================

"""
Este archivo se encarga de crear todas las tablas necesarias
para el funcionamiento del sistema de inventario.

Si las tablas ya existen, no las vuelve a crear.
Esto se logra usando CREATE TABLE IF NOT EXISTS.

También verifica que la tabla 'venta' tenga la columna 'metodo_pago'
y que la tabla 'respaldo' exista.
"""

from .conexion import conectar_bd


def crear_tablas():
    """
    Esta función crea todas las tablas necesarias para el sistema.

    Tablas creadas:
    - usuario: Almacena los usuarios del sistema
    - categoria: Clasifica los productos
    - proveedor: Almacena información de proveedores
    - producto: Información principal de cada producto
    - inventario: Controla la cantidad actual y ubicación de productos
    - venta: Registra las ventas realizadas
    - detalle_venta: Guarda los productos incluidos en cada venta
    - alerta: Registra alertas de stock bajo
    - respaldo: Guarda el historial de copias de seguridad

    También inserta un usuario administrador por defecto:
    - Usuario: admin
    - Contraseña: admin123
    """

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
            rol TEXT NOT NULL
        )
    """)

    # ==============================
    # TABLA CATEGORÍA
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
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
            stock_minimo INTEGER NOT NULL,
            id_categoria INTEGER,
            id_proveedor INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
            FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
        )
    """)

    # ==============================
    # TABLA INVENTARIO
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            cantidad_actual INTEGER NOT NULL,
            ubicacion TEXT,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    # ==============================
    # TABLA VENTA
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            id_usuario INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
    """)

    # ==============================
    # TABLA DETALLE DE VENTA
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
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
            atendida INTEGER DEFAULT 0,
            FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
        )
    """)

    # ==============================
    # TABLA RESPALDO
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respaldo (
            id_respaldo INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            ruta_archivo TEXT NOT NULL
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
            rol
        )
        VALUES (
            1,
            'Administrador',
            'admin',
            'admin123',
            'Administrador'
        )
    """)

    # ==============================
    # AGREGAR COLUMNA MÉTODO DE PAGO (SI NO EXISTE)
    # ==============================

    cursor.execute("PRAGMA table_info(venta)")
    columnas = [col[1] for col in cursor.fetchall()]

    if 'metodo_pago' not in columnas:
        cursor.execute("ALTER TABLE venta ADD COLUMN metodo_pago TEXT DEFAULT 'Efectivo'")
        print("✅ Columna 'metodo_pago' agregada a la tabla venta")

    # ==============================
    # GUARDAR CAMBIOS Y CERRAR
    # ==============================

    conexion.commit()
    conexion.close()

    print("✅ Tablas creadas/verificadas correctamente.")


if __name__ == "__main__":
    crear_tablas()