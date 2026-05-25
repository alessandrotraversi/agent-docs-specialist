DESIGN_DOC_PROMPT = """
Você é um Engenheiro de Software Senior. Com base no PRD, ADR, FDD e no histórico abaixo, gere um Design Doc técnico.
O documento deve descrever a implementação técnica de alto nível.

Histórico e Contexto do Projeto:
{history}

O documento deve incluir:
1. Arquitetura Proposta (Inclua um diagrama PlantUML C4Context)
2. Modelo de Dados (Inclua um diagrama de Entidade-Relacionamento Mermaid ou diagrama de classe)
3. Endpoints da API (exemplos)
4. Considerações de Segurança

Instruções OBRIGATÓRIAS para diagramas:
1. Arquitetura C4: Use EXCLUSIVAMENTE o bloco de código ```plantuml.
   - NÃO use Mermaid para diagramas C4.
   - Use a sintaxe C4-PlantUML RIGOROSAMENTE (@startuml, !include ..., etc).
2. Outros Diagramas (ER, Fluxo, Classe): Use o bloco de código ```mermaid.

Exemplo PlantUML C4 (OBRIGATÓRIO para Arquitetura):
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-office/C4-PlantUML/master/C4_Context.puml
Person(customer, "Cliente", "...")
System(system, "Sistema", "...")
Rel(customer, system, "Usa")
@enduml
```

Entrevista:
{interview_text}

PRD Gerado:
{prd_text}
ADR Gerado:
{adr_text}
FDD Gerado:
{fdd_text}
"""
