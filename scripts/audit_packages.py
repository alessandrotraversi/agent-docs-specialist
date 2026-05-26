import subprocess
import os
import sys

def get_command(command_name):
    """Retorna o caminho do comando no venv se existir, caso contrário o global."""
    venv_path = os.path.join(".venv", "bin", command_name)
    if os.path.exists(venv_path):
        return venv_path
    return command_name

def main():
    audit_cmd = get_command("pip-audit")
    
    print("--- Iniciando auditoria de segurança dos pacotes ---")
    
    try:
        # Executa o pip-audit
        result = subprocess.run([audit_cmd], check=False)
        
        if result.returncode == 0:
            print("✅ Nenhuma vulnerabilidade conhecida encontrada.")
        else:
            print("❌ Vulnerabilidades encontradas. Verifique a tabela acima.")
            
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"Erro: Comando '{audit_cmd}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar auditoria: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
