
from dao.interfaz_repositorio_apunte import InterfazRepositorioApunte

class RepositorioApunte(InterfazRepositorioApunte):
    APUNTES = []

    def agregar(self, apunte):
        RepositorioApunte.APUNTES.append(apunte)

    def modificar(self, id: str, apunte):
        for idx, a in enumerate(RepositorioApunte.APUNTES):
            if a.id == id:
                RepositorioApunte.APUNTES[idx] = apunte
                return
        raise ValueError(f"No se encontró apunte con id: {id}")

    def eliminar(self, id: str):
        for idx, a in enumerate(RepositorioApunte.APUNTES):
            if a.id == id:
                RepositorioApunte.APUNTES.pop(idx)
                return
        raise ValueError(f"No se encontró apunte con id: {id}")

    def listar(self):
        return [a.to_dict() for a in RepositorioApunte.APUNTES]

    def obtenerPorId(self, id: str):
        for a in RepositorioApunte.APUNTES:
            if a.id == id:
                return a
        return None