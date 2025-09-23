import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class SymmetricEncryptionHelper:
    DATA_FILE = "data_file.jama"
    def __init__(self, claveDerivadaArgon2: str):
        hashBase64 = claveDerivadaArgon2.split('$')[-1]
        print("$$$$$$$$$$$#########")
        print(hashBase64)
        hashBase64 = self.tobase64Relleno(hashBase64)
        print(hashBase64)
        hashBytes = base64.b64decode(hashBase64)
        self.clave = hashBytes[:32]

    def tobase64Relleno(self, hash: str) -> str:
        return hash + "=" * (-len(hash) % 4)

    @classmethod
    def existeDataFile(cls):
        return os.path.exists(cls.DATA_FILE)

    def cifrar(self, dato: dict, archivo: str) -> bool:
        #contenido = json.dumps(dato).encode('utf-8')

        contenido = json.dumps(dato.get("apuntes", [])).encode('utf-8')

        relleno = padding.PKCS7(128).padder()# Padding (AES requiere bloques de 16 bytes)
        contenidoRelleno = relleno.update(contenido) + relleno.finalize()

        vectorInicializaciónAleatorio = os.urandom(16)

        cipher = Cipher(algorithms.AES(self.clave), modes.CBC(vectorInicializaciónAleatorio))
        encryptor = cipher.encryptor()
        cifrado = encryptor.update(contenidoRelleno) + encryptor.finalize()
        contenidoCifrado = (vectorInicializaciónAleatorio + cifrado).hex()

        dato["apuntes"] = contenidoCifrado

        with open(archivo, "w") as file:
            #file.write(contenidoCifrado)
            json.dump(dato, file, ensure_ascii=False, indent=2)

        print(f"Archivo cifrado creado y sobrescrito si existe: {archivo}")
        return True

    def descifrar(self, archivo: str) -> dict:
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"El archivo {archivo} no existe.")

        with open(archivo, "r") as file:
            #contenidoCifrado = file.read()
            dato = json.load(file)

        contenidoCifrado = bytes.fromhex(dato["apuntes"])

        vectorInicializaciónAleatorio = contenidoCifrado[:16]
        cifrado = contenidoCifrado[16:]

        cipher = Cipher(algorithms.AES(self.clave), modes.CBC(vectorInicializaciónAleatorio))
        decryptor = cipher.decryptor()
        contenidoRelleno = decryptor.update(cifrado) + decryptor.finalize()

        sinRelleno = padding.PKCS7(128).unpadder()
        contenido = sinRelleno.update(contenidoRelleno) + sinRelleno.finalize()

        dato["apuntes"] = json.loads(contenido)
        return dato

    @staticmethod
    def obtenerClaveDerivadaArgon2(archivo: str) -> str:
        with open(archivo, "r", encoding="utf-8") as file:
            dato = json.load(file)
        return dato.get("hash", "")
