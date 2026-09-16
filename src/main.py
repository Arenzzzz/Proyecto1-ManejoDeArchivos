"""
main.py

Punto de entrada de la aplicación. Carga la configuración (con manejo de
errores incluido en config_manager) y arranca la ventana principal.

Ejecutar con: python src/main.py
"""

import config_manager as cm
from gui.main_window import MainWindow      


def main():
    config, aviso_carga = cm.load_config()
    app = MainWindow(config, aviso_carga=aviso_carga)
    app.mainloop()


if __name__ == "__main__":
    main()
