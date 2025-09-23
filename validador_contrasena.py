import re

class ValidadorContrasena:
    @staticmethod
    def validar(contrasena: str, confirmarContrasena: str) -> bool:
        if not contrasena or not confirmarContrasena:
            return False

        if contrasena != confirmarContrasena:
            return False

        if not ValidadorContrasena.cumpleRequisitos(contrasena):
            return False

        return True

    def esNuevaContrasenaValida(actual: str, nueva: str) -> bool:
        return actual != nueva

    @staticmethod
    def cumpleRequisitos(contrasena: str) -> bool:

        if len(contrasena) < 8:
            return False
        if not re.search(r"[A-Z]", contrasena):
            return False
        if not re.search(r"[a-z]", contrasena):
            return False
        if not re.search(r"\d", contrasena):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
            return False
        return True