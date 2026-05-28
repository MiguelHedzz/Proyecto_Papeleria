# ==============================
# VALIDACIONES DEL SISTEMA
# ==============================

def campo_vacio(valor):
    """
    Verifica si un campo está vacío.

    Parámetro:
    valor: dato que se quiere validar.

    Retorna:
    True si el campo está vacío.
    False si el campo tiene información.
    """

    if valor is None:
        return True

    if str(valor).strip() == "":
        return True

    return False


def validar_campos_obligatorios(campos):
    """
    Verifica que una lista de campos obligatorios no esté vacía.

    Parámetro:
    campos: diccionario con nombre del campo y valor.

    Ejemplo:
    campos = {
        "nombre": "Cuaderno",
        "codigo": "CUA001",
        "precio": "45.50"
    }

    Retorna:
    True si todos los campos están llenos.
    False si algún campo está vacío.
    """

    for nombre_campo, valor in campos.items():
        if campo_vacio(valor):
            return False, f"El campo '{nombre_campo}' es obligatorio."

    return True, "Todos los campos obligatorios están completos."


def es_numero(valor):
    """
    Verifica si un valor puede convertirse a número.

    Parámetro:
    valor: dato que se quiere validar.

    Retorna:
    True si es número.
    False si no es número.
    """

    try:
        float(valor)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def es_entero(valor):
    """
    Verifica si un valor puede convertirse a número entero.

    Parámetro:
    valor: dato que se quiere validar.

    Retorna:
    True si es entero.
    False si no es entero.
    """

    try:
        int(valor)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def validar_numero_positivo(valor):
    """
    Verifica si un valor es un número mayor que cero.

    Se puede usar para validar precios.

    Parámetro:
    valor: número a validar.

    Retorna:
    True si el número es mayor que cero.
    False si no lo es.
    """

    if not es_numero(valor):
        return False, "El valor debe ser numérico."

    numero = float(valor)

    if numero <= 0:
        return False, "El valor debe ser mayor que cero."

    return True, "Número válido."


def validar_entero_no_negativo(valor):
    """
    Verifica si un valor es un número entero igual o mayor que cero.

    Se puede usar para validar cantidades o stock mínimo.

    Parámetro:
    valor: cantidad a validar.

    Retorna:
    True si es entero y no negativo.
    False si no cumple.
    """

    if not es_entero(valor):
        return False, "El valor debe ser un número entero."

    numero = int(valor)

    if numero < 0:
        return False, "El valor no puede ser negativo."

    return True, "Cantidad válida."


def validar_precio(precio):
    """
    Valida que el precio sea correcto.

    Un precio debe ser numérico y mayor que cero.
    """

    return validar_numero_positivo(precio)


def validar_cantidad(cantidad):
    """
    Valida que una cantidad sea correcta.

    Una cantidad debe ser un número entero y no puede ser negativa.
    """

    return validar_entero_no_negativo(cantidad)


def validar_texto_minimo(texto, minimo=3):
    """
    Valida que un texto tenga una cantidad mínima de caracteres.

    Parámetros:
    texto: texto a validar.
    minimo: cantidad mínima de caracteres permitida.

    Retorna:
    True si el texto cumple.
    False si no cumple.
    """

    if campo_vacio(texto):
        return False, "El texto no puede estar vacío."

    if len(str(texto).strip()) < minimo:
        return False, f"El texto debe tener al menos {minimo} caracteres."

    return True, "Texto válido."


def validar_correo(correo):
    """
    Valida de forma sencilla un correo electrónico.

    Esta validación es básica para un proyecto escolar.
    Revisa que tenga arroba y punto.
    """

    if campo_vacio(correo):
        return True, "Correo vacío permitido."

    correo = str(correo).strip()

    if "@" not in correo or "." not in correo:
        return False, "El correo no tiene un formato válido."

    return True, "Correo válido."