# Importamos la función conectar_bd desde el archivo conexion.py.
# Esta función nos permite conectarnos a la base de datos SQLite.
from .conexion import conectar_bd


# ==============================
# CREACIÓN DE TABLAS
# ==============================

def crear_tablas():
    """
    Esta función crea todas las tablas necesarias para el sistema.

    Si las tablas ya existen, no las vuelve a crear.
    Esto se logra usando CREATE TABLE IF NOT EXISTS.
    """

    # Creamos una conexión con la base de datos.
    conexion = conectar_bd()

    # El cursor nos permite ejecutar instrucciones SQL.
    cursor = conexion.cursor()

    # ==============================
    # TABLA USUARIO
    # ==============================

    # Esta tabla guarda los usuarios que pueden entrar al sistema.
    # Por ejemplo: administrador o vendedor.
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

    # Esta tabla guarda las categorías de productos.
    # Ejemplo: útiles escolares, oficina, papelería, etc.
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

    # Esta tabla guarda los proveedores de la papelería.
    # Los proveedores son quienes suministran productos al negocio.
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

    # Esta tabla guarda la información principal de cada producto.
    # Se relaciona con categoria y proveedor mediante llaves foráneas.
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

    # Esta tabla guarda la cantidad disponible de cada producto.
    # Cada registro de inventario se relaciona con un producto.
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

    # Esta tabla guarda las ventas realizadas.
    # Cada venta se relaciona con el usuario que la realizó.
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

    # Esta tabla guarda los productos incluidos en cada venta.
    # Por ejemplo, una venta puede tener varios productos.
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

    # Esta tabla guarda las alertas de productos con stock bajo.
    # Se usa cuando la cantidad disponible llega al stock mínimo.
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
    # USUARIO ADMINISTRADOR POR DEFECTO
    # ==============================

    # Insertamos un usuario administrador inicial.
    # INSERT OR IGNORE evita que se duplique si ya existe.
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

    # Guardamos todos los cambios realizados en la base de datos.
    conexion.commit()

    # Cerramos la conexión para liberar recursos.
    conexion.close()

    # Mostramos un mensaje en consola para confirmar que todo salió bien.
    print("Tablas creadas correctamente.")


# ==============================
# EJECUCIÓN DE PRUEBA
# ==============================

# Esta parte se ejecuta solamente si abrimos directamente este archivo.
# Sirve para probar que las tablas se creen correctamente.
if __name__ == "__main__":
    crear_tablas()