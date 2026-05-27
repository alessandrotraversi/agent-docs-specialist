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
    if len(sys.argv) < 2:
        print("Erro: Nome do pacote não fornecido.")
        print("Uso: python scripts/add_package.py <nome_do_pacote>")
        sys.exit(1)

    package_name = sys.argv[1]
    pip_cmd = get_command("pip")

    print(f"--- Instalando pacote: {package_name} ---")
    try:
        # Instala o pacote
        install_result = subprocess.run([pip_cmd, "install", package_name], check=False)
        if install_result.returncode != 0:
            print(f"❌ Erro ao instalar o pacote {package_name}.")
            sys.exit(install_result.returncode)

        print("--- Atualizando requirements.txt ---")
        # Atualiza o requirements.txt
        with open("requirements.txt", "w") as f:
            subprocess.run([pip_cmd, "freeze"], stdout=f, check=True)

        print("--- Validando segurança com pip-audit ---")
        # Chama o script de auditoria Python
        audit_result = subprocess.run([sys.executable, "scripts/audit_packages.py"], check=False)
        sys.exit(audit_result.returncode)

    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
