import os
import json
import hashlib
from datetime import datetime
from uuid import uuid4
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, QTextEdit
)
from PyQt5.QtCore import QDate, Qt
from model.apunte import Apunte
from dao.interfaz_repositorio_apunte import InterfazRepositorioApunte
from dao.repositorio_apunte import RepositorioApunte
from helper.hash_password_helper import HashPasswordHelper
from helper.symmetric_encryption_helper import SymmetricEncryptionHelper

class AdministrarApunte(QWidget):

    def __init__(self, interfazRepositorioApunte: InterfazRepositorioApunte):
        super().__init__()

        self.interfazRepositorioApunte = interfazRepositorioApunte
        bxlPrincipal = QHBoxLayout()
        self.setLayout(bxlPrincipal)

        self.tablaApunte = QTableWidget()
        self.tablaApunte.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablaApunte.setSelectionMode(QTableWidget.SingleSelection)
        self.tablaApunte.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tablaApunte.setColumnCount(8)
        self.tablaApunte.setHorizontalHeaderLabels([
            "ID", "Título", "URL", "Usuario", "Contraseña",
            "Modificado", "Caducidad", "Comentario"
        ])
        self.tablaApunte.setColumnHidden(0, True)
        self.tablaApunte.cellClicked.connect(self.seleccionarFila)
        bxlPrincipal.addWidget(self.tablaApunte)

        bxlFormularioApunte = QVBoxLayout()

        self.txtId = QLineEdit()
        self.txtId.setVisible(False)  # No se muestra en el formulario
        bxlFormularioApunte.addWidget(self.txtId)

        self.txtTitulo = QLineEdit()
        bxlFormularioApunte.addWidget(QLabel("Título:"))
        bxlFormularioApunte.addWidget(self.txtTitulo)

        self.txtUrl = QLineEdit()
        bxlFormularioApunte.addWidget(QLabel("URL:"))
        bxlFormularioApunte.addWidget(self.txtUrl)

        self.txtUsuario = QLineEdit()
        bxlFormularioApunte.addWidget(QLabel("Usuario:"))
        bxlFormularioApunte.addWidget(self.txtUsuario)

        self.txtContrasena = QLineEdit()
        self.txtContrasena.setEchoMode(QLineEdit.Password)
        bxlFormularioApunte.addWidget(QLabel("Contraseña:"))
        bxlFormularioApunte.addWidget(self.txtContrasena)

        self.btnMostrarContrasena = QPushButton("👁")
        self.btnMostrarContrasena.setCheckable(True)
        self.btnMostrarContrasena.toggled.connect(self.accionMostrarContrasena)
        bxlFormularioApunte.addWidget(self.btnMostrarContrasena)

        self.dateCaducidad = QDateEdit()
        self.dateCaducidad.setCalendarPopup(True)
        self.dateCaducidad.setDisplayFormat("yyyy-MM-dd")
        #self.dateCaducidad.setDate(QDate(2000, 1, 1))
        self.dateCaducidad.setSpecialValueText("")
        bxlFormularioApunte.addWidget(QLabel("Caducidad:"))
        bxlFormularioApunte.addWidget(self.dateCaducidad)

        self.txtComentario = QTextEdit()
        bxlFormularioApunte.addWidget(QLabel("Comentario:"))
        bxlFormularioApunte.addWidget(self.txtComentario)

        self.btnNuevo = QPushButton("Nuevo")
        self.btnNuevo.clicked.connect(self.accionNuevo)
        bxlFormularioApunte.addWidget(self.btnNuevo)

        self.btnAgregar = QPushButton("Aceptar")
        self.btnAgregar.clicked.connect(self.accionAgregarApunte)
        bxlFormularioApunte.addWidget(self.btnAgregar)

        self.btnEditar = QPushButton("Editar")
        self.btnEditar.clicked.connect(self.accionEditarApunte)
        bxlFormularioApunte.addWidget(self.btnEditar)

        self.btnEliminar = QPushButton("Eliminar")
        self.btnEliminar.clicked.connect(self.accionEliminarApunte)
        bxlFormularioApunte.addWidget(self.btnEliminar)

        bxlPrincipal.addLayout(bxlFormularioApunte)
        bxlPrincipal.setStretch(0, 3)  # 75%
        bxlPrincipal.setStretch(1, 1)  # 25%

        self.filaSeleccionada = None
        self.accionNuevo()
        self.cargarDatos()

    def accionMostrarContrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QLineEdit.Normal)
        else:
            self.txtContrasena.setEchoMode(QLineEdit.Password)

    def accionNuevo(self):
        self.limpiarFormulario()
        self.filaSeleccionada = None
        self.btnAgregar.setEnabled(True)
        self.btnEditar.setEnabled(False)
        self.btnEliminar.setEnabled(False)

    def accionAgregarApunte(self):
        apunte = self.leerFormulario()
        if not apunte:
            return
        self.interfazRepositorioApunte.agregar(apunte.to_dict())
        self.guardarDatos()
        self.refrescarTabla()
        self.accionNuevo()

    def accionEditarApunte(self):
        if self.filaSeleccionada is None:
            QMessageBox.warning(self, "Error", "Seleccione un apunte para editar")
            return
        id = self.tablaApunte.item(self.filaSeleccionada, 0).text()
        apunte = self.leerFormulario(id)
        if not apunte:
            return
        self.interfazRepositorioApunte.modificar(apunte.id, apunte.to_dict())
        self.guardarDatos()
        self.refrescarTabla()

    def accionEliminarApunte(self):
        if self.filaSeleccionada is None:
            QMessageBox.warning(self, "Error", "Seleccione un apunte para eliminar")
            return
        id = self.tablaApunte.item(self.filaSeleccionada, 0).text()
        self.interfazRepositorioApunte.eliminar(id)
        self.guardarDatos()
        self.refrescarTabla()
        self.accionNuevo()

    def seleccionarFila(self, fila, columna):
        self.filaSeleccionada = fila
        id = self.tablaApunte.item(self.filaSeleccionada, 0).text()
        apunte = self.interfazRepositorioApunte.obtenerPorId(id)
        self.txtId.setText(apunte["id"])
        self.txtTitulo.setText(apunte["titulo"])
        self.txtUrl.setText(apunte["url"])
        self.txtUsuario.setText(apunte["usuario"])
        self.txtContrasena.setText(apunte["contrasena"])

        if apunte["caducidad"]:
            cad = datetime.fromisoformat(apunte["caducidad"])
            self.dateCaducidad.setDate(QDate(cad.year, cad.month, cad.day))
        #else:
            #self.dateCaducidad.setDate(QDate.currentDate())

        self.txtComentario.setPlainText(apunte['comentario'])

        self.btnAgregar.setEnabled(False)
        self.btnEditar.setEnabled(True)
        self.btnEliminar.setEnabled(True)

    def cargarDatos(self):
        self.refrescarTabla()

    def guardarDatos(self):
        symmetricEncryptionHelper = SymmetricEncryptionHelper(HashPasswordHelper.HASH_COMPLETE_GLOBAL)
        dato = {
            "version": "1.0",
            "hash": HashPasswordHelper.HASH_SALT_GLOBAL,
            "data": RepositorioApunte.APUNTES
        }
        if not symmetricEncryptionHelper.cifrar(dato, SymmetricEncryptionHelper.DATA_FILE):
            QMessageBox.warning(self, "Error", "Problema al almacenar apunte")

    def refrescarTabla(self):
        self.tablaApunte.setRowCount(len(self.interfazRepositorioApunte.listar()))
        for i, apunte in enumerate(self.interfazRepositorioApunte.listar()):
            self.tablaApunte.setItem(i, 0, QTableWidgetItem(apunte['id']))
            self.tablaApunte.setItem(i, 1, QTableWidgetItem(apunte['titulo']))
            self.tablaApunte.setItem(i, 2, QTableWidgetItem(apunte['url']))
            self.tablaApunte.setItem(i, 3, QTableWidgetItem(apunte['usuario']))

            itemContrasena = QTableWidgetItem(apunte['contrasena'])
            itemContrasena.setFlags(itemContrasena.flags() & ~Qt.ItemIsEditable)  # no editable
            itemContrasena.setData(Qt.DisplayRole, '*' * len(apunte['contrasena']))

            self.tablaApunte.setItem(i, 4, itemContrasena)

            modificado = apunte['modificado']
            if isinstance(modificado, str):
                modificado = datetime.fromisoformat(modificado)
            self.tablaApunte.setItem(i, 5, QTableWidgetItem(modificado.strftime("%Y-%m-%d %H:%M")))

            caducidad = apunte['caducidad']
            if isinstance(caducidad, str) and caducidad:
                caducidad = datetime.fromisoformat(caducidad)
            self.tablaApunte.setItem(i, 6, QTableWidgetItem(
                caducidad.strftime("%Y-%m-%d") if caducidad else "")
            )

            self.tablaApunte.setItem(i, 7, QTableWidgetItem(apunte['comentario']))

    def leerFormulario(self, idApunte=None):
        id = self.txtId.text().strip()
        titulo = self.txtTitulo.text().strip()
        url = self.txtUrl.text().strip()
        usuario = self.txtUsuario.text().strip()
        contrasena = self.txtContrasena.text().strip()
        caducidadAux = self.dateCaducidad.date().toPyDate()
        comentario = self.txtComentario.toPlainText().strip()

        if not titulo or not usuario or not contrasena:
            QMessageBox.warning(self, "Error", "Título, usuario y contraseña son obligatorios")
            return None

        contenido = f"{titulo}|{usuario}|{contrasena}|{url}|{caducidadAux}|{comentario}"
        hashContenido = hashlib.sha256(contenido.encode("utf-8")).hexdigest()

        return Apunte(
            id=idApunte or hashContenido,
            titulo=titulo,
            usuario=usuario,
            contrasena=contrasena,
            url=url,
            modificado=datetime.now(),
            caducidad=caducidadAux,
            comentario=comentario
        )

    def limpiarFormulario(self):
        self.txtId.clear()
        self.txtTitulo.clear()
        self.txtUrl.clear()
        self.txtUsuario.clear()
        self.txtContrasena.clear()
        #self.dateCaducidad.setDate(QDate.currentDate())
        self.dateCaducidad.setSpecialValueText("")
        self.txtComentario.clear()
        self.txtComentario.setPlainText("")
