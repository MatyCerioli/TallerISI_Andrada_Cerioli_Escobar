from myapp.extensions import db
question_tags = db.Table(
    'question_tags',
    db.Column('question_id', db.Integer, db.ForeignKey('preguntas.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    )
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category{self.nombre}>'
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.nombre}>'
    