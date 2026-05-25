from src.tools.utils import clean_diagram_code

def test_clean_diagram_code():
    # Caso 1: Bloco limpo
    assert clean_diagram_code("graph TD\nA-->B", "mermaid") == "graph TD\nA-->B"
    
    # Caso 2: Com blocos markdown
    assert clean_diagram_code("```mermaid\ngraph TD\nA-->B\n```", "mermaid") == "graph TD\nA-->B"
    
    # Caso 3: Com espaços e variações
    assert clean_diagram_code(" ```mermaid \n graph TD \n ``` ", "mermaid") == "graph TD"
    
    # Caso 4: PlantUML
    assert clean_diagram_code("```plantuml\n@startuml\n@enduml\n```", "plantuml") == "@startuml\n@enduml"

def test_extract_robustness():
    # Simula o que o agente faz
    import re
    text = "Aqui está o diagrama:\n```mermaid\ngraph TD\nA-->B```\nE outro:\n```PLANTUML\n@startuml\n@enduml\n```"
    
    mermaid_blocks = re.findall(r"```mermaid\s*\n?(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    assert len(mermaid_blocks) == 1
    assert mermaid_blocks[0].strip() == "graph TD\nA-->B"
    
    plantuml_blocks = re.findall(r"```plantuml\s*\n?(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    assert len(plantuml_blocks) == 1
    assert plantuml_blocks[0].strip() == "@startuml\n@enduml"

if __name__ == "__main__":
    test_clean_diagram_code()
    test_extract_robustness()
    print("Testes de robustez passariam!")
