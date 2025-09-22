import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDesktopWidget, QDialog, QDialogButtonBox, QLineEdit, QAction, QMdiArea, QMdiSubWindow, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from acerca_dialogo import AcercaDialogo

DATA_FILE = "apuntes.json"
PASSWORD = "1234"
class Jamasata(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jamasata")
        self.setGeometry(100, 100, 400, 300)

        widgetCentralPrincipal = QWidget()
        self.setCentralWidget(widgetCentralPrincipal)
        self.centrarRedimencionarVentana(0.4, 0.4)

        self.crearMenu()

        self.mdiAreaPrincipal = QMdiArea()
        self.setCentralWidget(self.mdiAreaPrincipal)
        self.subVentana = None

    def centrarRedimencionarVentana(self, anchoPorcentaje, altoPorcentaje):
        pantalla = QDesktopWidget().availableGeometry()  # Obtener tamaño de pantalla disponible
        pantallaAncho = pantalla.width()
        pantallaAlto = pantalla.height()

        # Calcular tamaño basado en porcentaje
        ventanaAncho = int(pantallaAncho * anchoPorcentaje)
        ventanaAlto = int(pantallaAlto * altoPorcentaje)

        # Establecer tamaño
        self.setGeometry(0, 0, ventanaAncho, ventanaAlto)

        # Centrar la ventana
        frameGeometry = self.frameGeometry()
        puntoCentral = pantalla.center()
        frameGeometry.moveCenter(puntoCentral)
        self.move(frameGeometry.topLeft())

    def crearMenu(self):
        barraMenu = self.menuBar()

        menuArchivo = barraMenu.addMenu("Archivo")

        menuAccionSalir = QAction("Salir", self)
        menuAccionSalir.triggered.connect(self.close)
        menuArchivo.addAction(menuAccionSalir)

        menuAccionAdministrarApunte = QAction("Administrar apunte", self)
        menuAccionAdministrarApunte.triggered.connect(self.mostrarAcercaDialogo)
        menuArchivo.addAction(menuAccionAdministrarApunte)

        menuAccionCambiarContrasenaMaestra = QAction("Cambiar contraseña maestra", self)
        menuAccionCambiarContrasenaMaestra.triggered.connect(self.mostrarAcercaDialogo)
        menuArchivo.addAction(menuAccionCambiarContrasenaMaestra)

        menuAyuda = barraMenu.addMenu("Ayuda")

        menuAccionAcerca = QAction("Acerca de", self)
        menuAccionAcerca.triggered.connect(self.mostrarAcercaDialogo)
        menuAyuda.addAction(menuAccionAcerca)

    def mostrarAcercaDialogo(self):
        acercaDialogo = AcercaDialogo()
        acercaDialogo.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Jamasata()
    ventana.show()
    sys.exit(app.exec_())