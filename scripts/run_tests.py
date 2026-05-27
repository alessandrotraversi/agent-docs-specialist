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
    pytest_cmd = get_command("pytest")
    
    # Argumentos extras passados ao script
    # Se o primeiro argumento for um diretório existente dentro de tests/, usa ele.
    # Caso contrário, usa o diretório padrão 'tests/' e passa todos os argumentos como extras.
    target_test = "tests/"
    extra_args = sys.argv[1:]
    
    if len(sys.argv) > 1 and (os.path.isdir(sys.argv[1]) or sys.argv[1].startswith("tests/")):
        target_test = sys.argv[1]
        extra_args = sys.argv[2:]

    print(f"--- Executando Testes com Pytest em: {target_test} ---")
    
    # Monta o comando completo: pytest --cov=src --cov-report=term-missing <target_test>
    cmd = [pytest_cmd, "--cov=src", "--cov-report=term-missing", target_test] + extra_args
    
    try:
        # Garante que o PYTHONPATH inclua o diretório atual para as importações do src
        env = os.environ.copy()
        current_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f".:{current_pythonpath}" if current_pythonpath else "."
        
        result = subprocess.run(cmd, check=False, env=env)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
        else:
            print("❌ Alguns testes falharam.")
            
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"Erro: Comando '{pytest_cmd}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar testes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
