import os
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class AcercaDialogo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de")
        self.setFixedSize(400, 200)

        organizacionLayout = QVBoxLayout()

        nombreAplicacion = QLabel("<h2>Jamasata</h2>")
        nombreAplicacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        organizacionLayout.addWidget(nombreAplicacion)

        version = QLabel("Versión: 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        organizacionLayout.addWidget(version)

        autor = QLabel("Autor: Elias Yana")
        autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        organizacionLayout.addWidget(autor)

        descripcion = QLabel("Esta es una aplicación de Gestor de Contraseñas Seguro con PyQt5.")
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        organizacionLayout.addWidget(descripcion)

        derechoAutor = QLabel("© 2025 Elias Yana. Todos los derechos reservados.")
        derechoAutor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        organizacionLayout.addWidget(derechoAutor)

        # Espacio
        organizacionLayout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(organizacionLayout)