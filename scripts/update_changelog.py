import subprocess
import datetime
import os
import sys

def main():
    print("--- Atualizando CHANGELOG.md ---")
    
    try:
        # Obtém a data atual
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Obtém a mensagem do último commit via git
        # git log -1 --pretty=%B | head -n 1
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        commit_msg = result.stdout.splitlines()[0] if result.stdout else "No commit message"
        
        changelog_path = "CHANGELOG.md"
        header = "# Changelog\n\nTodas as alterações notáveis neste projeto serão documentadas neste arquivo.\n\n"
        new_entry = f"### [{date_str}]\n- {commit_msg}\n\n"
        
        content = ""
        if os.path.exists(changelog_path):
            with open(changelog_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # O script original ignorava as primeiras 4 linhas se o arquivo existisse
                # para remontar com o cabeçalho fixo.
                # Aqui vamos pegar o conteúdo a partir de onde terminaria o cabeçalho padrão.
                # Se o arquivo for muito curto ou diferente, vamos apenas anexar o resto.
                found_content = False
                for i, line in enumerate(lines):
                    if i >= 4: # Pula o cabeçalho fixo (aprox 4 linhas)
                        content += line
                        found_content = True
        
        # Reconstrói o arquivo
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(new_entry)
            f.write(content)
            
        print("✅ CHANGELOG.md atualizado com sucesso.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter informações do Git: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao atualizar CHANGELOG.md: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
