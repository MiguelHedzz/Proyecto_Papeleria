# Importamos csv, una librería incluida en Python.
# Sirve para crear archivos CSV que pueden abrirse en Excel.
import csv


# ==============================
# EXPORTACIÓN DE DATOS
# ==============================

def exportar_a_csv(nombre_archivo, encabezados, datos):
    """
    Exporta información a un archivo CSV.

    Parámetros:
    nombre_archivo: nombre del archivo que se va a crear.
    encabezados: lista con los nombres de las columnas.
    datos: lista de registros que se van a exportar.

    Ejemplo:
    encabezados = ["ID", "Nombre", "Código", "Precio"]
    datos = [
        [1, "Cuaderno", "CUA001", 45.50],
        [2, "Lápiz", "LAP001", 8.00]
    ]
    """

    try:
        # Abrimos o creamos el archivo CSV.
        # newline="" evita saltos de línea extra en Windows.
        # encoding="utf-8-sig" ayuda a que Excel lea bien acentos y ñ.
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:
            
            # Creamos el escritor CSV.
            escritor = csv.writer(archivo)

            # Escribimos la primera fila con los encabezados.
            escritor.writerow(encabezados)

            # Escribimos todos los registros.
            escritor.writerows(datos)

        # Si todo sale bien, regresamos True y un mensaje.
        return True, f"Archivo exportado correctamente: {nombre_archivo}"

    except Exception as error:
        # Si ocurre algún error, regresamos False y el mensaje del error.
        return False, f"Error al exportar archivo: {error}"


# ==============================
# EXPORTAR PRODUCTOS
# ==============================

def exportar_productos(nombre_archivo, productos):
    """
    Exporta una lista de productos a CSV.

    Parámetro:
    nombre_archivo: nombre del archivo CSV.
    productos: lista de productos obtenida desde la base de datos.

    Se espera que cada producto tenga datos como:
    id, nombre, código, precio, stock mínimo, cantidad actual y ubicación.
    """

    encabezados = [
        "ID",
        "Nombre",
        "Código",
        "Precio",
        "Stock mínimo",
        "Cantidad actual",
        "Ubicación"
    ]

    return exportar_a_csv(nombre_archivo, encabezados, productos)


# ==============================
# EXPORTAR INVENTARIO
# ==============================

def exportar_inventario(nombre_archivo, inventario):
    """
    Exporta información del inventario a CSV.

    Parámetro:
    inventario: lista de registros de inventario.
    """

    encabezados = [
        "ID Inventario",
        "ID Producto",
        "Producto",
        "Cantidad actual",
        "Ubicación"
    ]

    return exportar_a_csv(nombre_archivo, encabezados, inventario)


# ==============================
# EXPORTAR VENTAS
# ==============================

def exportar_ventas(nombre_archivo, ventas):
    """
    Exporta información de ventas a CSV.

    Parámetro:
    ventas: lista de ventas registradas.
    """

    encabezados = [
        "ID Venta",
        "Fecha",
        "Total",
        "Usuario"
    ]

    return exportar_a_csv(nombre_archivo, encabezados, ventas)


# ==============================
# EXPORTAR ALERTAS
# ==============================

def exportar_alertas(nombre_archivo, alertas):
    """
    Exporta alertas de stock bajo a CSV.

    Parámetro:
    alertas: lista de alertas registradas.
    """

    encabezados = [
        "ID Alerta",
        "ID Producto",
        "Producto",
        "Mensaje",
        "Atendida"
    ]

    return exportar_a_csv(nombre_archivo, encabezados, alertas)


# ==============================
# PRUEBA DEL ARCHIVO
# ==============================

if __name__ == "__main__":
    """
    Esta prueba solo se ejecuta si abrimos directamente este archivo.
    Sirve para revisar que la exportación funcione.
    """

    productos_prueba = [
        [1, "Cuaderno profesional", "CUA001", 45.50, 10, 25, "Estante A1"],
        [2, "Lápiz", "LAP001", 8.00, 20, 100, "Estante B1"]
    ]

    resultado, mensaje = exportar_productos(
        "productos_prueba.csv",
        productos_prueba
    )

    print(mensaje)