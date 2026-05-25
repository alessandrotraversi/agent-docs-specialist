#!/bin/bash

# Script para auditar pacotes instalados no ambiente virtual
# Uso: ./scripts/audit_packages.sh

VENV_PYTHON="./.venv/bin/python"
VENV_PIP_AUDIT="./.venv/bin/pip-audit"

if [ ! -f "$VENV_PIP_AUDIT" ]; then
    echo "Erro: pip-audit não encontrado em $VENV_PIP_AUDIT"
    echo "Certifique-se de que o ambiente virtual está configurado e pip-audit está instalado."
    exit 1
fi

echo "--- Iniciando auditoria de segurança dos pacotes ---"
$VENV_PIP_AUDIT
AUDIT_EXIT_CODE=$?

if [ $AUDIT_EXIT_CODE -eq 0 ]; then
    echo "✅ Nenhuma vulnerabilidade conhecida encontrada."
else
    echo "❌ Vulnerabilidades encontradas. Verifique a tabela acima."
fi

exit $AUDIT_EXIT_CODE
