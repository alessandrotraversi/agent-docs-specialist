import sys
import re
import subprocess

# Regex para Conventional Commits
CONVENTIONAL_COMMIT_REGEX = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.*\))?!?: .+$"

def check_commit_message(message):
    if not re.match(CONVENTIONAL_COMMIT_REGEX, message):
        return False
    return True

def get_commit_messages(commit_range=None):
    try:
        args = ["git", "log", "--pretty=%B"]
        if commit_range:
            args.append(commit_range)
        else:
            args.append("-1")
            
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        # O git log separa as mensagens por \n\n se usarmos %B puro, mas queremos processar cada commit separadamente.
        # Usaremos %s para o título que é o que importa para conventional commits.
        args[2] = "--pretty=%s"
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Erro ao obter mensagens de commit: {e}")
        return []

def main():
    commit_range = sys.argv[1] if len(sys.argv) > 1 else None
    
    messages = get_commit_messages(commit_range)
    
    if not messages:
        print("Nenhuma mensagem de commit encontrada para validar.")
        sys.exit(0)
        
    errors = 0
    for msg in messages:
        if not msg.strip(): continue
        print(f"Analisando: {msg}")
        if not check_commit_message(msg):
            print(f"  ❌ FALHA: '{msg}' não segue o padrão.")
            errors += 1
        else:
            print(f"  ✅ OK")
            
    if errors > 0:
        print(f"\nTotal de erros encontrados: {errors}")
        print("O formato deve ser: tipo(escopo): assunto")
        print("Tipos válidos: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert")
        sys.exit(1)
    
    print("\n✅ Todos os commits seguem o padrão Conventional Commits.")
    sys.exit(0)

if __name__ == "__main__":
    main()
