# ==============================
# MODELO REPORTE (CORREGIDO)
# ==============================

class Reporte:
    """
    Esta clase representa un reporte generado por el sistema.
    """

    def __init__(
        self,
        id_reporte=None,
        nombre="",
        tipo="",
        fecha_generacion="",
        datos=None
    ):
        self.id_reporte = id_reporte
        self.nombre = nombre          # ← ahora se guarda
        self.tipo = tipo              # ← ahora se guarda
        self.fecha_generacion = fecha_generacion
        self.datos = datos if datos is not None else []

    def mostrar_informacion(self):
        return {
            "id_reporte": self.id_reporte,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "fecha_generacion": self.fecha_generacion,
            "total_registros": len(self.datos) if self.datos else 0
        }

    def validar_datos(self):
        if self.nombre == "":
            return False
        if self.tipo == "":
            return False
        if self.fecha_generacion == "":
            return False
        return True

    def agregar_datos(self, nuevos_datos):
        if isinstance(nuevos_datos, list):
            self.datos.extend(nuevos_datos)
        else:
            self.datos.append(nuevos_datos)
        return True

    def exportar_texto(self):
        lineas = []
        lineas.append("=" * 60)
        lineas.append(f"REPORTE: {self.nombre}")
        lineas.append(f"Tipo: {self.tipo}")
        lineas.append(f"Generado: {self.fecha_generacion}")
        lineas.append(f"Total registros: {len(self.datos)}")
        lineas.append("=" * 60)
        lineas.append("")
        if not self.datos:
            lineas.append("No hay datos para mostrar.")
        else:
            for i, registro in enumerate(self.datos[:10], 1):
                lineas.append(f"{i}. {registro}")
            if len(self.datos) > 10:
                lineas.append(f"... y {len(self.datos) - 10} registros más.")
        lineas.append("")
        lineas.append("=" * 60)
        return "\n".join(lineas)

    def exportar_csv(self, ruta_archivo):
        import csv
        if not self.datos:
            return False
        columnas = set()
        for registro in self.datos:
            columnas.update(registro.keys())
        columnas = sorted(list(columnas))
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(self.datos)
        return True