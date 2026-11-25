# src/myapp/services/llm.py
from abc import ABC, abstractmethod


# ==========================================
# Issue #4 & #6: Patron Strategy para los LLM
# ==========================================

class EstrategiaLLM(ABC):
    """
    Interfaz / Clase base abstracta para el Patron Strategy de LLM.
    """

    @abstractmethod
    def generarRespuesta(self, prompt: str) -> str:
        """Metodo abstracto que todas las estrategias concretas deben implementar."""
        pass


class OpenAIStrategy(EstrategiaLLM):
    """Estrategia concreta para integracion con OpenAI GPT."""

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generarRespuesta(self, prompt: str) -> str:
        # Aqui iria la llamada real a la API de OpenAI
        return f"[OpenAI - {self.model}] Respuesta generada automaticamente para: {prompt[:40]}..."


class GeminiStrategy(EstrategiaLLM):
    """Estrategia concreta para integracion con Google Gemini."""

    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model

    def generarRespuesta(self, prompt: str) -> str:
        # Aca iria la llamada real a la API de Gemini
        return f"[Gemini - {self.model}] Respuesta generada automaticamente para: {prompt[:40]}..."


class ModeloLocalStrategy(EstrategiaLLM):
    """Estrategia concreta para ejecucion de un modelo local (ej: Ollama / Llama3)."""

    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    def generarRespuesta(self, prompt: str) -> str:
        return f"[ModeloLocal - {self.model_name}] Respuesta simulada para: {prompt[:40]}..."


class MockLLMStrategy(EstrategiaLLM):
    """
    Estrategia Mock ideal para pruebas unitarias con Pytest.
    Permite probar el sistema sin depender de APIs ni gastar creditos.
    """

    def __init__(self, respuesta_fija: str = "Esta es una respuesta simulada por la IA para pruebas."):
        self.respuesta_fija = respuesta_fija

    def generarRespuesta(self, prompt: str) -> str:
        return self.respuesta_fija
