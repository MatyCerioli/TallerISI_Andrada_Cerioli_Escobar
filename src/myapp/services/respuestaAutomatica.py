from datetime import datetime, timedelta
from typing import  Any, List

from myapp.models.publicacion import Pregunta
from myapp.models.autor import AgenteIA

class ServicioRespuestaAutomatica:
    "Servicio que analisa preguntas y da respuestas automáticas con IA."

    def __init__(
        self,
        agente: "AgenteIA",
        etiqueta_disparo: str = "#ia-help",
        tiempo_maximo_sin_respuesta: timedelta = timedelta(hours=24),
    ):
        self.agente = agente
        self.etiquetaDisparo = etiqueta_disparo
        self.tiempoMaximoSinRespuesta = tiempo_maximo_sin_respuesta

    def evaluarPregunta(self, pregunta: Pregunta) -> bool:
        "Evalua si la pregunta contiene #ia-help o supero el tiempo maximo sin respuesta."
        # 1. Verificar si alguna etiqueta coincide con #ia-help
        etiquetas = getattr(pregunta, "etiquetas", [])
        tiene_etiqueta = any(
            getattr(etiqueta, "nombre", str(etiqueta)) == self.etiquetaDisparo
            for etiqueta in etiquetas
        )
        en_texto = (
            self.etiquetaDisparo in (pregunta.titulo or "")
            or self.etiquetaDisparo in (pregunta.cuerpo or "")
        )   
        if tiene_etiqueta or en_texto:
            return True

        # 2. Verificaa si no tiene respuestas y si supero la antigüedad máxima
        sin_respuestas = len(pregunta.respuestas) == 0
        fecha_pub = pregunta.fecha_publicacion

        if sin_respuestas and isinstance(fecha_pub, datetime):
            if (datetime.utcnow() - fecha_pub) >= self.tiempoMaximoSinRespuesta:
                return True
    
        return False
    
    def atenderPendientes(self, preguntas: List[Pregunta]) -> List[Any]:
        "Recorre las preguntas pendientes y genera respuesta automática en las que correspondan."
        respuestas_generadas = []
        for pregunta in preguntas:
            if self.evaluarPregunta(pregunta):
                # Usa responderPregunta (Issue #6) o responder (diagrama UML)
                if hasattr(self.agente, "responderPregunta"):
                    respuesta = self.agente.responderPregunta(pregunta)
                else:
                    respuesta = self.agente.responder(pregunta)
                respuestas_generadas.append(respuesta)
        return respuestas_generadas