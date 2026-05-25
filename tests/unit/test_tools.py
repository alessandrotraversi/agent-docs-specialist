import os
from unittest.mock import patch, MagicMock
from src.tools.mermaid_tool import generate_mermaid_diagram, save_diagram_to_file
from src.tools.plantuml_tool import generate_plantuml_diagram, save_plantuml_to_file
from src.config import settings

def test_generate_mermaid_diagram():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "graph TD\nA-->B"
    
    with patch('src.tools.mermaid_tool.get_ollama_model', return_value=mock_llm):
        result = generate_mermaid_diagram.invoke({"description": "test", "diagram_type": "flowchart"})
        assert "graph TD" in result
        mock_llm.invoke.assert_called_once()

def test_save_diagram_to_file():
    filename = "test_diag.mmd"
    filepath = os.path.join(settings.OUTPUT_DOCS_DIR, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        
    result = save_diagram_to_file.invoke({"mermaid_code": "code", "filename": filename})
    assert os.path.exists(filepath)
    assert "Diagrama salvo em" in result
    
    with open(filepath, "r") as f:
        assert f.read() == "code"
    
    os.remove(filepath)

def test_generate_plantuml_diagram():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "@startuml\n@enduml"
    
    with patch('src.tools.plantuml_tool.get_ollama_model', return_value=mock_llm):
        result = generate_plantuml_diagram.invoke({"description": "test", "diagram_type": "C4Context"})
        assert "@startuml" in result
        mock_llm.invoke.assert_called_once()

def test_save_plantuml_to_file():
    filename = "test_diag.puml"
    filepath = os.path.join(settings.OUTPUT_DOCS_DIR, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        
    save_plantuml_to_file.invoke({"plantuml_code": "puml code", "filename": filename})
    assert os.path.exists(filepath)
    
    with open(filepath, "r") as f:
        assert f.read() == "puml code"
    
    os.remove(filepath)
