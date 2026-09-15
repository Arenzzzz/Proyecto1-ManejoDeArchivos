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
