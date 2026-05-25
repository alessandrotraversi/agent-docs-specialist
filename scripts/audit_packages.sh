#!/bin/bash

# Script para auditar pacotes instalados no ambiente virtual
# Uso: ./scripts/audit_packages.sh

# Determina o comando pip-audit (usa venv se existir, caso contrário usa o global)
AUDIT_CMD="pip-audit"
if [ -f "./.venv/bin/pip-audit" ]; then
    AUDIT_CMD="./.venv/bin/pip-audit"
fi

echo "--- Iniciando auditoria de segurança dos pacotes ---"
$AUDIT_CMD
AUDIT_EXIT_CODE=$?

if [ $AUDIT_EXIT_CODE -eq 0 ]; then
    echo "✅ Nenhuma vulnerabilidade conhecida encontrada."
else
    echo "❌ Vulnerabilidades encontradas. Verifique a tabela acima."
fi

exit $AUDIT_EXIT_CODE
