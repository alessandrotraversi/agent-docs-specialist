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
    ruff_cmd = get_command("ruff")
    
    # Argumentos extras passados ao script
    extra_args = sys.argv[1:]
    
    print("--- Executando Ruff (Linter) ---")
    
    # Monta o comando completo
    cmd = [ruff_cmd, "check", "src/", "tests/"] + extra_args
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("✅ Nenhum problema de linting encontrado.")
        else:
            print("❌ Problemas encontrados pelo Ruff.")
            
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"Erro: Comando '{ruff_cmd}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar Ruff: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
