#!/bin/bash

# Script para executar o Ruff (linter) no projeto
# Uso: ./scripts/run_ruff.sh [argumentos extras, ex: --fix]

# Determina o comando ruff (usa venv se existir, caso contrário usa o global)
RUFF_CMD="ruff"
if [ -f "./.venv/bin/ruff" ]; then
    RUFF_CMD="./.venv/bin/ruff"
fi

echo "--- Executando Ruff (Linter) ---"
$RUFF_CMD check src/ tests/ "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Nenhum problema de linting encontrado."
else
    echo "❌ Problemas encontrados pelo Ruff."
fi

exit $EXIT_CODE
