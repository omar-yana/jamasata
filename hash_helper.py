import hashlib

class HashHelper:
    @staticmethod
    def generarHashSha256(texto: str) -> str:
        textoBytes = texto.encode('utf-8')
        hashStr = hashlib.sha256(textoBytes).hexdigest()
        return hashStr