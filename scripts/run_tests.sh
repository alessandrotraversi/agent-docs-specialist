#!/bin/bash

# Script para ejecutar pruebas con Pytest
# Uso: ./scripts/run_tests.sh [argumentos extras]

VENV_PYTEST="./.venv/bin/pytest"

if [ ! -f "$VENV_PYTEST" ]; then
    echo "Erro: pytest não encontrado em $VENV_PYTEST"
    echo "Certifique-se de que o ambiente virtual está configurado e pytest está instalado."
    exit 1
fi

echo "--- Executando Testes com Pytest ---"
# Executa com cobertura no diretório src e gera relatório no terminal
$VENV_PYTEST --cov=src --cov-report=term-missing tests/ "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
else
    echo "❌ Alguns testes falharam."
fi

exit $EXIT_CODE
