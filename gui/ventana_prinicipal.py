import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDesktopWidget, QDialog, QDialogButtonBox, QLineEdit, QAction, QMdiArea, QMdiSubWindow, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from gui_dialog.acerca_dialogo import AcercaDialogo
from gui_dialog.crear_contrasena_maestra_dialogo import CrearContrasenaMaestraDialogo
from gui_dialog.desbloquear_contrasena_maestra_dialogo import DesbloquearContrasenaMaestraDialogo
from gui_dialog.desbloquear_contrasena_maestra_dialogo import DesbloquearContrasenaMaestraDialogo
from gui_dialog.cambiar_contrasena_maestra_dialogo import CambiarContrasenaMaestraDialogo
from helper.symmetric_encryption_helper import SymmetricEncryptionHelper
from gui.adminsitrar_apunte import AdministrarApunte
from dao.repositorio_apunte import RepositorioApunte
class VentanaPrinicipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jamasata")
        self.setGeometry(100, 100, 600, 300)

        widgetCentralPrincipal = QWidget()
        self.setCentralWidget(widgetCentralPrincipal)
        self.centrarRedimencionarVentana(0.5, 0.5)

        self.crearMenu()

        self.mdiAreaPrincipal = QMdiArea()
        self.setCentralWidget(self.mdiAreaPrincipal)
        self.subVentana = None

        if SymmetricEncryptionHelper.existeDataFile():
            self.mostrarDesbloquearContrasenaMaestraDialogo()
        else:
            self.mostrarCrearContrasenaMaestraDialogo()

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

        menuAccionAdministrarApunte = QAction("Administrar apunte", self)
        menuAccionAdministrarApunte.triggered.connect(self.mostrarAdministrarApunte)
        menuArchivo.addAction(menuAccionAdministrarApunte)

        menuAccionCambiarContrasenaMaestra = QAction("Cambiar contraseña maestra", self)
        menuAccionCambiarContrasenaMaestra.triggered.connect(self.mostrarCambiarContrasenaMaestraDialogo)
        menuArchivo.addAction(menuAccionCambiarContrasenaMaestra)

        menuAccionSalir = QAction("Salir", self)
        menuAccionSalir.triggered.connect(self.close)
        menuArchivo.addAction(menuAccionSalir)

        menuAyuda = barraMenu.addMenu("Ayuda")

        menuAccionAcerca = QAction("Acerca de", self)
        menuAccionAcerca.triggered.connect(self.mostrarAcercaDialogo)
        menuAyuda.addAction(menuAccionAcerca)

    def mostrarAcercaDialogo(self):
        acercaDialogo = AcercaDialogo()
        acercaDialogo.exec_()

    def mostrarAdministrarApunte(self):
        self.crearSubVentana(AdministrarApunte(RepositorioApunte()), "Administrar apunte")

    def mostrarCrearContrasenaMaestraDialogo(self):
        crearContrasenaMaestraDialogo = CrearContrasenaMaestraDialogo()
        resultado = crearContrasenaMaestraDialogo.exec_()
        if resultado == QDialog.Rejected:
            sys.exit(0)

    def mostrarDesbloquearContrasenaMaestraDialogo(self):
        desbloquearContrasenaMaestraDialogo = DesbloquearContrasenaMaestraDialogo()
        resultado = desbloquearContrasenaMaestraDialogo.exec_()
        if resultado == QDialog.Rejected:
            sys.exit(0)

    def mostrarCambiarContrasenaMaestraDialogo(self):
        cambiarContrasenaMaestraDialogo = CambiarContrasenaMaestraDialogo()
        resultado = cambiarContrasenaMaestraDialogo.exec_()
        if resultado == QDialog.Rejected:
            sys.exit(0)

    def crearSubVentana(self, claseVentana, titulo="Ninguna"):
        if self.subVentana is not None and not self.subVentana.isHidden():
            self.subVentana.showNormal()
            self.subVentana.activateWindow()
            return

        self.subVentana = QMdiSubWindow()
        self.subVentana.setWidget(claseVentana)
        self.subVentana.setWindowTitle(titulo)
        self.mdiAreaPrincipal.addSubWindow(self.subVentana)
        self.subVentana.show()
        self.subVentana.showMaximized()