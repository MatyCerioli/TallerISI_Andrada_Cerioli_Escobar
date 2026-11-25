from abc import ABC, abstractmethod

#Interfaz EstrategiaLLM
class EstrategiaLLM(ABC):
    "Interfaz del patron Strategy la cual se comunica con los modelos de IA"
   
    #metodo de la interfaz
    @abstractmethod
    def generarRespuesta(self, prompt: str) -> str:
        pass

#Clases hijas que heredan el metodo del padre sobre generarRespuesta
class OpenAIStrategy(EstrategiaLLM):
    def generarRespuesta(self, prompt: str) -> str:
        return f"[OpenAI] Respuesta para: {prompt}"

class GeminiStrategy(EstrategiaLLM):
    def generarRespuesta(self, prompt: str) -> str:
        return f"[Gemini] Respuesta para: {prompt}"

class ModeloLocalStrategy(EstrategiaLLM):
    def generarRespuesta(self, prompt: str) -> str:
        return f"[ModeloLocal] Respuesta para: {prompt}"