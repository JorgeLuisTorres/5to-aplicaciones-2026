import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional
import customtkinter as ctk

from database import buscar_registros, insertar_registro, obtener_registros

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class KioscoVentana(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Sistema Kiosco - ABM")
        self.geometry("1000x540")
        self.minsize(840, 460)
        self.id_seleccionado: Optional[int] = None

        self.grid_columnconfigure(0, weight=0, minsize=315)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._crear_panel_formulario()
        self._crear_panel_tabla()
        self._configurar_estilo_treeview()
        self.refrescar_tabla()

    def _crear_panel_formulario(self) -> None:
        panel_izq = ctk.CTkFrame(self, corner_radius=12)
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(14, 7), pady=14)
        panel_izq.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_izq,
            text="Gestión de Productos",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=16, pady=(18, 12), sticky="w")

        ctk.CTkLabel(panel_izq, text="Código").grid(row=1, column=0, padx=16, pady=(6, 2), sticky="w")
        self.entry_codigo = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 7790001")
        self.entry_codigo.grid(row=2, column=0, padx=16, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(panel_izq, text="Nombre").grid(row=3, column=0, padx=16, pady=(6, 2), sticky="w")
        self.entry_nombre = ctk.CTkEntry(panel_izq, placeholder_text="Ej: Alfajor Triple")
        self.entry_nombre.grid(row=4, column=0, padx=16, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(panel_izq, text="Precio").grid(row=5, column=0, padx=16, pady=(6, 2), sticky="w")
        self.entry_precio = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 1350.00")
        self.entry_precio.grid(row=6, column=0, padx=16, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(panel_izq, text="Stock").grid(row=7, column=0, padx=16, pady=(6, 2), sticky="w")
        self.entry_stock = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 20")
        self.entry_stock.grid(row=8, column=0, padx=16, pady=(0, 14), sticky="ew")

        frame_botones = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_botones.grid(row=9, column=0, padx=16, pady=(4, 16), sticky="ew")
        frame_botones.grid_columnconfigure((0, 1), weight=1)

        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=self.guardar_datos)
        btn_guardar.grid(row=0, column=0, padx=(0, 5), pady=(0, 8), sticky="ew")

        btn_buscar = ctk.CTkButton(frame_botones, text="Buscar", command=self.buscar_datos)
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

    def seleccionar_registro(self, _event: object) -> None:
        # Capturamos el elemento activo en la tabla
        seleccion = self.tabla.focus()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion, "values")
        if not valores:
            return

        self.id_seleccionado = int(seleccion)
        print("ID fila:", self.id_seleccionado, "| Fila seleccionada:", valores)

        # Limpiamos los campos y volcamos los valores con .insert()
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, valores[0])

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, valores[1])

        self.entry_precio.delete(0, "end")
        self.entry_precio.insert(0, valores[2])

        self.entry_stock.delete(0, "end")
        self.entry_stock.insert(0, valores[3])

    def buscar_datos(self) -> None:
        texto = self.entry_nombre.get().strip()
        if not texto:
            # Si está vacío, mostramos todos los registros activos
            self.refrescar_tabla()
            return

        try:
            resultados = buscar_registros(texto)
            self.refrescar_tabla(resultados)
        except sqlite3.Error as exc:
            messagebox.showerror("Error SQLite", f"No se pudo buscar: {exc}")

    def guardar_datos(self) -> None:
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        precio_texto = self.entry_precio.get().strip().replace(",", ".")
        stock_texto = self.entry_stock.get().strip()

        print("Código capturado:", codigo)
        print("Nombre capturado:", nombre)
        print("Precio capturado:", precio_texto)
        print("Stock capturado:", stock_texto)

        if not codigo or not nombre or not precio_texto or not stock_texto:
            messagebox.showwarning("Campos vacíos", "Completá todos los campos antes de guardar.")
            return

        try:
            precio = float(precio_texto)
            stock = int(stock_texto)
            if precio < 0 or stock < 0:
                raise ValueError("Valores negativos no permitidos.")
        except ValueError:
            messagebox.showerror("Dato inválido", "Precio debe ser numérico y Stock un entero mayor o igual a 0.")
            return

        try:
            nuevo_id = insertar_registro(codigo, nombre, precio, stock)
            if nuevo_id is None:
                messagebox.showwarning("Duplicado", "Ya existe un producto con ese nombre.")
                return
        except sqlite3.Error as exc:
            messagebox.showerror("Error SQLite", f"No se pudo guardar: {exc}")
            return

        self.limpiar_campos()
        self.refrescar_tabla()
        messagebox.showinfo("Guardado", "Registro guardado correctamente en la base de datos.")

    def limpiar_campos(self) -> None:
        self.id_seleccionado = None
        self.entry_codigo.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")

    def refrescar_tabla(self, registros: Optional[List[sqlite3.Row]] = None) -> None:
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        datos = obtener_registros() if registros is None else registros

        for prod in datos:
            self.tabla.insert(
                "",
                tk.END,
                iid=str(prod["id"]),
                values=(
                    prod["codigo"],
                    prod["nombre"],
                    f"{prod['precio']:.2f}",
                    prod["stock"],
                ),
            )

    def _crear_panel_tabla(self) -> None:
        panel_der = ctk.CTkFrame(self, corner_radius=12)
        panel_der.grid(row=0, column=1, sticky="nsew", padx=(7, 14), pady=14)
        panel_der.grid_columnconfigure(0, weight=1)
        panel_der.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_der,
            text="Listado de Productos",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=16, pady=(18, 10), sticky="w")

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

        # Conectamos el clic en la tabla con seleccionar_registro
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)

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