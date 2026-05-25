import psycopg2
from src.config import settings

def get_db_connection():
    """
    Retorna uma conexão com o banco de dados PostgreSQL do projeto.
    """
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS
    )
    return conn

def init_db():
    """
    Inicializa as tabelas do banco de dados se elas não existirem.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela para decisões (ADRs consolidadas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        context TEXT,
        decision TEXT NOT NULL,
        consequences TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabela para padrões arquiteturais/código
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patterns (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        example TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabela para metadados do projeto/lições aprendidas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_context (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Banco de dados PostgreSQL inicializado com sucesso.")

if __name__ == "__main__":
    init_db()
