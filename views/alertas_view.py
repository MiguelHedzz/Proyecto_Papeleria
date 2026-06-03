# ==============================
# VISTA DE ALERTAS
# ==============================

"""
Vista para probar alertas de stock bajo.

Permite:
- Generar alertas para productos con stock bajo.
- Ver alertas pendientes.
- Marcar alertas como atendidas.

Ejecutar:
python -m views.alertas_view
"""

import os
import sys
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from database.conexion import conectar_bd


class VentanaAlertas(tk.Toplevel):
    """
    Ventana de alertas de inventario.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Alertas de Stock")
        self.geometry("950x600")
        self.minsize(850, 550)
        self.configure(bg="#ecf0f1")

        self.id_alerta_seleccionada = None

        self.crear_interfaz()
        self.cargar_alertas()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            contenedor,
            text="Alertas de Stock",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(contenedor, bg="white", padx=20, pady=20)
        card.pack(fill="both", expand=True)

        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(frame_botones, "Generar alertas", "#e67e22", self.generar_alertas_stock_bajo).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Marcar atendida", "#27ae60", self.marcar_atendida).pack(side="left", padx=(0, 10))
        self.crear_boton(frame_botones, "Actualizar", "#34495e", self.cargar_alertas).pack(side="left", padx=(0, 10))

        frame_tabla = tk.LabelFrame(
            card,
            text="Alertas registradas",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "producto", "mensaje", "atendida")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=14)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("mensaje", text="Mensaje")
        self.tabla.heading("atendida", text="Atendida")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("producto", width=240)
        self.tabla.column("mensaje", width=420)
        self.tabla.column("atendida", width=120, anchor="center")

        self.tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_alerta)

    def crear_boton(self, parent, texto, color, comando):
        return tk.Button(
            parent,
            text=texto,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=comando
        )

    def cargar_alertas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    a.id_alerta,
                    p.nombre,
                    a.mensaje,
                    CASE WHEN a.atendida = 1 THEN 'Sí' ELSE 'No' END
                FROM alerta a
                INNER JOIN producto p ON a.id_producto = p.id_producto
                ORDER BY a.atendida ASC, a.id_alerta DESC
            """)

            alertas = cursor.fetchall()
            conexion.close()

            for alerta in alertas:
                self.tabla.insert("", "end", values=alerta)

        except sqlite3.Error as error:
            messagebox.showerror("Error", f"No se pudieron cargar las alertas.\n\nDetalle: {error}")

    def generar_alertas_stock_bajo(self):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.stock_minimo,
                    IFNULL(i.cantidad_actual, 0)
                FROM producto p
                LEFT JOIN inventario i ON p.id_producto = i.id_producto
                WHERE IFNULL(i.cantidad_actual, 0) <= p.stock_minimo
            """)

            productos = cursor.fetchall()
            generadas = 0

            for id_producto, nombre, stock_minimo, cantidad_actual in productos:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM alerta
                    WHERE id_producto = ? AND atendida = 0
                """, (id_producto,))

                existe = cursor.fetchone()[0]

                if existe == 0:
                    mensaje = f"Stock bajo: {nombre}. Existencia actual: {cantidad_actual}. Stock mínimo: {stock_minimo}."
                    cursor.execute("""
                        INSERT INTO alerta (id_producto, mensaje, atendida)
                        VALUES (?, ?, 0)
                    """, (id_producto, mensaje))
                    generadas += 1

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Alertas", f"Alertas generadas: {generadas}")
            self.cargar_alertas()

        except sqlite3.Error as error:
            messagebox.showerror("Error", f"No se pudieron generar alertas.\n\nDetalle: {error}")

    def seleccionar_alerta(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")
        self.id_alerta_seleccionada = valores[0]

    def marcar_atendida(self):
        if self.id_alerta_seleccionada is None:
            messagebox.showwarning("Aviso", "Selecciona una alerta.")
            return

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE alerta
                SET atendida = 1
                WHERE id_alerta = ?
            """, (self.id_alerta_seleccionada,))

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Alerta marcada como atendida.")
            self.id_alerta_seleccionada = None
            self.cargar_alertas()

        except sqlite3.Error as error:
            messagebox.showerror("Error", f"No se pudo actualizar la alerta.\n\nDetalle: {error}")


def abrir_alertas(parent=None):
    ventana = VentanaAlertas(parent)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaAlertas(root)
    root.mainloop()
