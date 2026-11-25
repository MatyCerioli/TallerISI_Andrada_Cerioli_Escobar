from myapp.extensions import db

class Autor(db.Model):
    __tablename__ = "autores"


    #Atributos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50))

    #Relacion con preguntas y respuestas (no con publicacion porque no la hicimos como dbModel)
    publicaciones = db.relationship("Pregunta", back_populates="autor")
    respuestas = db.relationship("Respuesta", back_populates="autor")

    #configuracion de herencia SQLALCHEMY
    __mapper_args__ = {
        "polymorphic_identity": "autor",
        "polymorphic_on": tipo,
    }

    #simil toString en java
    def __repr__(self):
        return f"<Autor {self.nombre}>"


#Clase AgenteIA (hereda de autor)
class AgenteIA(Autor):
    __tablename__ = "agentes_ia"

    id = db.Column(db.Integer, db.ForeignKey("autores.id"), primary_key=True)
    proveedor = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "agente_ia"}

    def __repr__(self):
        return f"<AgenteIA {self.nombre}>"




#Clase Usuario (Hereda de autor, agrega email y password)
class Usuario(Autor):
    __tablename__ = "usuarios"

    #La clave primaria es a su vez clave foranea y referencia a "autores"
    id = db.Column(db.Integer, db.ForeignKey("autores.id"), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "usuario"}


#Subclase Admin que hereda de Usuario
class Admin(Usuario):
    __tablename__ = "admins"

    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}

    #funcion para moderar el contenido(eliminar)
    def moderar_contenido(self, publicacion):
        db.session.delete(publicacion)
        db.session.commit()


#Subclase UsuarioGeneral que hereda de Usuario
class UsuarioGeneral(Usuario):
    __tablename__ = "usuarios_generales"
    
    id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "usuario_general"}

    # Criterio de la Issue #1: Un usuario debe poder votar
    def votar(self, publicacion, valor):
        # Aca ira la logica del voto mas adelante
        pass