from src.memory.database import get_db_connection
from psycopg2.extras import RealDictCursor

class MemoryRepository:
    @staticmethod
    def add_decision(title, context, decision, consequences):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO decisions (title, context, decision, consequences) VALUES (%s, %s, %s, %s)",
            (title, context, decision, consequences)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_decisions():
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM decisions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_pattern(name, description, example):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patterns (name, description, example) VALUES (%s, %s, %s)",
            (name, description, example)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_patterns():
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM patterns")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update_project_context(key, value):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO project_context (key, value, updated_at) 
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
            """,
            (key, value)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_project_context():
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT key, value FROM project_context")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {row['key']: row['value'] for row in rows}

    @staticmethod
    def get_formatted_history():
        """
        Retorna uma string formatada com o histórico relevante para ser injetado no prompt.
        """
        decisions = MemoryRepository.get_all_decisions()
        patterns = MemoryRepository.get_all_patterns()
        context = MemoryRepository.get_project_context()
        
        history_str = ""
        
        if context:
            history_str += "\nContexto do Projeto:\n"
            for k, v in context.items():
                history_str += f"- {k}: {v}\n"
        
        if decisions:
            history_str += "\nDecisões Anteriores (ADRs):\n"
            for d in decisions[:5]: # Pegar as 5 mais recentes
                history_str += f"- {d['title']}: {d['decision']}\n"
                
        if patterns:
            history_str += "\nPadrões Identificados:\n"
            for p in patterns:
                history_str += f"- {p['name']}: {p['description']}\n"
                
        return history_str
