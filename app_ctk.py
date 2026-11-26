import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

import customtkinter as ctk

from productos_abm import alta, baja_logica, listar, modificar

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class KioscoAppCTk:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Kiosco - Gestión de Productos (CustomTkinter)")
        self.root.geometry("800x480")
        self.selected_id: Optional[int] = None

        self._construir_interfaz()
        self.refrescar_tabla()

    def _construir_interfaz(self) -> None:
        form = ctk.CTkFrame(self.root, corner_radius=10)
        form.pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkLabel(form, text="Nombre:").grid(row=0, column=0, padx=(12, 6), pady=12, sticky="w")
        self.entry_nombre = ctk.CTkEntry(form, width=240, placeholder_text="Ej: Alfajor Triple")
        self.entry_nombre.grid(row=0, column=1, padx=(0, 12), pady=12)

        ctk.CTkLabel(form, text="Precio:").grid(row=0, column=2, padx=(0, 6), pady=12, sticky="w")
        self.entry_precio = ctk.CTkEntry(form, width=110, placeholder_text="1350.00")
        self.entry_precio.grid(row=0, column=3, padx=(0, 12), pady=12)

        ctk.CTkLabel(form, text="Stock:").grid(row=0, column=4, padx=(0, 6), pady=12, sticky="w")
        self.entry_stock = ctk.CTkEntry(form, width=90, placeholder_text="20")
        self.entry_stock.grid(row=0, column=5, padx=(0, 12), pady=12)

        botones = ctk.CTkFrame(self.root, fg_color="transparent")
        botones.pack(fill="x", padx=12, pady=4)

        ctk.CTkButton(botones, text="Alta", width=95, command=self.agregar_producto).pack(side="left", padx=(0, 6))
        ctk.CTkButton(botones, text="Modificar", width=95, command=self.editar_producto).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            botones,
            text="Baja lógica",
            width=105,
            fg_color="#b42318",
            hover_color="#912018",
            command=self.eliminar_producto,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            botones,
            text="Limpiar",
            width=90,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.limpiar_campos,
        ).pack(side="left", padx=(0, 6))

        self.combo_tema = ctk.CTkComboBox(
            botones,
            values=["System", "Dark", "Light"],
            width=110,
            command=self._cambiar_tema,
        )
        self.combo_tema.set("System")
        self.combo_tema.pack(side="right")
        ctk.CTkLabel(botones, text="Tema:").pack(side="right", padx=(0, 6))

        tabla_frame = ctk.CTkFrame(self.root, corner_radius=10)
        tabla_frame.pack(fill="both", expand=True, padx=12, pady=(6, 12))

        columnas = ("id", "nombre", "precio", "stock")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=380, anchor="w")
        self.tree.column("precio", width=130, anchor="e")
        self.tree.column("stock", width=110, anchor="center")

        scrollbar = ctk.CTkScrollbar(tabla_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(4, 10), pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def _cambiar_tema(self, modo: str) -> None:
        ctk.set_appearance_mode(modo)

    def _leer_formulario(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            raise ValueError("Ingresá un nombre de producto.")

        precio_texto = self.entry_precio.get().strip().replace(",", ".")
        stock_texto = self.entry_stock.get().strip()

        precio = float(precio_texto)
        stock = int(stock_texto)

        if precio < 0 or stock < 0:
            raise ValueError("Precio y stock deben ser mayores o iguales a 0.")

        return nombre, precio, stock

    def agregar_producto(self) -> None:
        try:
            nombre, precio, stock = self._leer_formulario()
            nuevo_id = alta(nombre, precio, stock)
            if nuevo_id is None:
                messagebox.showwarning("Duplicado", "Ya existe un producto con ese nombre.")
                return
            self.refrescar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except ValueError as exc:
            messagebox.showerror("Dato inválido", str(exc))
        except sqlite3.Error as exc:
            messagebox.showerror("Error de base de datos", str(exc))

    def editar_producto(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Sin selección", "Seleccioná un producto de la tabla para modificar.")
            return
        try:
            nombre, precio, stock = self._leer_formulario()
            actualizado = modificar(self.selected_id, nombre, precio, stock)
            if not actualizado:
                messagebox.showwarning("No encontrado", "No se pudo actualizar el producto.")
                return
            self.refrescar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Producto actualizado.")
        except ValueError as exc:
            messagebox.showerror("Dato inválido", str(exc))
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicado", "Otro producto ya usa ese nombre.")
        except sqlite3.Error as exc:
            messagebox.showerror("Error de base de datos", str(exc))

    def eliminar_producto(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Sin selección", "Seleccioná un producto de la tabla para dar de baja.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar baja",
            "¿Dar de baja este producto? No se borrará de la base de datos.",
        )
        if not confirmar:
            return

        try:
            baja_logica(self.selected_id)
            self.refrescar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Producto dado de baja.")
        except sqlite3.Error as exc:
            messagebox.showerror("Error de base de datos", str(exc))

    def al_seleccionar(self, _event: object) -> None:
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0], "values")
        self.selected_id = int(valores[0])

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, valores[2].replace("$", "").strip())

        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, valores[3])

    def limpiar_campos(self) -> None:
        self.selected_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def refrescar_tabla(self) -> None:
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        for prod in listar(solo_activos=True):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    prod["id"],
                    prod["nombre"],
                    f"{prod['precio']:.2f}",
                    prod["stock"],
                ),
            )


if __name__ == "__main__":
    ventana = ctk.CTk()
    app = KioscoAppCTk(ventana)
    ventana.mainloop()