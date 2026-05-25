ADR_PROMPT = """
Você é um Arquiteto de Software. Com base na entrevista, no PRD e no histórico de decisões abaixo, gere um Registro de Decisão de Arquitetura (ADR).
Concentre-se em uma decisão técnica fundamental (ex: escolha do banco de dados, linguagem ou framework).

Histórico e Contexto do Projeto:
{history}

O documento deve seguir o formato:
1. Título
2. Contexto
3. Decisão
4. Consequências

Entrevista:
{interview_text}

PRD Gerado:
{prd_text}
"""
