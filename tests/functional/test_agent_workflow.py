from unittest.mock import patch, MagicMock
from src.agent.doc_generator_agent import create_doc_agent

def test_agent_workflow_structure():
    # Cria o agente sem checkpointer para teste de estrutura
    agent = create_doc_agent()
    assert agent is not None
    # Verifica se os nós esperados existem no grafo (via inspeção do objeto, se possível)
    # No LangGraph, podemos ver os nós em agent.nodes
    assert "generate_prd" in agent.nodes
    assert "generate_adr" in agent.nodes
    assert "update_memory" in agent.nodes

def test_agent_invocation_logic():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Mock Content"
    
    with patch('src.agent.doc_generator_agent.get_ollama_model', return_value=mock_llm), \
         patch('src.memory.repository.MemoryRepository.get_formatted_history', return_value="History"), \
         patch('src.memory.repository.MemoryRepository.add_decision'), \
         patch('src.memory.repository.MemoryRepository.update_project_context'), \
         patch('src.agent.doc_generator_agent.extract_and_save_diagrams'):
        
        agent = create_doc_agent()
        initial_state = {
            "interview_text": "Sample Interview",
            "history": "",
            "prd": "",
            "adr": "",
            "fdd": "",
            "design_doc": ""
        }
        
        # Executa apenas um passo ou o fluxo completo com mocks
        result = agent.invoke(initial_state)
        
        assert result["prd"] == "Mock Content"
        assert result["adr"] == "Mock Content"
        assert result["design_doc"] == "Mock Content"
