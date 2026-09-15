"""
settings_window.py

Ventana de Settings: permite configurar nombre_usuario, tema_interfaz,
idioma y tamaño_fuente. Los selectores de color y foto de perfil se
agregan en un commit posterior.
"""

from tkinter import messagebox

import customtkinter as ctk


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, config: dict, on_save):
        """
        master: ventana principal (MainWindow)
        config: dict con la configuración actual
        on_save: callback(nuevo_config: dict) que se llama al guardar
        """
        super().__init__(master)
        self.title("Settings")
        self.geometry("420x480")
        self.resizable(False, False)

        self.on_save = on_save
        self.config_actual = config.copy()

        self._build_form()

        # Modal: bloquea la ventana principal mientras está abierta
        self.transient(master)
        self.grab_set()

    def _build_form(self):
        pad = {"padx": 20, "pady": (10, 0)}

        ctk.CTkLabel(self, text="Nombre de usuario").pack(anchor="w", **pad)
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.insert(0, self.config_actual.get("nombre_usuario", ""))
        self.entry_nombre.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Tema de interfaz").pack(anchor="w", **pad)
        self.combo_tema = ctk.CTkComboBox(self, values=["claro", "oscuro"])
        self.combo_tema.set(self.config_actual.get("tema_interfaz", "claro"))
        self.combo_tema.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Idioma").pack(anchor="w", **pad)
        self.combo_idioma = ctk.CTkComboBox(
            self, values=["es", "es-ES", "en", "en-US"]
        )
        self.combo_idioma.set(self.config_actual.get("idioma", "es"))
        self.combo_idioma.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Tamaño de fuente").pack(anchor="w", **pad)
        self.entry_fuente = ctk.CTkEntry(self)
        self.entry_fuente.insert(0, str(self.config_actual.get("tamaño_fuente", 12)))
        self.entry_fuente.pack(fill="x", padx=20)

        # Placeholder para los selectores de color y foto (commit siguiente)
        self.frame_extra = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_extra.pack(fill="x", padx=20, pady=10)

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=20, pady=20, side="bottom")
        ctk.CTkButton(botones, text="Guardar", command=self._guardar).pack(
            side="right", padx=(10, 0)
        )
        ctk.CTkButton(
            botones, text="Cancelar", fg_color="gray", command=self.destroy
        ).pack(side="right")

    def _guardar(self):
        try:
            tamano_fuente = int(self.entry_fuente.get())
        except ValueError:
            messagebox.showerror(
                "Valor inválido", "El tamaño de fuente debe ser un número entero."
            )
            return

        self.config_actual["nombre_usuario"] = self.entry_nombre.get()
        self.config_actual["tema_interfaz"] = self.combo_tema.get()
        self.config_actual["idioma"] = self.combo_idioma.get()
        self.config_actual["tamaño_fuente"] = tamano_fuente

        self.on_save(self.config_actual)
        self.destroy()
