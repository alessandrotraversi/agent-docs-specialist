from unittest.mock import patch
from src.llm.ollama_loader import get_ollama_model

def test_get_ollama_model_defaults():
    with patch('src.llm.ollama_loader.ChatOllama') as mock_chat:
        get_ollama_model()
        mock_chat.assert_called_once()
        # Verifica se foi chamado com os parâmetros do settings (indiretamente via mock)
        args, kwargs = mock_chat.call_args
        assert 'model' in kwargs
        assert 'temperature' in kwargs
        assert 'base_url' in kwargs

def test_get_ollama_model_custom():
    with patch('src.llm.ollama_loader.ChatOllama') as mock_chat:
        get_ollama_model(model_name="test-model", temperature=0.1)
        args, kwargs = mock_chat.call_args
        assert kwargs['model'] == "test-model"
        assert kwargs['temperature'] == 0.1
