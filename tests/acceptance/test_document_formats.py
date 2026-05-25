import os
from src.agent.doc_generator_agent import save_docs

def test_save_docs_acceptance():
    """
    Teste de aceitação: Verifica se o sistema é capaz de salvar todos os documentos
    obrigatórios na pasta de saída.
    """
    state = {
        "prd": "# PRD\nContent",
        "adr": "# ADR\nContent",
        "fdd": "# FDD\nContent",
        "design_doc": "# Design Doc\nContent"
    }
    
    # Usa uma pasta temporária para o teste
    test_output_dir = ".test_outputs"
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)
        
    try:
        save_docs(state, output_dir=test_output_dir)
        
        expected_files = ["PRD.md", "ADR.md", "FDD.md", "DesignDoc.md"]
        for file in expected_files:
            path = os.path.join(test_output_dir, file)
            assert os.path.exists(path), f"Arquivo {file} não foi gerado."
            with open(path, "r") as f:
                content = f.read()
                assert content.startswith("#"), f"Arquivo {file} não tem formato Markdown válido."
    finally:
        # Cleanup
        import shutil
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)
