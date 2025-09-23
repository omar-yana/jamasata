from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from validator.validador_contrasena import ValidadorContrasena
from helper.hash_helper import HashHelper
from helper.hash_password_helper import HashPasswordHelper
from helper.symmetric_encryption_helper import SymmetricEncryptionHelper

class CrearContrasenaMaestraDialogo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear nueva contraseña maestra")
        self.iniciarFormulario()

    def iniciarFormulario(self):
        lytOrganizador = QVBoxLayout()

        self.txtContrasena = QLineEdit()
        self.txtContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Ingresa la contraseña:"))
        lytOrganizador.addWidget(self.txtContrasena)

        self.txtConfirmarContrasena = QLineEdit()
        self.txtConfirmarContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Confirmar la contraseña:"))
        lytOrganizador.addWidget(self.txtConfirmarContrasena)

        layOrganizadorBotones = QHBoxLayout()

        btnAceptar = QPushButton("Aceptar")
        btnAceptar.clicked.connect(self.accionVerificarContrasena)
        layOrganizadorBotones.addWidget(btnAceptar)

        btnCancelar = QPushButton("Cancelar")
        btnCancelar.clicked.connect(self.reject)  # Cierra el diálogo sin aceptar
        layOrganizadorBotones.addWidget(btnCancelar)

        lytOrganizador.addLayout(layOrganizadorBotones)

        self.setLayout(lytOrganizador)

    def accionVerificarContrasena(self):
        contrasena = self.txtContrasena.text()
        confirmarContrasena = self.txtConfirmarContrasena.text()

        if ValidadorContrasena.validar(contrasena, confirmarContrasena) :
            HashPasswordHelper.generarHashAleatorio(contrasena)
            if(HashPasswordHelper.verificarHash(HashPasswordHelper.HASH_COMPLETE_GLOBAL, contrasena)):
                print(HashPasswordHelper.HASH_COMPLETE_GLOBAL)
                print(HashPasswordHelper.HASH_SALT_GLOBAL)
                symmetricEncryptionHelper = SymmetricEncryptionHelper(HashPasswordHelper.HASH_COMPLETE_GLOBAL)
                dato = {
                    "version": "2.0",
                    "hash": HashPasswordHelper.HASH_SALT_GLOBAL,
                    "data": [{
                    "id": "hash1",
                    "titulo": "Correo Personal",
                    "usuario": "juan@gmail.com",
                    "contrasena": "1234abcd",
                    "url": "https://mail.google.com",
                    "modificado": "2025-09-22T22:30:00",
                    "caducidad": "2026-09-22T22:30:00",
                    "comentario": "Contraseña principal del correo"
                    }]
                }
                if(symmetricEncryptionHelper.cifrar(dato, SymmetricEncryptionHelper.DATA_FILE)):
                    QMessageBox.information(self, "Éxito", "Clave maestra creada correctamente...")
            else:
                QMessageBox.warning(self, "Error", "Contraseña incorrecta...")
                return;
        else:
            QMessageBox.warning(self, "Error",
                "La contraseña no cumple los requisitos de seguridad:\n"
                "- Las contraseñas deben coincidir\n"
                "- Al menos 8 caracteres\n"
                "- Una mayúscula\n"
                "- Una minúscula\n"
                "- Un número\n"
                "- Un símbolo")
            return;

        self.accept()