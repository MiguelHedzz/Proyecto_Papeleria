# ==============================
# VISTA DE RESPALDOS
# ==============================

"""
Vista para crear, listar, eliminar y restaurar respaldos de la base de datos.

Permite:
- Ver la ruta de la base de datos principal.
- Crear respaldo en la carpeta por defecto.
- Crear respaldo seleccionando una carpeta.
- Listar respaldos registrados.
- Eliminar un registro de respaldo del historial.
- Restaurar una base de datos desde un archivo .db.

Ejecutar:
python -m views.respaldos_view
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RUTA_PROYECTO not in sys.path:
    sys.path.insert(0, RUTA_PROYECTO)

from controllers.respaldo_controller import RespaldoController


class VentanaRespaldos(tk.Toplevel):
    """
    Ventana para administrar respaldos de la base de datos.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Respaldos del Sistema")
        self.geometry("980x620")
        self.minsize(880, 560)
        self.configure(bg="#ecf0f1")

        self.respaldo_controller = RespaldoController()
        self.id_respaldo_seleccionado = None
        self.ruta_respaldo_seleccionado = None

        self.crear_interfaz()
        self.cargar_respaldos()

    # ==============================
    # INTERFAZ
    # ==============================

    def crear_interfaz(self):
        """
        Crea la interfaz visual.
        """

        contenedor = tk.Frame(self, bg="#ecf0f1")
        contenedor.pack(fill="both", expand=True, padx=25, pady=25)

        titulo = tk.Label(
            contenedor,
            text="Respaldos del Sistema",
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 24, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(
            contenedor,
            bg="white",
            padx=20,
            pady=20
        )
        card.pack(fill="both", expand=True)

        # Información de la base de datos
        frame_info = tk.LabelFrame(
            card,
            text="Base de datos principal",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=12
        )
        frame_info.pack(fill="x", pady=(0, 15))

        ruta_bd = self.respaldo_controller.obtener_ruta_base_datos()

        self.lbl_ruta_bd = tk.Label(
            frame_info,
            text=ruta_bd,
            bg="white",
            fg="#34495e",
            font=("Segoe UI", 10),
            wraplength=850,
            justify="left"
        )
        self.lbl_ruta_bd.pack(anchor="w")

        if self.respaldo_controller.verificar_base_datos():
            estado = "Estado: base de datos encontrada."
            color_estado = "#27ae60"
        else:
            estado = "Estado: no se encontró la base de datos."
            color_estado = "#e74c3c"

        self.lbl_estado_bd = tk.Label(
            frame_info,
            text=estado,
            bg="white",
            fg=color_estado,
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_estado_bd.pack(anchor="w", pady=(8, 0))

        # Botones
        frame_botones = tk.Frame(card, bg="white")
        frame_botones.pack(fill="x", pady=(0, 15))

        self.crear_boton(
            frame_botones,
            "Crear respaldo",
            "#e67e22",
            self.crear_respaldo_default
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_botones,
            "Elegir carpeta",
            "#34495e",
            self.crear_respaldo_en_carpeta
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_botones,
            "Restaurar respaldo",
            "#27ae60",
            self.restaurar_respaldo
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_botones,
            "Eliminar registro",
            "#e74c3c",
            self.eliminar_registro
        ).pack(side="left", padx=(0, 10))

        self.crear_boton(
            frame_botones,
            "Actualizar lista",
            "#95a5a6",
            self.cargar_respaldos
        ).pack(side="left", padx=(0, 10))

        # Tabla
        frame_tabla = tk.LabelFrame(
            card,
            text="Respaldos registrados",
            bg="white",
            fg="#2c3e50",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "fecha", "ruta")

        self.tabla_respaldos = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=13
        )

        self.tabla_respaldos.heading("id", text="ID")
        self.tabla_respaldos.heading("fecha", text="Fecha")
        self.tabla_respaldos.heading("ruta", text="Ruta del archivo")

        self.tabla_respaldos.column("id", width=60, anchor="center")
        self.tabla_respaldos.column("fecha", width=180, anchor="center")
        self.tabla_respaldos.column("ruta", width=620)

        self.tabla_respaldos.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_respaldos.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tabla_respaldos.configure(yscrollcommand=scrollbar.set)
        self.tabla_respaldos.bind("<<TreeviewSelect>>", self.seleccionar_respaldo)

        # Nota
        nota = tk.Label(
            card,
            text=(
                "Nota: eliminar un registro solo borra el historial dentro del sistema. "
                "No borra el archivo físico, a menos que se programe esa opción."
            ),
            bg="white",
            fg="#7f8c8d",
            font=("Segoe UI", 9),
            wraplength=880,
            justify="left"
        )
        nota.pack(anchor="w", pady=(10, 0))

    def crear_boton(self, parent, texto, color, comando):
        """
        Crea un botón estándar.
        """

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

    # ==============================
    # CARGAR RESPALDOS
    # ==============================

    def cargar_respaldos(self):
        """
        Carga la lista de respaldos en la tabla.
        """

        self.id_respaldo_seleccionado = None
        self.ruta_respaldo_seleccionado = None

        for fila in self.tabla_respaldos.get_children():
            self.tabla_respaldos.delete(fila)

        respaldos = self.respaldo_controller.listar_respaldos()

        for respaldo in respaldos:
            try:
                id_respaldo = respaldo["id_respaldo"]
                fecha = respaldo["fecha"]
                ruta_archivo = respaldo["ruta_archivo"]
            except Exception:
                id_respaldo = respaldo[0]
                fecha = respaldo[1]
                ruta_archivo = respaldo[2]

            self.tabla_respaldos.insert(
                "",
                "end",
                values=(
                    id_respaldo,
                    fecha,
                    ruta_archivo
                )
            )

    def seleccionar_respaldo(self, event):
        """
        Guarda el respaldo seleccionado de la tabla.
        """

        seleccion = self.tabla_respaldos.selection()

        if not seleccion:
            return

        valores = self.tabla_respaldos.item(seleccion[0], "values")

        self.id_respaldo_seleccionado = valores[0]
        self.ruta_respaldo_seleccionado = valores[2]

    # ==============================
    # CREAR RESPALDO
    # ==============================

    def crear_respaldo_default(self):
        """
        Crea respaldo en la carpeta por defecto:
        database/respaldos/
        """

        resultado, mensaje = self.respaldo_controller.crear_respaldo()

        if resultado:
            messagebox.showinfo("Respaldo creado", mensaje)
            self.cargar_respaldos()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_respaldo_en_carpeta(self):
        """
        Permite elegir carpeta para guardar el respaldo.
        """

        carpeta = filedialog.askdirectory(
            title="Selecciona la carpeta donde se guardará el respaldo"
        )

        if not carpeta:
            return

        resultado, mensaje = self.respaldo_controller.crear_respaldo(carpeta)

        if resultado:
            messagebox.showinfo("Respaldo creado", mensaje)
            self.cargar_respaldos()
        else:
            messagebox.showerror("Error", mensaje)

    # ==============================
    # ELIMINAR REGISTRO
    # ==============================

    def eliminar_registro(self):
        """
        Elimina el respaldo seleccionado del historial.
        """

        if self.id_respaldo_seleccionado is None:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un respaldo de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este respaldo del historial?"
        )

        if not confirmar:
            return

        resultado, mensaje = self.respaldo_controller.eliminar_respaldo(
            self.id_respaldo_seleccionado,
            eliminar_archivo=False
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_respaldos()
        else:
            messagebox.showerror("Error", mensaje)

    # ==============================
    # RESTAURAR RESPALDO
    # ==============================

    def restaurar_respaldo(self):
        """
        Restaura un respaldo seleccionado.

        Puede restaurar:
        - El respaldo seleccionado de la tabla.
        - Un archivo .db elegido manualmente.
        """

        ruta_a_restaurar = self.ruta_respaldo_seleccionado

        if not ruta_a_restaurar:
            ruta_a_restaurar = filedialog.askopenfilename(
                title="Selecciona un archivo de respaldo",
                filetypes=[
                    ("Base de datos SQLite", "*.db"),
                    ("Todos los archivos", "*.*")
                ]
            )

        if not ruta_a_restaurar:
            return

        confirmar = messagebox.askyesno(
            "Restaurar respaldo",
            (
                "Esta acción reemplazará la base de datos actual por el respaldo seleccionado.\n\n"
                "Antes de restaurar, el sistema intentará crear una copia de la base actual.\n\n"
                "¿Deseas continuar?"
            )
        )

        if not confirmar:
            return

        resultado, mensaje = self.respaldo_controller.restaurar_respaldo(
            ruta_a_restaurar
        )

        if resultado:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_respaldos()
        else:
            messagebox.showerror("Error", mensaje)


def abrir_respaldos(parent=None):
    """
    Abre la ventana de respaldos.
    """

    ventana = VentanaRespaldos(parent)
    ventana.grab_set()
    return ventana


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    VentanaRespaldos(root)
    root.mainloop()
