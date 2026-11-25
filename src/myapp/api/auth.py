from flask import Blueprint, request, jsonify
from myapp.extensions import db
from myapp.services.factories import FabricaUsuario, FabricaAdmin
from myapp.models.autor import Autor
from myapp.models.autor import Usuario

api_auth_bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")

@api_auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if not data or not data.get("nombre") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan datos obligatorios (nombre, email, password)"}), 400

    usuario_existente = Usuario.query.filter_by(email=data["email"]).first()
    if usuario_existente:
        return jsonify({"error": "El email ya esta registrado"}), 400

    # Usamos la fabrica (Issue #5)
    fabrica = FabricaUsuario()
    nuevo_usuario = fabrica.crear_autor(
        nombre=data["nombre"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado con éxito",
        "usuario": {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "email": nuevo_usuario.email,
            "tipo": nuevo_usuario.tipo
        }
    }), 201




#Para la verificacion del admin usamos una contraseña establecida "super-secreto-123"
@api_auth_bp.route("/register-admin", methods=["POST"])
def register_admin():
    # 1. Verificamos la clave secreta (proteccion)
    token = request.headers.get("X-Admin-Token")
    if token != "super-secreto-123":
        return jsonify({"error": "No autorizado. Falta la clave de admin."}), 401

    data = request.get_json()
    if not data or not data.get("nombre") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan datos"}), 400

    usuario_existente = Usuario.query.filter_by(email=data["email"]).first()
    if usuario_existente:
        return jsonify({"error": "El email ya esta registrado"}), 400

    # 2. Usamos la Fabrica de Admin
    fabrica = FabricaAdmin()
    nuevo_admin = fabrica.crear_autor(
        nombre=data["nombre"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(nuevo_admin)
    db.session.commit()

    return jsonify({
        "mensaje": "Administrador creado con exito",
        "admin": {
            "id": nuevo_admin.id,
            "nombre": nuevo_admin.nombre,
            "email": nuevo_admin.email,
            "tipo": nuevo_admin.tipo
        }
    }), 201