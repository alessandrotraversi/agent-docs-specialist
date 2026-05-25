from src.config import settings

def test_settings_load():
    """Verifica se as configurações básicas são carregadas corretamente."""
    assert settings.OLLAMA_MODEL is not None
    assert settings.OUTPUT_DOCS_DIR is not None

def test_output_dir_exists():
    """Verifica se o diretório de saída está configurado."""
    assert ".outputs" in str(settings.OUTPUT_DOCS_DIR)
