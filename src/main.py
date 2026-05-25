from src.agent.doc_generator_agent import create_doc_agent, save_docs
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from src.config import settings
from src.memory.database import init_db

def main():
    # Inicializa as tabelas do histórico do projeto no Postgres
    try:
        init_db()
    except Exception as e:
        print(f"Aviso: Não foi possível inicializar o banco de dados de histórico: {e}")
        print("Certifique-se de que o PostgreSQL está rodando (via docker-compose ou LocalStack).")
    
    # Exemplo de entrevista simulada
    interview_text = """
    Entrevistador: Olá, queremos expandir a plataforma LocalFresh para incluir um sistema de logística própria.
    Cliente: Sim, agora queremos gerenciar nossa própria frota de entregadores ciclistas.
    
    Entrevistador: Quais as novas funcionalidades?
    Cliente: App para o entregador, cálculo de rota otimizada e rastreamento em tempo real para o cliente.
    
    Entrevistador: Alguma restrição?
    Cliente: Deve seguir os padrões que já estabelecemos nos projetos anteriores para manter a consistência.
    """

    print("--- Iniciando Agente de Documentação com Persistência (PostgreSQL) ---")
    
    # Configuração da string de conexão
    connection_string = settings.DATABASE_URL
    
    # Inicializa o checkpointer com PostgreSQL usando um pool de conexões
    try:
        with ConnectionPool(conninfo=connection_string, max_size=10) as pool:
            checkpointer = PostgresSaver(pool)
            
            # Cria as tabelas de checkpoint se não existirem
            checkpointer.setup()
            
            # Inicializa o agente (grafo compilado) com o checkpointer
            agent = create_doc_agent(checkpointer=checkpointer)
            
            # Define o estado inicial
            initial_state = {
                "interview_text": interview_text,
                "history": "",
                "prd": "",
                "adr": "",
                "fdd": "",
                "design_doc": ""
            }
            
            # Configuração da thread (id da conversa/projeto)
            config = {"configurable": {"thread_id": "projeto_local_fresh_pg_001"}}
            
            # Executa o agente
            final_state = agent.invoke(initial_state, config=config)
            
            # Salva os documentos gerados
            save_docs(final_state)
            
            print("\n--- Todos os documentos foram gerados com sucesso! ---")
            print(f"Estado salvo no thread_id: {config['configurable']['thread_id']} (PostgreSQL)")
            
    except Exception as e:
        print(f"Erro durante a execução do agente: {e}")
        print("\nDica: Verifique se o banco de dados PostgreSQL está acessível em:", connection_string)

if __name__ == "__main__":
    main()
