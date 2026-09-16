# Laboratorio No. 1 — Manejo e Implementación de Archivos

Aplicación de escritorio en Python (CustomTkinter) para gestionar un archivo
de configuración de usuario, con lectura, escritura segura, respaldo y
manejo robusto de errores.

## Ejecución

```bash
pip install -r requirements.txt
python src/main.py
```

## Estructura del proyecto

```
src/
  config_manager.py     # Toda la persistencia: carga, guardado, respaldo, errores
  main.py                # Punto de entrada
  gui/
    main_window.py       # Menú (Archivo/Edición/Ver simulados) + Settings
    settings_window.py   # Formulario de configuración
tests/
  test_manual.py          # Verificación de UTF-8 y los 3 casos de error
ejemplos/
  config.ejemplo.json      # Ejemplo de archivo generado (con tildes/ñ)
  config.ejemplo.json.bak  # Ejemplo del respaldo generado
```

## Formato de almacenamiento: JSON

Se eligió **JSON** frente a **XML** (alternativa descartada) para el archivo
de configuración:

| Criterio                  | JSON                                             | XML (descartado)                                   |
|----------------------------|---------------------------------------------------|------------------------------------------------------|
| Tamaño                    | Más compacto (sin etiquetas de cierre repetidas) | Más pesado por las etiquetas de apertura/cierre       |
| Legibilidad               | Estructura clave-valor clara para configs planas | Verboso para pares clave-valor simples                |
| Facilidad de parseo       | Soporte nativo en Python (`json`), sin dependencias | Requiere `xml.etree` o librerías extra, más código     |
| Robustez ante corrupción  | Un solo `json.JSONDecodeError` cubre casi todos los errores de formato | Errores de parseo más variados y difíciles de anticipar |
| Tipos de datos             | Mapea directo a `dict`/`int`/`str` de Python     | Todo es texto; hay que convertir tipos manualmente     |

Para una configuración de usuario (pares clave-valor simples, sin
jerarquías profundas ni necesidad de validación por esquema), JSON ofrece
menor complejidad de código y menor superficie de error sin sacrificar
legibilidad.

## Escritura segura y respaldo

`config_manager.save_config()` sigue tres pasos para que un cierre abrupto
nunca deje el archivo corrupto:

```python
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
```

`os.replace` es atómico a nivel de sistema operativo: si la aplicación se
cierra durante el paso 2, `config.json` conserva su versión anterior
intacta; el archivo nuevo solo reemplaza al viejo una vez que está
completamente escrito.

## Manejo de errores

`config_manager.load_config()` y `save_config()` capturan explícitamente:

1. **Archivo ausente** → se usan los valores por defecto (`DEFAULT_CONFIG`),
   sin excepción ni aviso al usuario.
2. **Archivo corrupto / formato inválido** → se captura
   `json.JSONDecodeError`, se usan los valores por defecto y se muestra un
   aviso al usuario (`messagebox.showwarning` en `MainWindow`).
3. **Falta de permisos de lectura/escritura** → se captura `PermissionError`
   (y `OSError` como respaldo general), degradando a valores por defecto
   (lectura) o avisando que el guardado falló (escritura).

Evidencia de estos tres casos: `tests/test_manual.py` (ejecutar con
`python tests/test_manual.py`).

## Codificación UTF-8

Toda lectura y escritura especifica `encoding="utf-8"` explícitamente, y
`json.dump` se llama con `ensure_ascii=False` para que tildes y la letra
`ñ` se guarden como caracteres reales (no como escapes `\uXXXX`). Ver
`ejemplos/config.ejemplo.json`, generado con "José Ángel Muñoz Peláez".

## Settings

La ventana de Settings (única opción funcional del menú) permite
configurar: `nombre_usuario`, `tema_interfaz`, `idioma`, `tamaño_fuente`,
`color_barra_menu` y `color_letra` (con el selector de color nativo del
sistema vía `tkinter.colorchooser`), y `foto_perfil` (con el explorador de
archivos nativo vía `tkinter.filedialog`). Todos los valores pasan por el
mismo flujo de persistencia (`save_config` / `load_config`).
