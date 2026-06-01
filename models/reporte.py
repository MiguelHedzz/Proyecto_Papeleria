"""
Modelo Reporte.
Representa consultas o reportes generados por el sistema.
"""


class Reporte:
    """
    Clase que representa un reporte del sistema.

    Attributes:
        id_reporte (int): Identificador único del reporte.
        tipo (str): Tipo de reporte (inventario, ventas, alertas).
        fecha_generacion (str): Fecha y hora en que se generó el reporte.
        contenido (str): Resumen o contenido del reporte.
    """

    def __init__(self, tipo, fecha_generacion, contenido, id_reporte=None):
        self.id_reporte = id_reporte
        self.tipo = tipo
        self.fecha_generacion = fecha_generacion
        self.contenido = contenido

    def __repr__(self):
        return f"<Reporte {self.tipo} - {self.fecha_generacion}>"

    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        return {
            'id_reporte': self.id_reporte,
            'tipo': self.tipo,
            'fecha_generacion': self.fecha_generacion,
            'contenido': self.contenido
        }