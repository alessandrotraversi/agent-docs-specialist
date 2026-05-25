import sys
import os

# Adiciona o diretório raiz ao path para permitir importações do src
sys.path.append(os.getcwd())

from src.tools.mermaid_tool import generate_mermaid_diagram, save_diagram_to_file
from src.tools.plantuml_tool import generate_plantuml_diagram, save_plantuml_to_file

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/tools/generate_diagram_cli.py \"descrição do diagrama\" [tipo] [arquivo_saida]")
        print("Tipos Mermaid: flowchart, sequence, class, state, er, gantt, pie")
        print("Tipos PlantUML: C4Context, C4Container, C4Component")
        return

    description = sys.argv[1]
    diagram_type = sys.argv[2] if len(sys.argv) > 2 else "flowchart"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "diagrama"

    print(f"--- Gerando diagrama {diagram_type} ---")
    print(f"Descrição: {description}")
    
    try:
        if diagram_type.startswith("C4"):
            code = generate_plantuml_diagram.invoke({"description": description, "diagram_type": diagram_type})
            print("\nCódigo PlantUML Gerado:")
            print("-------------------")
            print(code)
            print("-------------------")
            result = save_plantuml_to_file.invoke({"plantuml_code": code, "filename": output_file})
        else:
            code = generate_mermaid_diagram.invoke({"description": description, "diagram_type": diagram_type})
            print("\nCódigo Mermaid Gerado:")
            print("-------------------")
            print(code)
            print("-------------------")
            result = save_diagram_to_file.invoke({"mermaid_code": code, "filename": output_file})
            
        print(f"\n{result}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
