PRD_PROMPT = """
Você é um Gerente de Produto experiente. Com base na entrevista e no histórico de decisões abaixo, gere um Documento de Requisitos do Produto (PRD).
O documento deve incluir:
1. Visão Geral
2. Público-Alvo
3. Problemas que Resolve
4. Principais Funcionalidades
5. Métricas de Sucesso

Histórico e Contexto do Projeto:
{history}

Entrevista:
{interview_text}
"""
