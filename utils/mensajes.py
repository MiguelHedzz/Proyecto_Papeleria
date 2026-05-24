# Importamos messagebox desde tkinter.
# Este módulo permite mostrar ventanas emergentes con mensajes.
from tkinter import messagebox


# ==============================
# MENSAJES DEL SISTEMA
# ==============================

def mostrar_info(titulo, mensaje):
    """
    Muestra un mensaje informativo al usuario.

    Se utiliza cuando una acción se realiza correctamente.

    Ejemplo:
    mostrar_info("Éxito", "Producto registrado correctamente.")
    """

    messagebox.showinfo(titulo, mensaje)


def mostrar_error(titulo, mensaje):
    """
    Muestra un mensaje de error al usuario.

    Se utiliza cuando ocurre un problema en el sistema.

    Ejemplo:
    mostrar_error("Error", "No se pudo registrar el producto.")
    """

    messagebox.showerror(titulo, mensaje)


def mostrar_advertencia(titulo, mensaje):
    """
    Muestra una advertencia al usuario.

    Se utiliza cuando falta información o se necesita prevenir una acción.

    Ejemplo:
    mostrar_advertencia("Campos vacíos", "Debes llenar todos los campos.")
    """

    messagebox.showwarning(titulo, mensaje)


def confirmar_accion(titulo, mensaje):
    """
    Muestra una ventana de confirmación.

    Se utiliza cuando el usuario debe confirmar una acción importante,
    por ejemplo eliminar un producto.

    Retorna:
    True si el usuario selecciona Sí.
    False si el usuario selecciona No.
    """

    respuesta = messagebox.askyesno(titulo, mensaje)
    return respuesta