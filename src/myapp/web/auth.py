from flask import Blueprint, render_template, request, redirect, url_for, session
from myapp.extensions import db
from myapp.models.autor import Usuario
from myapp.services.factories import FabricaUsuario

web_auth_bp = Blueprint("web_auth", __name__, url_prefix="/auth")

@web_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # 1. Recibimos los datos del formulario HTML (no JSON)
        email = request.form.get("email")
        password = request.form.get("password")
        
        # 2. Buscamos al usuario en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        
        # 3. Verificamos si existe y si la contraseña es correcta
        if usuario and usuario.password == password:
            # Login exitoso
            session['user_id'] = usuario.id #guardamos esto para que el servidor recuerde al usuario
            session['user_name'] = usuario.nombre
            return redirect(url_for("web_main.index"))
        else:
            # Login fallido
            return render_template("auth/login.html", error="Email o password incorrectos")
            
    # Si es un GET, mostramos el formulario vacio
    return render_template("auth/login.html")

@web_auth_bp.route("/logout")
def logout():
    session.clear() #borra los datos de la session
    return redirect(url_for("web_auth.login"))


@web_auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Verificamos si ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template("auth/register.html", error="El email ya está en uso")
            
        # Usamos tu Fabrica (Issue #5)
        fabrica = FabricaUsuario()
        nuevo_usuario = fabrica.crear_autor(nombre=nombre, email=email, password=password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Redirigimos al login tras registrarse con exito
        return redirect(url_for("web_auth.login"))
        
    return render_template("auth/register.html")