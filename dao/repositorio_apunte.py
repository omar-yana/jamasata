
from dao.interfaz_repositorio_apunte import InterfazRepositorioApunte

class RepositorioApunte(InterfazRepositorioApunte):
    APUNTES = []

    def agregar(self, apunte):
        RepositorioApunte.APUNTES.append(apunte)

    def modificar(self, id: str, apunte):
        for idx, apun in enumerate(RepositorioApunte.APUNTES):
            if apun['id'] == id:
                RepositorioApunte.APUNTES[idx] = apunte
                return
        raise ValueError(f"No se encontró apunte con id: {id}")

    def eliminar(self, id: str):
        for idx, apun in enumerate(RepositorioApunte.APUNTES):
            if apun['id'] == id:
                RepositorioApunte.APUNTES.pop(idx)
                return
        raise ValueError(f"No se encontró apunte con id: {id}")

    def listar(self):
        return RepositorioApunte.APUNTES

    def obtenerPorId(self, id: str):
        for apun in RepositorioApunte.APUNTES:
            if apun['id'] == id:
                return apun
        return None