from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from validador_contrasena import ValidadorContrasena
from hash_helper import HashHelper
from hash_password_helper import HashPasswordHelper
from symmetric_encryption_helper import SymmetricEncryptionHelper
from repositorio_apunte import RepositorioApunte

class CambiarContrasenaMaestraDialogo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambiar contraseña maestra")
        self.iniciarFormulario()

    def iniciarFormulario(self):
        lytOrganizador = QVBoxLayout()

        self.txtActualContrasena = QLineEdit()
        self.txtActualContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Ingresa la actual contraseña:"))
        lytOrganizador.addWidget(self.txtActualContrasena)

        self.txtNuevaContrasena = QLineEdit()
        self.txtNuevaContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Ingresa la nueva contraseña:"))
        lytOrganizador.addWidget(self.txtNuevaContrasena)

        self.txtConfirmarNuevaContrasena = QLineEdit()
        self.txtConfirmarNuevaContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Confirmar la nueva contraseña:"))
        lytOrganizador.addWidget(self.txtConfirmarNuevaContrasena)

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
        actualContrasena = self.txtActualContrasena.text()
        nuevaContrasena = self.txtNuevaContrasena.text()
        confirmarNuevaContrasena = self.txtConfirmarNuevaContrasena.text()
        if ValidadorContrasena.cumpleRequisitos(actualContrasena) and ValidadorContrasena.esNuevaContrasenaValida(actualContrasena, nuevaContrasena):
            HashPasswordHelper.HASH_GLOBAL = SymmetricEncryptionHelper.obtenerClaveDerivadaArgon2(SymmetricEncryptionHelper.DATA_FILE)
            if HashPasswordHelper.verificarHash(HashPasswordHelper.HASH_GLOBAL, actualContrasena):
                if ValidadorContrasena.validar(nuevaContrasena, confirmarNuevaContrasena) :
                    valor = HashPasswordHelper.generarHash(nuevaContrasena)
                    HashPasswordHelper.HASH_GLOBAL = valor
                    symmetricEncryptionHelper = SymmetricEncryptionHelper(HashPasswordHelper.HASH_GLOBAL)
                    dato = {
                        "version": "1.0",
                        "hash": HashPasswordHelper.HASH_GLOBAL,
                        "apuntes": RepositorioApunte.APUNTES
                    }
                    if(symmetricEncryptionHelper.cifrar(dato, SymmetricEncryptionHelper.DATA_FILE)):
                        QMessageBox.information(self, "Éxito", "Clave maestra cambiada correctamente...")
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
            else:
                 QMessageBox.warning(self, "Error", "Contraseña incorrecta...")
                 return;
        else:
            QMessageBox.warning(self, "Error",
                "La contraseña no cumple los requisitos de seguridad:\n"
                "- La contraseña nueva no debe coincidir con la actual\n"
                "- Las contraseñas nuevas deben coincidir\n"
                "- Al menos 8 caracteres\n"
                "- Una mayúscula\n"
                "- Una minúscula\n"
                "- Un número\n"
                "- Un símbolo")
            return;

        self.accept()