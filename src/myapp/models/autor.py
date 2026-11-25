from myapp.extensions import db

class Autor(db.Model):
    __tablename__ = "autores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))  # Discriminador para herencia polimórfica

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "autor",
    }

    # Relación para las preguntas (que apuntan a Pregunta)
    publicaciones = db.relationship("Pregunta", back_populates="autor")
    # Relación para las respuestas (que apuntan a Respuesta)
    respuestas = db.relationship("Respuesta", back_populates="autor")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nombre}>"


class Usuario(Autor):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, db.ForeignKey("autores.id"), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "usuario",
    }


class Admin(Usuario):
    
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class UsuarioGeneral(Usuario):
    
    __tablename__ = "usuarios_generales"
    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "usuario_general",
    }


# ==========================================
# Issue #6: Subclase AgenteIA (Hereda de Autor)
# ==========================================
class AgenteIA(Autor):
    __tablename__ = "agentes_ia"

    id = db.Column(db.Integer, db.ForeignKey("autores.id"), primary_key=True)
    modelo = db.Column(db.String(50), default="gemini")

    __mapper_args__ = {
        "polymorphic_identity": "agente_ia",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._estrategia = None

    @property
    def estrategia(self):
        return self._estrategia

    @estrategia.setter
    def estrategia(self, estrategia):
        self._estrategia = estrategia

    def set_estrategia(self, estrategia):
        """Asigna dinamicamente la estrategia LLM (Patron Strategy)."""
        self._estrategia = estrategia

    def responder(self, pregunta):
        """
        Genera y retorna un objeto Respuesta utilizando la estrategia LLM configurada.
        """
        if not self._estrategia:
            raise ValueError("No se ha configurado una EstrategiaLLM en el AgenteIA.")

        prompt = f"Titulo: {pregunta.titulo}\nPregunta: {pregunta.cuerpo}"
        
        cuerpo_generado = self._estrategia.generarRespuesta(prompt)

        from myapp.models.publicacion import Respuesta

        respuesta = Respuesta(
            cuerpo=cuerpo_generado,
            autor=self,
            pregunta=pregunta
        )
        return respuesta