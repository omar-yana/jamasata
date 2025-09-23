from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from validator.validador_contrasena import ValidadorContrasena
from helper.hash_helper import HashHelper
from helper.hash_password_helper import HashPasswordHelper
from helper.symmetric_encryption_helper import SymmetricEncryptionHelper
from dao.repositorio_apunte import RepositorioApunte

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
            HashPasswordHelper.HASH_COMPLETE_GLOBAL = None
            HashPasswordHelper.HASH_SALT_GLOBAL = None
            HashPasswordHelper.HASH_SALT_GLOBAL = SymmetricEncryptionHelper.obtenerClaveDerivadaArgon2(SymmetricEncryptionHelper.DATA_FILE)
            HashPasswordHelper.HASH_COMPLETE_GLOBAL = HashPasswordHelper.generarHash(contrasena, HashPasswordHelper.HASH_SALT_GLOBAL)
            print(HashPasswordHelper.HASH_COMPLETE_GLOBAL)
            print(HashPasswordHelper.HASH_SALT_GLOBAL)
            try:
                symmetricEncryptionHelper = SymmetricEncryptionHelper(HashPasswordHelper.HASH_COMPLETE_GLOBAL)
                dato = symmetricEncryptionHelper.descifrar(SymmetricEncryptionHelper.DATA_FILE)
                RepositorioApunte.APUNTES = dato["data"]
                print(RepositorioApunte.APUNTES)
            except Exception as e:
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