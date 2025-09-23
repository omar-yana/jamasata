from abc import ABC, abstractmethod
from apunte import Apunte

class InterfazRepositorioApunte(ABC):

    @abstractmethod
    def agregar(self, apunte: Apunte):
        pass

    @abstractmethod
    def modificar(self, id: str, apunte: Apunte):
        pass

    @abstractmethod
    def eliminar(self, id: str):
        pass

    @abstractmethod
    def obtener(self, id: str):
        pass

    @abstractmethod
    def listar(self):
        pass
