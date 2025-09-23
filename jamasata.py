import sys
from PyQt5.QtWidgets import QApplication
from gui.ventana_prinicipal import VentanaPrinicipal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrinicipal()
    ventana.show()
    sys.exit(app.exec_())