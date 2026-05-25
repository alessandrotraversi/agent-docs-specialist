#!/bin/bash

# Script para ejecutar pruebas con Pytest
# Uso: ./scripts/run_tests.sh [argumentos extras]

# Determina o comando pytest (usa venv se existir, caso contrário usa o global)
PYTEST_CMD="pytest"
if [ -f "./.venv/bin/pytest" ]; then
    PYTEST_CMD="./.venv/bin/pytest"
fi

echo "--- Executando Testes com Pytest ---"
# Executa com cobertura no diretório src e gera relatório no terminal
$PYTEST_CMD --cov=src --cov-report=term-missing tests/ "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
else
    echo "❌ Alguns testes falharam."
fi

exit $EXIT_CODE
