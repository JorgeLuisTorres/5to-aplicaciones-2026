import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Configuración global de apariencia y color de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class KioscoVentana(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Configuración básica de la ventana principal
        self.title("Sistema Kiosco - Interfaz ABM")
        self.geometry("980x520")
        self.minsize(820, 450)

        # Layout principal de 2 columnas: formulario a la izquierda, tabla a la derecha
        self.grid_columnconfigure(0, weight=0, minsize=310)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._crear_panel_formulario()
        self._crear_panel_tabla()
        self._configurar_estilo_treeview()

    # Bloque 1: Formulario a la izquierda con 4 campos CTkEntry y 4 botones CTkButton
    def _crear_panel_formulario(self) -> None:
        panel_izq = ctk.CTkFrame(self, corner_radius=12)
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(14, 7), pady=14)
        panel_izq.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            panel_izq,
            text="Gestión de Productos",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        titulo.grid(row=0, column=0, padx=16, pady=(18, 12), sticky="w")

        # Campo 1: Código
        ctk.CTkLabel(panel_izq, text="Código").grid(
            row=1, column=0, padx=16, pady=(6, 2), sticky="w"
        )
        self.entry_codigo = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 7790001")
        self.entry_codigo.grid(row=2, column=0, padx=16, pady=(0, 8), sticky="ew")

        # Campo 2: Nombre
        ctk.CTkLabel(panel_izq, text="Nombre").grid(
            row=3, column=0, padx=16, pady=(6, 2), sticky="w"
        )
        self.entry_nombre = ctk.CTkEntry(panel_izq, placeholder_text="Ej: Alfajor Triple")
        self.entry_nombre.grid(row=4, column=0, padx=16, pady=(0, 8), sticky="ew")

        # Campo 3: Precio
        ctk.CTkLabel(panel_izq, text="Precio").grid(
            row=5, column=0, padx=16, pady=(6, 2), sticky="w"
        )
        self.entry_precio = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 1350.00")
        self.entry_precio.grid(row=6, column=0, padx=16, pady=(0, 8), sticky="ew")

        # Campo 4: Stock
        ctk.CTkLabel(panel_izq, text="Stock").grid(
            row=7, column=0, padx=16, pady=(6, 2), sticky="w"
        )
        self.entry_stock = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 20")
        self.entry_stock.grid(row=8, column=0, padx=16, pady=(0, 14), sticky="ew")

        # Contenedor de botones de acción (sin lógica funcional por ahora)
        frame_botones = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_botones.grid(row=9, column=0, padx=16, pady=(4, 16), sticky="ew")
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar")
        btn_guardar.grid(row=0, column=0, padx=(0, 5), pady=(0, 8), sticky="ew")

        btn_buscar = ctk.CTkButton(frame_botones, text="Buscar")
        btn_buscar.grid(row=0, column=1, padx=(5, 0), pady=(0, 8), sticky="ew")

        btn_modificar = ctk.CTkButton(frame_botones, text="Modificar")
        btn_modificar.grid(row=1, column=0, padx=(0, 5), pady=(0, 0), sticky="ew")

        btn_eliminar = ctk.CTkButton(
            frame_botones,
            text="Eliminar",
            fg_color="#9e2a2b",
            hover_color="#7a1f20",
        )
        btn_eliminar.grid(row=1, column=1, padx=(5, 0), pady=(0, 0), sticky="ew")

    # Bloque 2: Panel derecho con tabla ttk.Treeview y barra de desplazamiento
    def _crear_panel_tabla(self) -> None:
        panel_der = ctk.CTkFrame(self, corner_radius=12)
        panel_der.grid(row=0, column=1, sticky="nsew", padx=(7, 14), pady=14)
        panel_der.grid_columnconfigure(0, weight=1)
        panel_der.grid_rowconfigure(1, weight=1)

        encabezado = ctk.CTkLabel(
            panel_der,
            text="Listado de Productos",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        encabezado.grid(row=0, column=0, padx=16, pady=(18, 10), sticky="w")

        contenedor_tabla = ctk.CTkFrame(panel_der, fg_color="transparent")
        contenedor_tabla.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        contenedor_tabla.grid_columnconfigure(0, weight=1)
        contenedor_tabla.grid_rowconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "precio", "stock")
        self.tabla = ttk.Treeview(
            contenedor_tabla,
            columns=columnas,
            show="headings",
            style="Dark.Treeview",
        )

        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        self.tabla.column("codigo", width=110, anchor="center")
        self.tabla.column("nombre", width=280, anchor="w")
        self.tabla.column("precio", width=120, anchor="e")
        self.tabla.column("stock", width=100, anchor="center")

        scrollbar = ctk.CTkScrollbar(
            contenedor_tabla, orientation="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(6, 0))

    # Bloque 3: Estilo visual oscuro para ttk.Treeview
    def _configurar_estilo_treeview(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Dark.Treeview",
            background="#1e1f24",
            foreground="#e6e6eb",
            fieldbackground="#1e1f24",
            bordercolor="#2b2d36",
            rowheight=32,
            font=("Segoe UI", 11),
        )
        estilo.configure(
            "Dark.Treeview.Heading",
            background="#2b2d36",
            foreground="#ffffff",
            bordercolor="#2b2d36",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
        )
        estilo.map(
            "Dark.Treeview",
            background=[("selected", "#1f538d")],
            foreground=[("selected", "#ffffff")],
        )
        estilo.map(
            "Dark.Treeview.Heading",
            background=[("active", "#383b47")],
        )


if __name__ == "__main__":
    app = KioscoVentana()
    app.mainloop()