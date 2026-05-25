import os
import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.llm.ollama_loader import get_ollama_model
from src.prompts.prd import PRD_PROMPT
from src.prompts.adr import ADR_PROMPT
from src.prompts.fdd import FDD_PROMPT
from src.prompts.design_doc import DESIGN_DOC_PROMPT
from src.tools.mermaid_tool import save_diagram_to_file
from src.tools.plantuml_tool import save_plantuml_to_file
from src.config import settings
from src.memory.repository import MemoryRepository
from langchain_core.messages import HumanMessage

class AgentState(TypedDict):
    interview_text: str
    history: str
    prd: str
    adr: str
    fdd: str
    design_doc: str

def extract_and_save_diagrams(text: str, base_filename: str):
    """
    Extrai blocos de código mermaid e plantuml do texto e salva em arquivos.
    Usa regex flexíveis para lidar com variações de formatação do LLM.
    """
    # Extrair Mermaid - Flexível com espaços e quebras de linha opcionais
    mermaid_blocks = re.findall(r"```mermaid\s*\n?(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    for i, code in enumerate(mermaid_blocks):
        if code.strip():
            filename = f"{base_filename}_diagram_{i+1}.mmd"
            save_diagram_to_file.invoke({"mermaid_code": code.strip(), "filename": filename})
            print(f"  -> Diagrama Mermaid extraído: {filename}")

    # Extrair PlantUML - Flexível com espaços e quebras de linha opcionais
    plantuml_blocks = re.findall(r"```plantuml\s*\n?(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    for i, code in enumerate(plantuml_blocks):
        if code.strip():
            filename = f"{base_filename}_diagram_{i+1}.puml"
            save_plantuml_to_file.invoke({"plantuml_code": code.strip(), "filename": filename})
            print(f"  -> Diagrama PlantUML extraído: {filename}")

def enrich_history_node(state: AgentState):
    print("--- Carregando Histórico e Contexto ---")
    history = MemoryRepository.get_formatted_history()
    return {"history": history}

def generate_prd_node(state: AgentState):
    print("--- Gerando PRD ---")
    llm = get_ollama_model()
    prompt = PRD_PROMPT.format(
        interview_text=state["interview_text"],
        history=state.get("history", "Nenhum histórico disponível.")
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    extract_and_save_diagrams(content, "PRD")
    return {"prd": content}

def generate_adr_node(state: AgentState):
    print("--- Gerando ADR ---")
    llm = get_ollama_model()
    prompt = ADR_PROMPT.format(
        interview_text=state["interview_text"], 
        prd_text=state["prd"],
        history=state.get("history", "Nenhum histórico disponível.")
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    extract_and_save_diagrams(content, "ADR")
    return {"adr": content}

def generate_fdd_node(state: AgentState):
    print("--- Gerando FDD ---")
    llm = get_ollama_model()
    prompt = FDD_PROMPT.format(
        interview_text=state["interview_text"], 
        prd_text=state["prd"],
        history=state.get("history", "Nenhum histórico disponível.")
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    extract_and_save_diagrams(content, "FDD")
    return {"fdd": content}

def generate_design_doc_node(state: AgentState):
    print("--- Gerando Design Doc ---")
    llm = get_ollama_model()
    prompt = DESIGN_DOC_PROMPT.format(
        interview_text=state["interview_text"],
        prd_text=state["prd"],
        adr_text=state["adr"],
        fdd_text=state["fdd"],
        history=state.get("history", "Nenhum histórico disponível.")
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    extract_and_save_diagrams(content, "DesignDoc")
    return {"design_doc": content}

def update_memory_node(state: AgentState):
    print("--- Atualizando Memória do Projeto ---")
    # Tenta extrair a decisão principal do ADR se ele existir
    if state.get("adr"):
        # Regex mais flexível para capturar Título e Decisão em Markdown
        match_title = re.search(r"(?:1\.|\*\*)\s*Título\s*[:\*]*\s*(.*)", state["adr"], re.IGNORECASE)
        match_decision = re.search(r"(?:3\.|\*\*)\s*Decisão\s*[:\*]*\s*(.*)", state["adr"], re.IGNORECASE)
        
        if match_title and match_decision:
            title = match_title.group(1).strip().strip("*").strip()
            decision = match_decision.group(1).strip().strip("*").strip()
            MemoryRepository.add_decision(
                title=title,
                context="Extraído do ADR gerado",
                decision=decision,
                consequences="Verificar ADR.md"
            )
            print(f"Decisão salva: {title}")
    
    # Atualiza o contexto com o nome do projeto se encontrado no PRD
    if state.get("prd"):
        # Procura por "Visão Geral" ou o título principal do documento
        match_project = re.search(r"(?:Visão Geral|#)\s*(.*)", state["prd"], re.IGNORECASE)
        if match_project:
            project_name = match_project.group(1).strip().replace("**", "").replace("#", "")
            MemoryRepository.update_project_context("Último Projeto Analisado", project_name[:100])
            
    return {}

def create_doc_agent(checkpointer=None):
    workflow = StateGraph(AgentState)

    # Adicionando os nós
    workflow.add_node("enrich_history", enrich_history_node)
    workflow.add_node("generate_prd", generate_prd_node)
    workflow.add_node("generate_adr", generate_adr_node)
    workflow.add_node("generate_fdd", generate_fdd_node)
    workflow.add_node("generate_design_doc", generate_design_doc_node)
    workflow.add_node("update_memory", update_memory_node)

    # Definindo as arestas
    workflow.set_entry_point("enrich_history")
    workflow.add_edge("enrich_history", "generate_prd")
    workflow.add_edge("generate_prd", "generate_adr")
    workflow.add_edge("generate_prd", "generate_fdd")
    
    workflow.add_edge("generate_adr", "generate_design_doc")
    workflow.add_edge("generate_fdd", "generate_design_doc")
    
    workflow.add_edge("generate_design_doc", "update_memory")
    workflow.add_edge("update_memory", END)

    return workflow.compile(checkpointer=checkpointer)

def save_docs(state: AgentState, output_dir=None):
    if output_dir is None:
        output_dir = settings.OUTPUT_DOCS_DIR
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    docs = {
        "PRD.md": state["prd"],
        "ADR.md": state["adr"],
        "FDD.md": state["fdd"],
        "DesignDoc.md": state["design_doc"]
    }
    
    for filename, content in docs.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Arquivo salvo: {path}")
