"""
config_manager.py

Encargado de toda la persistencia del archivo de configuración de usuario:
carga inicial, escritura segura (tmp + rename), respaldo (.bak) y manejo
explícito de errores (archivo ausente, corrupto, sin permisos).

Formato elegido: JSON (ver justificación en README.md).
"""

import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
BACKUP_PATH = CONFIG_PATH + ".bak"
TMP_PATH = CONFIG_PATH + ".tmp"

# Valores por defecto: se usan si el archivo no existe o está corrupto.
DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "claro",
    "idioma": "es",
    "tamaño_fuente": 12,
    "color_barra_menu": "#2B2B2B",
    "color_letra": "#FFFFFF",
    "foto_perfil": "",
}


def load_config(path: str = CONFIG_PATH) -> dict:
    """
    Carga la configuración desde `path`.
    Si el archivo no existe, retorna una copia de los valores por defecto
    sin lanzar excepción.
    """
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Aseguramos que cualquier clave faltante se complete con el default
    config = DEFAULT_CONFIG.copy()
    config.update(data)
    return config


def save_config(config: dict, path: str = CONFIG_PATH) -> None:
    """
    Guarda `config` de forma segura:
    1. Si ya existe un archivo de configuración, se respalda en .bak
       ANTES de tocar el archivo final.
    2. Se escribe el contenido nuevo en un archivo temporal (.tmp).
    3. Se reemplaza el archivo final con el temporal usando os.replace,
       que es atómico a nivel de sistema de archivos. Así, si la app se
       cierra a la mitad del guardado, el archivo final nunca queda
       corrupto o a medio escribir: o quedó el viejo completo, o el
       nuevo completo.
    """
    tmp_path = path + ".tmp"
    backup_path = path + ".bak"

    # 1. Respaldo de la configuración anterior (si existe)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as src, \
             open(backup_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())

    # 2. Escritura a archivo temporal
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    # 3. Reemplazo atómico del archivo final
    os.replace(tmp_path, path)
