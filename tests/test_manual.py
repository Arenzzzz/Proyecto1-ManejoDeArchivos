"""
test_manual.py

Script de verificación manual (no requiere pytest) para evidenciar:
  1. Codificación UTF-8: nombre_usuario e idioma con tildes/ñ sobreviven
     un ciclo completo de guardado + carga.
  2. Caso "archivo ausente": carga limpia con valores por defecto.
  3. Caso "archivo corrupto": carga limpia con valores por defecto + aviso.
  4. Escritura segura + respaldo: tras dos guardados consecutivos existe
     un config.bak con el contenido del guardado anterior.

Ejecutar con: python tests/test_manual.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import config_manager as cm

TEST_PATH = os.path.join(os.path.dirname(__file__), "config_test.json")
BACKUP_PATH = TEST_PATH + ".bak"


def limpiar():
    for p in (TEST_PATH, BACKUP_PATH, TEST_PATH + ".tmp"):
        if os.path.exists(p):
            os.remove(p)


def caso_archivo_ausente():
    limpiar()
    config, aviso = cm.load_config(TEST_PATH)
    assert aviso is None
    assert config == cm.DEFAULT_CONFIG
    print("[OK] Caso archivo ausente -> valores por defecto, sin excepción.")


def caso_utf8_tildes_enye():
    limpiar()
    original = cm.DEFAULT_CONFIG.copy()
    original["nombre_usuario"] = "José Muñoz Peláez"
    original["idioma"] = "es-ES"

    error = cm.save_config(original, TEST_PATH)
    assert error is None

    cargado, aviso = cm.load_config(TEST_PATH)
    assert aviso is None
    assert cargado["nombre_usuario"] == "José Muñoz Peláez"
    assert cargado["idioma"] == "es-ES"
    print("[OK] UTF-8: tildes y ñ se guardaron y recuperaron sin corrupción.")


def caso_archivo_corrupto():
    limpiar()
    with open(TEST_PATH, "w", encoding="utf-8") as f:
        f.write("{ esto no es json válido ")

    config, aviso = cm.load_config(TEST_PATH)
    assert aviso is not None
    assert config == cm.DEFAULT_CONFIG
    print(f"[OK] Caso archivo corrupto -> aviso mostrado: '{aviso}'")


def caso_respaldo():
    limpiar()
    primero = cm.DEFAULT_CONFIG.copy()
    primero["nombre_usuario"] = "Primera versión"
    cm.save_config(primero, TEST_PATH)

    segundo = cm.DEFAULT_CONFIG.copy()
    segundo["nombre_usuario"] = "Segunda versión"
    cm.save_config(segundo, TEST_PATH)

    assert os.path.exists(BACKUP_PATH)
    respaldo, _ = cm.load_config(BACKUP_PATH)
    assert respaldo["nombre_usuario"] == "Primera versión"
    print("[OK] Respaldo (.bak) conserva la configuración anterior al guardado.")


if __name__ == "__main__":
    caso_archivo_ausente()
    caso_utf8_tildes_enye()
    caso_archivo_corrupto()
    caso_respaldo()
    limpiar()
    print("\nTodas las verificaciones manuales pasaron correctamente.")
