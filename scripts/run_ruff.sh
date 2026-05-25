#!/bin/bash

# Script para executar o Ruff (linter) no projeto
# Uso: ./scripts/run_ruff.sh [argumentos extras, ex: --fix]

VENV_RUFF="./.venv/bin/ruff"

if [ ! -f "$VENV_RUFF" ]; then
    echo "Erro: ruff não encontrado em $VENV_RUFF"
    echo "Certifique-se de que o ambiente virtual está configurado e ruff está instalado."
    exit 1
fi

echo "--- Executando Ruff (Linter) ---"
$VENV_RUFF check src/ tests/ "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Nenhum problema de linting encontrado."
else
    echo "❌ Problemas encontrados pelo Ruff."
fi

exit $EXIT_CODE
