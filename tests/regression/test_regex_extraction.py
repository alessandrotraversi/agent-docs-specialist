from unittest.mock import patch
from src.agent.doc_generator_agent import update_memory_node

def test_regression_adr_extraction_robustness():
    """
    Regressão: Garante que a extração de decisões do ADR funcione com diferentes estilos de Markdown.
    """
    adr_content = """
    # ADR 1: Escolha do Banco
    
    **1. Título**: PostgreSQL para Persistência
    **2. Contexto**: Precisamos de ACID.
    **3. Decisão**: Usar Postgres via LocalStack.
    """
    
    state = {"adr": adr_content, "prd": ""}
    
    with patch('src.memory.repository.MemoryRepository.add_decision') as mock_add, \
         patch('src.memory.repository.MemoryRepository.update_project_context'):
        
        update_memory_node(state)
        
        mock_add.assert_called_once()
        args, kwargs = mock_add.call_args
        assert kwargs['title'] == "PostgreSQL para Persistência"
        assert kwargs['decision'] == "Usar Postgres via LocalStack."

def test_regression_adr_extraction_numeric_list():
    """
    Regressão: Garante que a extração funcione com listas numeradas (ex: 1. Título).
    """
    adr_content = """
    # ADR 1
    1. Título: FastAPI
    2. Status: Proposto
    3. Decisão: Usar FastAPI para a API.
    """
    state = {"adr": adr_content, "prd": ""}
    
    with patch('src.memory.repository.MemoryRepository.add_decision') as mock_add, \
         patch('src.memory.repository.MemoryRepository.update_project_context'):
        
        update_memory_node(state)
        
        mock_add.assert_called_once()
        args, kwargs = mock_add.call_args
        assert kwargs['title'] == "FastAPI"
        assert kwargs['decision'] == "Usar FastAPI para a API."
