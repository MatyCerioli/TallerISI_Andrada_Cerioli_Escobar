# src/myapp/models/publicacion.py
from datetime import datetime
from myapp.extensions import db


# 1. Clase base Publicacion (con configuración polimórfica)
class Publicacion(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Discriminador para herencia polimórfica (Requerido por SQLAlchemy)
    tipo = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "publicacion",
    }

    # Relación bidireccional polimórfica con Autor
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("autores.id"),
        nullable=False
    )

    autor = db.relationship(
        "Autor",
        back_populates="publicaciones"
    )


# 2. Subclase "Pregunta"
class Pregunta(Publicacion):
    __tablename__ = "preguntas"

    id = db.Column(
        db.Integer,
        db.ForeignKey("publications.id"),
        primary_key=True
    )

    titulo = db.Column(db.String(200), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "pregunta",
    }

    # Relación de composición con Respuesta
    respuestas = db.relationship(
        "Respuesta",
        back_populates="pregunta",
        cascade="all, delete-orphan",
        foreign_keys="Respuesta.pregunta_id"
    )

    # Categorías y Etiquetas (Issue #3)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship(
        "Category",
        backref=db.backref("preguntas", lazy=True)
    )

    tags = db.relationship(
        "Tag",
        secondary="question_tags",
        backref=db.backref("preguntas", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Pregunta {self.titulo}>"


# 3. Subclase "Respuesta"
class Respuesta(Publicacion):
    __tablename__ = "respuestas"

    id = db.Column(
        db.Integer,
        db.ForeignKey("publications.id"),
        primary_key=True
    )

    es_aceptada = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "respuesta",
    }

    # Relación bidireccional con Pregunta (especificando FK)
    pregunta_id = db.Column(
        db.Integer,
        db.ForeignKey("preguntas.id"),
        nullable=False
    )

    pregunta = db.relationship(
        "Pregunta",
        back_populates="respuestas",
        foreign_keys=[pregunta_id]
    )

    def __repr__(self):
        return f"<Respuesta {self.id}>"
