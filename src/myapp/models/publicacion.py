from datetime import datetime
from myapp.extensions import db

# 1. Clase abstracta "Publicacion"
class Publicacion(db.Model):
    __abstract__ = True  # Esto indica que no crea tabla propia

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    autor_id = db.Column(db.Integer, db.ForeignKey("autor.id"), nullable=False)
    autor = db.relationship("Autor", back_populates="publicaciones")
    

# 2. Subclase "Pregunta"
class Pregunta(Publicacion):
    __tablename__ = "preguntas"
    
    titulo = db.Column(db.String(200), nullable=False)
    
    # 4 y 5. Relacion de composicion con Respuesta
    respuestas = db.relationship(
        "Respuesta", 
        back_populates="pregunta", 
        cascade="all, delete-orphan" # Composicion: si se borra la pregunta, se borran sus respuestas
    )

    def __repr__(self):
        return f"<Pregunta {self.titulo}>"

# 3. Subclase "Respuesta"
class Respuesta(Publicacion):
    __tablename__ = "respuestas"
    
    es_aceptada = db.Column(db.Boolean, default=False)
    
    # Relacion bidireccional
    pregunta_id = db.Column(db.Integer, db.ForeignKey("preguntas.id"), nullable=False)
    pregunta = db.relationship("Pregunta", back_populates="respuestas")

    def __repr__(self):
        return f"<Respuesta {self.id}>"