from datetime import datetime

class Apunte:
    def __init__(self, id: str, titulo: str, usuario: str, contrasena: str,
                 url: str = "", modificado: datetime = None,
                 caducidad: datetime = None, comentario: str = ""):
        self.id = id
        self.titulo = titulo
        self.usuario = usuario
        self.contrasena = contrasena
        self.url = url
        self.modificado = modificado if modificado else datetime.now()
        self.caducidad = caducidad
        self.comentario = comentario

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "url": self.url,
            "modificado": self.modificado.isoformat(),
            "caducidad": self.caducidad.isoformat() if self.caducidad else None,
            "comentario": self.comentario
        }

    @staticmethod
    def from_dict(data):
        modificado = datetime.fromisoformat(data["modificado"]) if data.get("modificado") else None
        caducidad = datetime.fromisoformat(data["caducidad"]) if data.get("caducidad") else None
        return Apunte(
            id=data.get("id", ""),  # ID viene del diccionario
            titulo=data.get("titulo", ""),
            usuario=data.get("usuario", ""),
            contrasena=data.get("contrasena", ""),
            url=data.get("url", ""),
            modificado=modificado,
            caducidad=caducidad,
            comentario=data.get("comentario", "")
        )