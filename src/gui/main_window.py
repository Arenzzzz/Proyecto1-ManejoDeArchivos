"""
main_window.py

Ventana principal de la aplicación. Contiene un menú con Archivo, Edición
y Ver (simulados: muestran un mensaje, no tienen funcionalidad real) y
Settings (funcional, abre la ventana de configuración real).
"""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


class MainWindow(ctk.CTk):
    def __init__(self, config: dict):
        super().__init__()

        self.config_data = config

        self.title("Laboratorio 1 - Manejo de Archivos")
        self.geometry("700x450")

        self._build_menu()
        self._build_body()
        self.apply_config(config)

    # ------------------------------------------------------------------
    # Menú
    # ------------------------------------------------------------------
    def _build_menu(self):
        menubar = tk.Menu(self)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        for label in ("Nuevo", "Abrir", "Guardar", "Salir"):
            menu_archivo.add_command(
                label=label, command=lambda l=label: self._simulado(l)
            )
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        menu_edicion = tk.Menu(menubar, tearoff=0)
        for label in ("Deshacer", "Rehacer", "Copiar", "Pegar"):
            menu_edicion.add_command(
                label=label, command=lambda l=label: self._simulado(l)
            )
        menubar.add_cascade(label="Edición", menu=menu_edicion)

        menu_ver = tk.Menu(menubar, tearoff=0)
        for label in ("Zoom +", "Zoom -", "Pantalla completa"):
            menu_ver.add_command(
                label=label, command=lambda l=label: self._simulado(l)
            )
        menubar.add_cascade(label="Ver", menu=menu_ver)

        # Settings: única opción funcional del menú
        menubar.add_command(label="Settings", command=self.open_settings)

        self.configure(menu=menubar)

    def _simulado(self, nombre_opcion: str):
        messagebox.showinfo(
            "Opción simulada",
            f"'{nombre_opcion}' es una opción simulada del menú "
            "(no requiere funcionalidad real según el enunciado).",
        )

    # ------------------------------------------------------------------
    # Cuerpo de la ventana
    # ------------------------------------------------------------------
    def _build_body(self):
        self.label_bienvenida = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_bienvenida.pack(pady=30)

        self.label_info = ctk.CTkLabel(
            self,
            text="Usa el menú Settings para configurar tu perfil y la interfaz.",
        )
        self.label_info.pack(pady=10)

        boton_settings = ctk.CTkButton(
            self, text="Abrir Settings", command=self.open_settings
        )
        boton_settings.pack(pady=20)

    def open_settings(self):
        # Se implementa en un commit posterior (settings_window.py)
        pass

    # ------------------------------------------------------------------
    # Aplicar configuración a la interfaz
    # ------------------------------------------------------------------
    def apply_config(self, config: dict):
        self.config_data = config
        nombre = config.get("nombre_usuario", "Usuario")
        self.label_bienvenida.configure(text=f"Bienvenido, {nombre}")
