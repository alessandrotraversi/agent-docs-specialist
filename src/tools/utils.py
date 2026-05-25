import re

def clean_diagram_code(code: str, identifier: str) -> str:
    """
    Remove blocos de código markdown (ex: ```mermaid ... ```) se o LLM os incluiu por engano.
    """
    code = code.strip()
    # Se começar com o identificador em bloco markdown, extrai apenas o conteúdo
    pattern = rf"```(?:{identifier})?\s*\n?(.*?)\s*```"
    match = re.search(pattern, code, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Se o LLM apenas repetiu o identificador no início da string sem backticks
    if code.lower().startswith(identifier.lower()):
        # Remove apenas o identificador inicial se não for parte da sintaxe (ex: 'mermaid graph TD')
        # Mas cuidado para não remover 'mermaid' se for o início legítimo da sintaxe em alguns casos.
        # No PlantUML é comum começar com @startuml. No Mermaid começa com o tipo de grafo.
        pass

    return code
