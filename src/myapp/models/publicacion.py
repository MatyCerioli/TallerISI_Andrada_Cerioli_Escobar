from datetime import datetime
from myapp.extensions import db

# 1. Clase base
class Publicacion:
    

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    autor_id = db.Column(db.Integer, db.ForeignKey("autores.id"), nullable=False)
    

# 2. Subclase "Pregunta"
class Pregunta(Publicacion, db.Model):
    __tablename__ = "preguntas"
    
    titulo = db.Column(db.String(200), nullable=False)

    autor = db.relationship("Autor", back_populates="publicaciones")

    #  Relacion de composicion con Respuesta
    respuestas = db.relationship(
        "Respuesta", 
        back_populates="pregunta", 
        cascade="all, delete-orphan" # Composicion: si se borra la pregunta, se borran sus respuestas
    )

    def __repr__(self):
        return f"<Pregunta {self.titulo}>"

# 3. Subclase "Respuesta"
class Respuesta(Publicacion, db.Model):
    __tablename__ = "respuestas"
    
    es_aceptada = db.Column(db.Boolean, default=False)

    autor = db.relationship("Autor", back_populates="publicaciones")

    # Relacion bidireccional
    pregunta_id = db.Column(db.Integer, db.ForeignKey("preguntas.id"), nullable=False)
    pregunta = db.relationship("Pregunta", back_populates="respuestas")

    def __repr__(self):
        return f"<Respuesta {self.id}>"