# ==============================
# MODELO REPORTE
# ==============================

class Reporte:
    """
    Esta clase representa un reporte generado por el sistema.

    Los reportes permiten visualizar informacion consolidada
    del inventario, ventas, movimientos y otros aspectos
    importantes para la toma de decisiones.

    Ejemplo:
    - Reporte de inventario actual
    - Reporte de productos mas vendidos
    - Reporte de movimientos (entradas y salidas)
    - Reporte de productos con stock bajo
    """

    def __init__(
        self,
        id_reporte=None,
        nombre="",
        tipo="",
        fecha_generacion="",
        datos=None
    ):
        """
        Este metodo se ejecuta automaticamente cuando se crea un objeto Reporte.

        Parametros:
        id_reporte: Identificador unico del reporte.
        nombre: Nombre descriptivo del reporte.
        tipo: Tipo de reporte (inventario, ventas, movimientos, alertas).
        fecha_generacion: Fecha y hora en que se genero el reporte.
        datos: Contenido del reporte (lista de diccionarios).
        """

        # Guardamos el id del reporte.
        # Puede ser None si todavia no se guarda en la base de datos.
        self.id_reporte = id_reporte

        # Guardamos el nombre del reporte.
        self.nombre = nombre

        # Guardamos el tipo de reporte.
        self.tipo = tipo

        # Guardamos la fecha de generacion del reporte.
        self.fecha_generacion = fecha_generacion

        # Guardamos los datos del reporte.
        # Puede ser una lista de objetos o un diccionario con la informacion.
        self.datos = datos if datos is not None else []

    # ==============================
    # MOSTRAR INFORMACION
    # ==============================

    def mostrar_informacion(self):
        """
        Este metodo devuelve la informacion del reporte
        en forma de diccionario.

        Sirve para mostrar los datos de manera ordenada.
        """

        return {
            "id_reporte": self.id_reporte,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "fecha_generacion": self.fecha_generacion,
            "total_registros": len(self.datos) if self.datos else 0
        }

    # ==============================
    # VALIDAR DATOS
    # ==============================

    def validar_datos(self):
        """
        Este metodo revisa que los datos importantes del reporte
        esten completos.

        Retorna True si los datos son correctos.
        Retorna False si falta algun dato.
        """

        # Validamos que el nombre no este vacio.
        if self.nombre == "":
            return False

        # Validamos que el tipo no este vacio.
        if self.tipo == "":
            return False

        # Validamos que la fecha no este vacia.
        if self.fecha_generacion == "":
            return False

        return True

    # ==============================
    # AGREGAR DATOS
    # ==============================

    def agregar_datos(self, nuevos_datos):
        """
        Este metodo permite agregar informacion al reporte.

        Parametro:
        nuevos_datos: Datos a agregar al reporte (lista o elemento individual).
        """

        if isinstance(nuevos_datos, list):
            self.datos.extend(nuevos_datos)
        else:
            self.datos.append(nuevos_datos)

        return True

    # ==============================
    # GENERAR REPORTE DE INVENTARIO
    # ==============================

    def generar_reporte_inventario(self, productos):
        """
        Este metodo genera un reporte de inventario actual.

        Parametro:
        productos: Lista de productos con su stock actual.

        Retorna el mismo objeto Reporte con los datos cargados.
        """

        self.nombre = "Reporte de Inventario Actual"
        self.tipo = "inventario"
        self.datos = []

        for producto in productos:
            stock_actual = getattr(producto, 'stock_actual', 0)
            self.datos.append({
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "stock_actual": stock_actual,
                "stock_minimo": producto.stock_minimo,
                "estado": "Stock bajo" if stock_actual <= producto.stock_minimo else "Normal"
            })

        return self

    # ==============================
    # GENERAR REPORTE DE STOCK BAJO
    # ==============================

    def generar_reporte_stock_bajo(self, productos):
        """
        Este metodo genera un reporte de productos con stock bajo.

        Parametro:
        productos: Lista de productos con su stock actual.

        Retorna el mismo objeto Reporte con los datos cargados.
        """

        self.nombre = "Reporte de Productos con Stock Bajo"
        self.tipo = "alertas"
        self.datos = []

        for producto in productos:
            stock_actual = getattr(producto, 'stock_actual', 0)
            if stock_actual <= producto.stock_minimo:
                self.datos.append({
                    "codigo": producto.codigo,
                    "nombre": producto.nombre,
                    "stock_actual": stock_actual,
                    "stock_minimo": producto.stock_minimo,
                    "faltante": producto.stock_minimo - stock_actual if stock_actual < producto.stock_minimo else 0
                })

        return self

    # ==============================
    # EXPORTAR A TEXTO
    # ==============================

    def exportar_texto(self):
        """
        Este metodo convierte el reporte a formato texto plano.

        Util para mostrar en consola o guardar en archivo TXT.
        """

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
                lineas.append(f"... y {len(self.datos) - 10} registros mas.")

        lineas.append("")
        lineas.append("=" * 60)

        return "\n".join(lineas)

    # ==============================
    # EXPORTAR A CSV
    # ==============================

    def exportar_csv(self, ruta_archivo):
        """
        Este metodo exporta el reporte a un archivo CSV.

        Parametro:
        ruta_archivo: Ruta donde se guardara el archivo CSV.
        """

        import csv

        if not self.datos:
            return False

        # Obtener todas las columnas posibles
        columnas = set()
        for registro in self.datos:
            columnas.update(registro.keys())
        columnas = sorted(list(columnas))

        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(self.datos)

        return True