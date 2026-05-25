from langchain_ollama import ChatOllama
from src.config import settings

def get_ollama_model(model_name=None, temperature=None):
    """
    Inicializa e retorna o modelo ChatOllama usando configurações centralizadas.
    """
    return ChatOllama(
        model=model_name or settings.OLLAMA_MODEL,
        temperature=temperature if temperature is not None else settings.OLLAMA_TEMPERATURE,
        base_url=settings.OLLAMA_BASE_URL,
    )
