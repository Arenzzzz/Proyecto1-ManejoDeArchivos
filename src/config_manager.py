"""
config_manager.py

Encargado de toda la persistencia del archivo de configuración de usuario:
carga inicial, escritura segura (tmp + rename), respaldo (.bak) y manejo
explícito de errores (archivo ausente, corrupto, sin permisos).

Formato elegido: JSON (ver justificación en README.md).
"""

import json
import logging
import os

logger = logging.getLogger("config_manager")

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
    "color_letra": "#1A1A1A",
    "foto_perfil": "",
}


def load_config(path: str = CONFIG_PATH) -> tuple[dict, str | None]:
    """
    Carga la configuración desde `path`.

    Maneja explícitamente los tres casos exigidos por el laboratorio,
    degradando siempre a un comportamiento definido (nunca a un
    traceback sin capturar):

      - Archivo ausente        -> valores por defecto, sin aviso de error.
      - Archivo corrupto/JSON inválido -> valores por defecto + aviso.
      - Sin permisos de lectura -> valores por defecto + aviso.

    Retorna una tupla (config, mensaje_de_aviso). `mensaje_de_aviso` es
    None cuando la carga fue normal, o un texto para mostrar al usuario
    en la GUI cuando hubo un problema y se usaron valores por defecto.
    """
    # Caso 1: archivo ausente
    if not os.path.exists(path):
        logger.info("Archivo de configuración no encontrado, usando valores por defecto.")
        return DEFAULT_CONFIG.copy(), None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config, None

    # Caso 2: archivo corrupto o formato inválido
    except json.JSONDecodeError as e:
        logger.error("Configuración corrupta (%s): %s", path, e)
        return DEFAULT_CONFIG.copy(), (
            "El archivo de configuración está dañado o tiene un formato "
            "inválido. Se cargaron los valores por defecto."
        )

    # Caso 3: falta de permisos de lectura
    except PermissionError as e:
        logger.error("Sin permisos de lectura sobre %s: %s", path, e)
        return DEFAULT_CONFIG.copy(), (
            "No se tienen permisos para leer el archivo de configuración. "
            "Se cargaron los valores por defecto."
        )

    # Cualquier otro error de E/S inesperado también se captura, nunca
    # se deja propagar como traceback sin controlar.
    except OSError as e:
        logger.error("Error de E/S al leer %s: %s", path, e)
        return DEFAULT_CONFIG.copy(), (
            "Ocurrió un error inesperado al leer la configuración. "
            "Se cargaron los valores por defecto."
        )


def save_config(config: dict, path: str = CONFIG_PATH) -> str | None:
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

    Retorna None si el guardado fue exitoso, o un mensaje de error para
    mostrar al usuario si falló por falta de permisos u otro error de E/S
    (caso 3 del laboratorio: falta de permisos de escritura).
    """
    tmp_path = path + ".tmp"
    backup_path = path + ".bak"

    try:
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
        return None

    except PermissionError as e:
        logger.error("Sin permisos de escritura sobre %s: %s", path, e)
        return (
            "No se tienen permisos para escribir el archivo de "
            "configuración. Los cambios no se guardaron."
        )

    except OSError as e:
        logger.error("Error de E/S al guardar %s: %s", path, e)
        return (
            "Ocurrió un error inesperado al guardar la configuración. "
            "Los cambios no se guardaron."
        )

def reset_config(path: str = CONFIG_PATH) -> str | None:
    """
    Restablece la configuración a los valores por defecto, eliminando el
    archivo config.json actual (config.json.bak se conserva como
    respaldo). En el siguiente load_config() se ejecutará el mismo camino
    de "archivo ausente" que al primer arranque de la aplicación.

    Retorna None si se eliminó correctamente (o si ya no existía), o un
    mensaje de error si falló por falta de permisos.
    """
    if not os.path.exists(path):
        return None

    try:
        os.remove(path)
        return None
    except PermissionError as e:
        logger.error("Sin permisos para eliminar %s: %s", path, e)
        return "No se tienen permisos para eliminar el archivo de configuración."
    except OSError as e:
        logger.error("Error de E/S al eliminar %s: %s", path, e)
        return "Ocurrió un error inesperado al eliminar la configuración."