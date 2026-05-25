from langchain_core.tools import tool
from src.llm.ollama_loader import get_ollama_model
from langchain_core.messages import HumanMessage
from src.tools.utils import clean_diagram_code

@tool
def generate_plantuml_diagram(description: str, diagram_type: str = "C4Context") -> str:
    """
    Gera o código PlantUML para um diagrama com base em uma descrição e tipo.
    Focado principalmente em diagramas C4 (C4Context, C4Container, C4Component).
    """
    llm = get_ollama_model(temperature=0)
    
    prompt = f"""
    Você é um especialista em PlantUML e C4 Model. Sua tarefa é gerar APENAS o código PlantUML para o seguinte diagrama:
    
    Tipo: {diagram_type}
    Descrição: {description}
    
    REGRAS CRÍTICAS:
    1. Retorne APENAS o código do diagrama começando com '@startuml' e terminando com '@enduml'.
    2. NÃO use blocos de código markdown (```plantuml).
    3. NÃO use explicações antes ou depois.
    4. Use as bibliotecas C4-PlantUML adequadas.
    
    Exemplo Correto C4Context:
    @startuml
    !include https://raw.githubusercontent.com/plantuml-office/C4-PlantUML/master/C4_Context.puml
    
    title Diagrama de Contexto de Sistema
    
    Person(customer, "Cliente", "Um usuário do sistema")
    System(system, "Sistema", "Descrição do sistema")
    
    Rel(customer, system, "Usa", "HTTPS")
    @enduml
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return clean_diagram_code(response.content, "plantuml")

@tool
def save_plantuml_to_file(plantuml_code: str, filename: str) -> str:
    """
    Salva um código PlantUML em um arquivo .puml na pasta de documentos.
    """
    import os
    from src.config import settings
    
    output_dir = settings.OUTPUT_DOCS_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not filename.endswith(".puml"):
        filename += ".puml"
        
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(plantuml_code)
        
    return f"Diagrama PlantUML salvo em: {file_path}"
