"""
main_window.py

Ventana principal de la aplicación. Contiene un menú con Archivo, Edición
y Ver (simulados: muestran un mensaje, no tienen funcionalidad real) y
Settings (funcional, abre la ventana de configuración real).
"""

import os
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from gui.settings_window import SettingsWindow
import config_manager as cm


class MainWindow(ctk.CTk):
    def __init__(self, config: dict, aviso_carga: str | None = None):
        super().__init__()

        self.config_data = config

        self.title("Laboratorio 1 - Manejo de Archivos")
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
        self.label_bienvenida.pack(pady=(30, 10))

        # Avatar circular con la foto de perfil (si hay una configurada).
        # Se usa un frame contenedor porque, en algunas versiones de
        # CustomTkinter, hacer label.configure(image=None) no limpia de
        # forma confiable una imagen previamente mostrada; en vez de eso,
        # el label del avatar se destruye y se recrea cada vez.
        self.frame_foto = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_foto.pack(pady=5)
        self.label_foto = None

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
        SettingsWindow(
            self,
            self.config_data,
            on_save=self._guardar_config,
            on_reset=self._restablecer_config,
        )

    def _guardar_config(self, nuevo_config: dict):
        error = cm.save_config(nuevo_config)
        if error:
            messagebox.showerror("Error al guardar", error)
            return  # config_data no se actualiza: el guardado falló

        self.apply_config(nuevo_config)
        messagebox.showinfo("Settings", "Configuración guardada correctamente.")

    def _restablecer_config(self):
        error = cm.reset_config()
        if error:
            messagebox.showerror("Error al restablecer", error)
            return

        config, _ = cm.load_config()  # archivo ya no existe -> valores por defecto
        self.apply_config(config)
        messagebox.showinfo(
            "Settings", "Configuración restablecida a los valores por defecto."
        )

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

        self._actualizar_foto_perfil(config.get("foto_perfil", ""))

        # customtkinter usa "dark"/"light"; el enunciado pide "claro"/"oscuro"
        modo = "dark" if config.get("tema_interfaz") == "oscuro" else "light"
        ctk.set_appearance_mode(modo)

    def _actualizar_foto_perfil(self, ruta: str):
        # Se destruye el label anterior (si existía) para evitar el bug
        # de CTkLabel que no limpia imágenes previas al reconfigurar.
        if self.label_foto is not None:
            self.label_foto.destroy()
            self.label_foto = None

        # Si no hay foto configurada, o el archivo ya no existe / no se
        # puede abrir como imagen (movido, borrado, corrupto), no se crea
        # ningún label nuevo: el avatar simplemente no se muestra, sin
        # lanzar una excepción sin capturar.
        if not ruta or not os.path.exists(ruta):
            return

        try:
            img = Image.open(ruta)
            img.thumbnail((96, 96))
            foto_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.label_foto = ctk.CTkLabel(self.frame_foto, text="", image=foto_ctk)
            self.label_foto.image = foto_ctk  # referencia para que no la recoja el GC
            self.label_foto.pack()
        except Exception as e:
            print(f"No se pudo cargar la foto de perfil ({ruta}): {e}")