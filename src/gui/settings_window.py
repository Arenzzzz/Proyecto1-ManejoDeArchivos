"""
settings_window.py

Ventana de Settings: permite configurar nombre_usuario, tema_interfaz,
idioma y tamaño_fuente. Los selectores de color y foto de perfil se
agregan en un commit posterior.
"""

from tkinter import colorchooser, filedialog, messagebox

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

        # --- Selectores de color (usan el selector nativo del sistema) ---
        self.color_barra_menu = self.config_actual.get("color_barra_menu", "#2B2B2B")
        self.color_letra = self.config_actual.get("color_letra", "#FFFFFF")

        ctk.CTkLabel(self, text="Color de la barra de menú").pack(anchor="w", **pad)
        fila_barra = ctk.CTkFrame(self, fg_color="transparent")
        fila_barra.pack(fill="x", padx=20)
        self.preview_barra = ctk.CTkLabel(
            fila_barra, text="", width=30, height=20, fg_color=self.color_barra_menu
        )
        self.preview_barra.pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            fila_barra, text="Elegir color...", command=self._elegir_color_barra
        ).pack(side="left")

        ctk.CTkLabel(self, text="Color de letra").pack(anchor="w", **pad)
        fila_letra = ctk.CTkFrame(self, fg_color="transparent")
        fila_letra.pack(fill="x", padx=20)
        self.preview_letra = ctk.CTkLabel(
            fila_letra, text="", width=30, height=20, fg_color=self.color_letra
        )
        self.preview_letra.pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            fila_letra, text="Elegir color...", command=self._elegir_color_letra
        ).pack(side="left")

        # --- Foto de perfil (seleccionada desde el sistema de archivos) ---
        self.foto_perfil = self.config_actual.get("foto_perfil", "")

        ctk.CTkLabel(self, text="Foto de perfil").pack(anchor="w", **pad)
        fila_foto = ctk.CTkFrame(self, fg_color="transparent")
        fila_foto.pack(fill="x", padx=20)
        self.label_ruta_foto = ctk.CTkLabel(
            fila_foto,
            text=self._nombre_corto(self.foto_perfil) or "(ninguna)",
            anchor="w",
        )
        self.label_ruta_foto.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            fila_foto, text="Elegir archivo...", command=self._elegir_foto
        ).pack(side="left")

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=20, pady=20, side="bottom")
        ctk.CTkButton(botones, text="Guardar", command=self._guardar).pack(
            side="right", padx=(10, 0)
        )
        ctk.CTkButton(
            botones, text="Cancelar", fg_color="gray", command=self.destroy
        ).pack(side="right")

    def _elegir_color_barra(self):
        # colorchooser.askcolor abre el selector de color nativo del SO
        _, hex_color = colorchooser.askcolor(
            color=self.color_barra_menu, title="Color de la barra de menú"
        )
        if hex_color:
            self.color_barra_menu = hex_color
            self.preview_barra.configure(fg_color=hex_color)

    def _elegir_color_letra(self):
        _, hex_color = colorchooser.askcolor(
            color=self.color_letra, title="Color de letra"
        )
        if hex_color:
            self.color_letra = hex_color
            self.preview_letra.configure(fg_color=hex_color)

    @staticmethod
    def _nombre_corto(ruta: str) -> str:
        import os
        return os.path.basename(ruta) if ruta else ""

    def _elegir_foto(self):
        # filedialog.askopenfilename abre el explorador de archivos nativo del SO
        ruta = filedialog.askopenfilename(
            title="Selecciona una foto de perfil",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if ruta:
            self.foto_perfil = ruta
            self.label_ruta_foto.configure(text=self._nombre_corto(ruta))

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
        self.config_actual["color_barra_menu"] = self.color_barra_menu
        self.config_actual["color_letra"] = self.color_letra
        self.config_actual["foto_perfil"] = self.foto_perfil

        self.on_save(self.config_actual)
        self.destroy()
