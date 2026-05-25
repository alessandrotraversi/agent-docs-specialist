from unittest.mock import patch
from src.memory.repository import MemoryRepository

def test_get_formatted_history_empty():
    with patch('src.memory.repository.MemoryRepository.get_all_decisions', return_value=[]), \
         patch('src.memory.repository.MemoryRepository.get_all_patterns', return_value=[]), \
         patch('src.memory.repository.MemoryRepository.get_project_context', return_value={}):
        
        result = MemoryRepository.get_formatted_history()
        assert result == ""

def test_get_formatted_history_with_data():
    decisions = [{"title": "DB Choice", "decision": "Postgres"}]
    patterns = [{"name": "Clean Arch", "description": "Separation of concerns"}]
    context = {"Project Name": "LocalFresh"}
    
    with patch('src.memory.repository.MemoryRepository.get_all_decisions', return_value=decisions), \
         patch('src.memory.repository.MemoryRepository.get_all_patterns', return_value=patterns), \
         patch('src.memory.repository.MemoryRepository.get_project_context', return_value=context):
        
        result = MemoryRepository.get_formatted_history()
        assert "Contexto do Projeto:" in result
        assert "LocalFresh" in result
        assert "Decisões Anteriores (ADRs):" in result
        assert "DB Choice: Postgres" in result
        assert "Padrões Identificados:" in result
        assert "Clean Arch: Separation of concerns" in result
