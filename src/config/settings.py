import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho para a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carrega variáveis do arquivo .env se ele existir
load_dotenv(BASE_DIR / ".env")

# Configurações do Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Configurações de saída
OUTPUT_DOCS_DIR = BASE_DIR / os.getenv("OUTPUT_DOCS_DIR", ".outputs")

# Configurações do Banco de Dados (PostgreSQL)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432") # Porta padrão do Postgres
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# URI de conexão para o SQLAlchemy/Psycopg2
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
