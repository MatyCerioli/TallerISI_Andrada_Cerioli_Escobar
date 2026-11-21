from abc import ABC, abstractmethod
# Importamos las clases que definió tu compañero en la Issue #1
# (Aunque todavía no existan, Python no dará error hasta que se ejecute)
from myapp.models.autor import Usuario, AgenteIA

# 1. Crear clase abstracta/interfaz "fabricaAutor" con método 'CrearAutor()'
class FabricaAutor(ABC):
    
    @abstractmethod
    def crear_autor(self, **kwargs):
        """
        Método abstracto que deben implementar las fábricas concretas.
        Recibe los datos necesarios para crear el autor.
        """
        pass

# 2. Implementar 'fabricaUsuario' para instanciar usuarios humanos
class FabricaUsuario(FabricaAutor):
    
    def crear_autor(self, **kwargs):
        # Asumimos que el modelo Usuario recibe nombre, email y password (o rol)
        # Ojo: Ajustar los parámetros según cómo lo haga MatiCerioli en su Issue #1
        return Usuario(
            nombre=kwargs.get("nombre"),
            email=kwargs.get("email"),
            password_hash=kwargs.get("password"), # O como se llame el campo
            rol="general" # Por defecto, o se puede pasar por parámetro
        )

# 3. Implementar 'fabricaAgenteIA' para instanciar agentes automáticos
class FabricaAgenteIA(FabricaAutor):
    
    def crear_autor(self, **kwargs):
        # El AgenteIA solo necesita un nombre (ej: "GPT-4")
        return AgenteIA(
            nombre=kwargs.get("nombre")
        )