from abc import ABC, abstractmethod
from myapp.models.autor import UsuarioGeneral, AgenteIA, Admin


# 1. Interfaz Abstracta
class FabricaAutor(ABC):
    @abstractmethod
    def crear_autor(self, **kwargs):
        pass

# 2. Fabrica de Usuarios
class FabricaUsuario(FabricaAutor):
    def crear_autor(self, **kwargs):
        # Usamos UsuarioGeneral porque es la que tiene email y password
        return UsuarioGeneral(
            nombre=kwargs.get("nombre"),
            email=kwargs.get("email"),
            password=kwargs.get("password")
        )

# 3. Fabrica de Agentes IA
class FabricaAgenteIA(FabricaAutor):
    def crear_autor(self, **kwargs):
        return AgenteIA(
            nombre=kwargs.get("nombre"),
            proveedor=kwargs.get("proveedor", "OpenAI") # Valor por defecto
        )
#Fabrica de Admins
class FabricaAdmin(FabricaAutor):
    def crear_autor(self, **kwargs):
        return Admin(
            nombre=kwargs.get("nombre"),
            email=kwargs.get("email"),
            password=kwargs.get("password")
        )