import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# 4. Tema visual oscuro obligatorio
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppFarmacia(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Sistema de Farmacia - Gestión de Medicamentos")
        self.geometry("1000x500")
        self.resizable(False, False)

        # Configurar la cuadrícula principal (2 columnas: Formulario | Tabla)
        self.grid_columnconfigure(0, weight=1) # Columna del formulario (Izquierda)
        self.grid_columnconfigure(1, weight=2) # Columna de la tabla (Derecha)
        self.grid_rowconfigure(0, weight=1)

        # =========================================================================
        # 1. FORMULARIO A LA IZQUIERDA (Campos de Texto CTkEntry)
        # =========================================================================
        self.frame_izquierdo = ctk.CTkFrame(self, width=320, corner_radius=10)
        self.frame_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_izquierdo.grid_propagate(False) # Mantiene el tamaño fijo del panel

        # Título del Formulario
        lbl_titulo = ctk.CTkLabel(self.frame_izquierdo, text="Datos del Medicamento", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_titulo.pack(pady=(20, 15))

        # Campo 1: Nombre del Medicamento
        self.entry_nombre = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Nombre del Medicamento", width=260)
        self.entry_nombre.pack(pady=10)

        # Campo 2: Monodroga / Componente
        self.entry_monodroga = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Monodroga (ej: Paracetamol)", width=260)
        self.entry_monodroga.pack(pady=10)

        # Campo 3: Precio
        self.entry_precio = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Precio ($)", width=260)
        self.entry_precio.pack(pady=10)

        # Campo 4: Stock disponible
        self.entry_stock = ctk.CTkEntry(self.frame_izquierdo, placeholder_text="Cantidad en Stock", width=260)
        self.entry_stock.pack(pady=10)

        # =========================================================================
        # 2. BOTONES DE ACCIÓN (CTkButton - Solo interfaz visual)
        # =========================================================================
        self.frame_botones = ctk.CTkFrame(self.frame_izquierdo, fg_color="transparent")
        self.frame_botones.pack(pady=(20, 0))

        # Fila 1 de botones
        self.btn_guardar = ctk.CTkButton(self.frame_botones, text="Guardar", width=120, fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=5)

        self.btn_buscar = ctk.CTkButton(self.frame_botones, text="Buscar", width=120)
        self.btn_buscar.grid(row=0, column=1, padx=5, pady=5)

        # Fila 2 de botones
        self.btn_modificar = ctk.CTkButton(self.frame_botones, text="Modificar", width=120, fg_color="#f39c12", hover_color="#d35400")
        self.btn_modificar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar", width=120, fg_color="#e74c3c", hover_color="#c0392b")
        self.btn_eliminar.grid(row=1, column=1, padx=5, pady=5)


        # =========================================================================
        # 3. TABLA A LA DERECHA (ttk.Treeview con Estilo Oscuro)
        # =========================================================================
        self.frame_derecho = ctk.CTkFrame(self, corner_radius=10)
        self.frame_derecho.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        # Configurar estilos de tkinter clásico (ttk) para integrarse al modo oscuro
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Treeview",
                        background="#2a2d2e",       # Fondo de las celdas
                        foreground="white",          # Color de la letra
                        rowheight=25,                # Altura de cada fila
                        fieldbackground="#2a2d2e",   # Fondo del área vacía
                        borderwidth=0)
        
        style.configure("Treeview.Heading",
                        background="#1f2122",       # Fondo de los encabezados
                        foreground="white",          # Letra de encabezados
                        relief="flat")
        
        # Cambiar el color de selección de la fila de la tabla
        style.map('Treeview', background=[('selected', '#1f538d')])

        # Definición de las columnas del Treeview
        columnas = ("medicamento", "monodroga", "precio", "stock")
        self.tabla = ttk.Treeview(self.frame_derecho, columns=columnas, show="headings")
        
        # Definir los encabezados de las columnas
        self.tabla.heading("medicamento", text="Medicamento")
        self.tabla.heading("monodroga", text="Monodroga")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        # Configurar anchos de columna
        self.tabla.column("medicamento", width=180, anchor="w")
        self.tabla.column("monodroga", width=180, anchor="w")
        self.tabla.column("precio", width=100, anchor="center")
        self.tabla.column("stock", width=100, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.frame_derecho, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # Ubicar la tabla y su barra de desplazamiento
        self.tabla.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

        # Inserción de datos de prueba / demostración visual
        datos_ejemplo = [
            ("Ibuprofeno 600mg", "Ibuprofeno", "$1.500", "45"),
            ("Paracetamol 500mg", "Paracetamol", "$1.200", "12"),
            ("Amoxidal 500", "Amoxicilina", "$4.300", "8"),
            ("Losartan 50mg", "Losartan", "$2.800", "30")
        ]
        for item in datos_ejemplo:
            self.tabla.insert("", "end", values=item)

# Inicialización y ejecución del bucle de la aplicación
if __name__ == "__main__":
    app = AppFarmacia()
    app.mainloop()
