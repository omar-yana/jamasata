from argon2 import PasswordHasher

class HashPasswordHelper:

    HASH_GLOBAL = None
    passwordHasher = PasswordHasher(
        time_cost=2,       # número de iteraciones
        memory_cost=102400, # memoria usada en KB (100 MB)
        parallelism=8,     # núm. de hilos
        hash_len=32,       # longitud del hash
        salt_len=16        # longitud de la sal
    )

    @classmethod
    def generarHash(cls, contrasena: str) -> str:
        return cls.passwordHasher.hash(contrasena)

    @classmethod
    def verificarHash(cls, hashGenerado: str, contrasena: str) -> bool:
        try:
            return cls.passwordHasher.verify(hashGenerado, contrasena)
        except:
            return False