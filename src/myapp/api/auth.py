from flask import Blueprint, request, jsonify
from myapp.extensions import db
from myapp.services.factories import FabricaUsuario, FabricaAdmin
from myapp.models.autor import Autor, Usuario, AgenteIA
from myapp.services.strategies import OpenAIStrategy 
from myapp.services.respuestaAutomatica import ServicioRespuestaAutomatica
from myapp.models.publicacion import Pregunta

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
        "mensaje": "Usuario creado con exito",
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


#Ruta para crear un agenteIA
@api_auth_bp.route("/crear-agente-ia", methods=["POST"])
def crear_agente_ia():
    # Creamos al agente (como si fuera un usuario)
    agente = AgenteIA(nombre="Asistente-IA", modelo="OpenAI")
    db.session.add(agente)
    db.session.commit()
    return jsonify({"mensaje": "Agente IA creado con exito", "id": agente.id}), 201

@api_auth_bp.route("/ia/responder-todo", methods=["POST"])
def responder_todo():
    # 1. Buscamos un AgenteIA
    agente = AgenteIA.query.first()
    if not agente:
        return jsonify({"error": "No hay Agente IA en la base de datos"}), 404

    # 2. Le inyectamos la Estrategia (Patron Strategy)
    agente.set_estrategia(OpenAIStrategy())

    # 3. Instanciamos el Servicio
    servicio = ServicioRespuestaAutomatica(agente=agente, etiqueta_disparo="#ia-help")

    # 4. Buscamos todas las preguntas
    preguntas = Pregunta.query.all()

    # 5. se evalua que preguntas necesitan respuesta y genera los objetos Respuesta
    respuestas = servicio.atenderPendientes(preguntas)

    # 6. Guardamos las respuestas generadas en la base de datos
    for r in respuestas:
        db.session.add(r)
    db.session.commit()

    return jsonify({"mensaje": f"Se generaron {len(respuestas)} respuestas automáticas."}), 200