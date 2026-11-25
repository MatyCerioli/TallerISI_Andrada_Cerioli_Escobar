# tests/test_agente_ia.py
import pytest
from myapp import create_app
from myapp.extensions import db
from myapp.models.autor import AgenteIA
from myapp.models.category import Category
from myapp.models.publicacion import Pregunta, Respuesta
from myapp.services.llm import MockLLMStrategy, GeminiStrategy, OpenAIStrategy


@pytest.fixture
def db_session():
    """Fixture autosuficiente de base de datos en memoria para los tests de AgenteIA."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


def test_agente_ia_responder_con_mock_llm(db_session):
    """Verifica que AgenteIA genere una Respuesta asociada a la Pregunta utilizando una EstrategiaLLM."""
    
    # 1. Crear categoría obligatoria
    categoria = Category(nombre="Python")
    db_session.add(categoria)
    db_session.commit()

    # 2. Crear AgenteIA y la Pregunta
    bot = AgenteIA(nombre="BotAsistente", modelo="gemini")
    db_session.add(bot)
    db_session.commit()

    pregunta = Pregunta(
        titulo="¿Cómo funciona el patrón Strategy?",
        cuerpo="Quisiera entender el patrón Strategy en Python.",
        autor=bot,
        category=categoria
    )
    db_session.add(pregunta)
    db_session.commit()

    # 3. Configurar estrategia Mock
    estrategia_mock = MockLLMStrategy(respuesta_fija="El patrón Strategy encapsula algoritmos intercambiables.")
    bot.set_estrategia(estrategia_mock)

    # 4. Generar la respuesta automática
    respuesta = bot.responder(pregunta)
    db_session.add(respuesta)
    db_session.commit()

    # 5. Aserciones
    assert respuesta.cuerpo == "El patrón Strategy encapsula algoritmos intercambiables."
    assert respuesta.autor_id == bot.id
    assert respuesta.pregunta_id == pregunta.id
    assert len(pregunta.respuestas) == 1


def test_agente_ia_sin_estrategia_lanza_error(db_session):
    """Verifica que AgenteIA lance un ValueError si intenta responder sin estrategia configurada."""
    bot = AgenteIA(nombre="BotIncompleto")
    categoria = Category(nombre="Flask")
    pregunta = Pregunta(titulo="Duda", cuerpo="Detalle", autor=bot, category=categoria)

    with pytest.raises(ValueError, match="No se ha configurado una EstrategiaLLM"):
        bot.responder(pregunta)
