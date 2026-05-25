from langchain_core.tools import tool
from src.llm.ollama_loader import get_ollama_model
from langchain_core.messages import HumanMessage
from src.tools.utils import clean_diagram_code

@tool
def generate_mermaid_diagram(description: str, diagram_type: str = "flowchart") -> str:
    """
    Gera o código Mermaid.js para um diagrama com base em uma descrição e tipo.
    Tipos suportados: flowchart, sequence, class, state, er, gantt, pie.
    """
    llm = get_ollama_model(temperature=0)  # Usar temperatura 0 para maior precisão na sintaxe
    
    prompt = f"""
    Você é um especialista em Mermaid.js. Sua tarefa é gerar APENAS o código Mermaid.js para o seguinte diagrama:
    
    Tipo: {diagram_type}
    Descrição: {description}
    
    REGRAS CRÍTICAS:
    1. Retorne APENAS o código do diagrama.
    2. NÃO use blocos de código markdown (```mermaid).
    3. NÃO use explicações antes ou depois.
    
    Exemplo Correto flowchart:
    graph TD
      A[Início] --> B{{Decisão}}
      B -- Sim --> C[Resultado 1]
      B -- Não --> D[Resultado 2]
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return clean_diagram_code(response.content, "mermaid")

@tool
def save_diagram_to_file(mermaid_code: str, filename: str) -> str:
    """
    Salva um código Mermaid em um arquivo .mmd na pasta de documentos.
    """
    import os
    from src.config import settings
    
    output_dir = settings.OUTPUT_DOCS_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not filename.endswith(".mmd"):
        filename += ".mmd"
        
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)
        
    return f"Diagrama salvo em: {file_path}"
