import base64
from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type

class HashPasswordHelper:

    HASH_COMPLETE_GLOBAL = None
    HASH_SALT_GLOBAL = None
    passwordHasherAleatorio = PasswordHasher(
        time_cost=2,       # número de iteraciones
        memory_cost=102400, # memoria usada en KB (100 MB)
        parallelism=8,     # núm. de hilos
        hash_len=32,       # longitud del hash
        salt_len=16        # longitud de la sal
    )

    @classmethod
    def generarHashAleatorio(cls, contrasena: str) -> str:
        HASH_COMPLETE_GLOBAL = None
        HASH_SALT_GLOBAL = None
        hashCompleto = cls.passwordHasherAleatorio.hash(contrasena)
        cls.HASH_COMPLETE_GLOBAL = hashCompleto
        hashPartes = hashCompleto.split('$')
        saltBase64 = hashPartes[-2]
        cls.HASH_SALT_GLOBAL = saltBase64
        return saltBase64

    @classmethod
    def generarHash(cls, contrasena: str, salt: str) -> str:
        contrasenaBytes = contrasena.encode()
        saltBytes = cls.decodeSalt(salt)
        hashBytes = hash_secret_raw(
            secret=contrasenaBytes,
            salt=saltBytes,
            time_cost=cls.passwordHasherAleatorio.time_cost,
            memory_cost=cls.passwordHasherAleatorio.memory_cost,
            parallelism=cls.passwordHasherAleatorio.parallelism,
            hash_len=cls.passwordHasherAleatorio.hash_len,
            type=Type.ID  # Argon2id
        )
        hashBase64 = base64.b64encode(hashBytes).decode().rstrip("=")
        return f"$argon2id$v=19$m=102400,t=2,p=8${salt}${hashBase64}"

    @classmethod
    def verificarHash(cls, hashGenerado: str, contrasena: str) -> bool:
        try:
            return cls.passwordHasherAleatorio.verify(hashGenerado, contrasena)
        except:
            return False
    @classmethod
    def decodeSalt(cls, saltBase64: str) -> bytes:
        saltBase64 = saltBase64.strip()
        padding = 4 - (len(saltBase64) % 4)
        if padding != 4:
            saltBase64 += "=" * padding
        saltBytes = base64.b64decode(saltBase64)
        return saltBytes