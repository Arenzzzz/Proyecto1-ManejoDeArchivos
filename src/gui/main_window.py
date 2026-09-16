"""
main_window.py

Ventana principal de la aplicación. Contiene un menú con Archivo, Edición
y Ver (simulados: muestran un mensaje, no tienen funcionalidad real) y
Settings (funcional, abre la ventana de configuración real).
"""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from gui.settings_window import SettingsWindow
import config_manager as cm


class MainWindow(ctk.CTk):
    def __init__(self, config: dict, aviso_carga: str | None = None):
        super().__init__()

        self.config_data = config

        self.title("Proyecto 1 - Manejo de Archivos")
        self.geometry("700x450")

        self._build_menu()
        self._build_body()
        self.apply_config(config)

        if aviso_carga:
            # Se muestra después de construir la ventana para no bloquear el arranque
            self.after(200, lambda: messagebox.showwarning("Aviso de carga", aviso_carga))

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

        # Settings: única opción funcional del menú.
        # Se usa add_cascade (en vez de add_command) porque en macOS los
        # comandos puestos directo en la barra de menú no siempre se
        # muestran de forma confiable; un cascade sí funciona en todas
        # las plataformas.
        menu_settings = tk.Menu(menubar, tearoff=0)
        menu_settings.add_command(label="Abrir Settings", command=self.open_settings)
        menubar.add_cascade(label="Settings", menu=menu_settings)

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
        SettingsWindow(self, self.config_data, on_save=self._guardar_config)

    def _guardar_config(self, nuevo_config: dict):
        error = cm.save_config(nuevo_config)
        if error:
            messagebox.showerror("Error al guardar", error)
            return  # config_data no se actualiza: el guardado falló

        self.apply_config(nuevo_config)
        messagebox.showinfo("Settings", "Configuración guardada correctamente.")

    # ------------------------------------------------------------------
    # Aplicar configuración a la interfaz
    # ------------------------------------------------------------------
    def apply_config(self, config: dict):
        self.config_data = config
        nombre = config.get("nombre_usuario", "Usuario")
        self.label_bienvenida.configure(
            text=f"Bienvenido, {nombre}",
            text_color=config.get("color_letra", "#FFFFFF"),
        )
        self.label_info.configure(text_color=config.get("color_letra", "#FFFFFF"))

        # customtkinter usa "dark"/"light"; el enunciado pide "claro"/"oscuro"
        modo = "dark" if config.get("tema_interfaz") == "oscuro" else "light"
        ctk.set_appearance_mode(modo)
