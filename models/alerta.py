# ==============================
# MODELO ALERTA
# ==============================

from database.conexion import conectar_bd

class Alerta:
    """
    Modelo que representa la tabla 'alerta' en la base de datos.
    Se encarga de gestionar las notificaciones cuando los productos 
    llegan a su stock mínimo.
    """

    def __init__(self, id_alerta=None, id_producto=None, mensaje="", atendida=0):
        # Atributos de la clase que coinciden con las columnas de la tabla en SQLite.
        self.id_alerta = id_alerta
        self.id_producto = id_producto
        self.mensaje = mensaje
        self.atendida = atendida

    # ==============================
    # MÉTODO: CREAR ALERTA
    # ==============================
    @staticmethod
    def generar_alerta_stock_bajo(id_producto, mensaje):
        """
        Inserta una nueva alerta en la base de datos cuando un producto tiene poco stock.
        """
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        try:
            # Insertamos la alerta. Por defecto, 'atendida' es 0 (Falso) en la base de datos.
            cursor.execute("""
                INSERT INTO alerta (id_producto, mensaje, atendida)
                VALUES (?, ?, 0)
            """, (id_producto, mensaje))
            
            conexion.commit()
            print(f"Alerta generada para el producto ID {id_producto}.")
        except Exception as e:
            print("Error al generar la alerta:", e)
        finally:
            conexion.close()

    # ==============================
    # MÉTODO: OBTENER ALERTAS PENDIENTES
    # ==============================
    @staticmethod
    def obtener_alertas_pendientes():
        """
        Recupera todas las alertas que aún no han sido leídas o atendidas.
        Hace un JOIN con la tabla 'producto' para traer también el nombre del artículo.
        """
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        # Seleccionamos información cruzando la tabla alerta y producto
        cursor.execute("""
            SELECT a.id_alerta, p.nombre, a.mensaje 
            FROM alerta a
            INNER JOIN producto p ON a.id_producto = p.id_producto
            WHERE a.atendida = 0
        """)
        
        alertas = cursor.fetchall()
        conexion.close()
        
        return alertas

    # ==============================
    # MÉTODO: MARCAR COMO LEÍDA/ATENDIDA
    # ==============================
    @staticmethod
    def marcar_como_leida(id_alerta):
        """
        Actualiza el estado de una alerta en específico para marcarla como solucionada.
        Cambia el valor de 'atendida' de 0 a 1.
        """
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        try:
            cursor.execute("""
                UPDATE alerta
                SET atendida = 1
                WHERE id_alerta = ?
            """, (id_alerta,))
            
            conexion.commit()
            print(f"Alerta ID {id_alerta} marcada como atendida.")
        except Exception as e:
            print("Error al actualizar la alerta:", e)
        finally:
            conexion.close()