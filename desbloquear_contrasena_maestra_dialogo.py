from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from validador_contrasena import ValidadorContrasena
from hash_helper import HashHelper
from hash_password_helper import HashPasswordHelper
from symmetric_encryption_helper import SymmetricEncryptionHelper
from repositorio_apunte import RepositorioApunte

class DesbloquearContrasenaMaestraDialogo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Desbloquear con contraseña maestra")
        self.iniciarFormulario()

    def iniciarFormulario(self):
        lytOrganizador = QVBoxLayout()

        self.txtContrasena = QLineEdit()
        self.txtContrasena.setEchoMode(QLineEdit.Password)
        lytOrganizador.addWidget(QLabel("Ingresa la contraseña:"))
        lytOrganizador.addWidget(self.txtContrasena)

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

        if ValidadorContrasena.cumpleRequisitos(contrasena) :
            HashPasswordHelper.HASH_GLOBAL = SymmetricEncryptionHelper.obtenerClaveDerivadaArgon2(SymmetricEncryptionHelper.DATA_FILE)
            if HashPasswordHelper.verificarHash(HashPasswordHelper.HASH_GLOBAL, contrasena):
                symmetricEncryptionHelper = SymmetricEncryptionHelper(HashPasswordHelper.HASH_GLOBAL)
                dato = symmetricEncryptionHelper.descifrar(SymmetricEncryptionHelper.DATA_FILE)
                #if dato is None:
                    #QMessageBox.information(self, "Éxito", "Contraseña incorrecta...")
                    #return;
                RepositorioApunte.APUNTES = dato["apuntes"]
                print(RepositorioApunte.APUNTES)
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