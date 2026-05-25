FDD_PROMPT = """
Você é um Analista de Sistemas. Com base no PRD, na entrevista e no histórico abaixo, gere um Documento de Design Funcional (FDD).
Descreva detalhadamente como uma das principais funcionalidades deve se comportar.

Histórico e Contexto do Projeto:
{history}

O documento deve incluir:
1. Descrição da Funcionalidade
2. Fluxo do Usuário (Inclua um diagrama de sequência ou fluxograma em Mermaid)
3. Casos de Borda
4. Regras de Negócio

Instruções para diagramas:
- Use blocos de código ```mermaid para os diagramas.

Entrevista:
{interview_text}

PRD Gerado:
{prd_text}
"""
