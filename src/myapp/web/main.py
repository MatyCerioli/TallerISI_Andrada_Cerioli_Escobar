from flask import Blueprint, render_template, request, redirect, url_for, session
from myapp.models.publicacion import Pregunta, Respuesta
from myapp.models.autor import Usuario
from myapp.extensions import db

web_main_bp = Blueprint("web_main", __name__)

@web_main_bp.route("/")
def index():
    # Traemos todas las preguntas de la base de datos
    preguntas = Pregunta.query.order_by(Pregunta.fecha_publicacion.desc()).all()
    
    # Renderizamos el HTML pasandole la lista
    return render_template("index.html", preguntas=preguntas)


@web_main_bp.route("/preguntar", methods=["POST"])
def preguntar():
    # Verificamos que esté logueado
    if not session.get('user_id'):
        return redirect(url_for("web_auth.login"))
    
    titulo = request.form.get("titulo")
    cuerpo = request.form.get("cuerpo")
    
    # Buscamos al autor logueado
    autor = Usuario.query.get(session['user_id'])
    
    # Creamos la pregunta
    nueva_pregunta = Pregunta(titulo=titulo, cuerpo=cuerpo, autor=autor)
    db.session.add(nueva_pregunta)
    db.session.commit()
    
    return redirect(url_for("web_main.index"))




@web_main_bp.route("/responder/<int:pregunta_id>", methods=["POST"])
def responder(pregunta_id):
    if not session.get('user_id'):
        return redirect(url_for("web_auth.login"))
    
    cuerpo = request.form.get("cuerpo")
    autor = Usuario.query.get(session['user_id'])
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    
    nueva_respuesta = Respuesta(cuerpo=cuerpo, autor=autor, pregunta=pregunta)
    db.session.add(nueva_respuesta)
    db.session.commit()
    
    return redirect(url_for("web_main.index"))