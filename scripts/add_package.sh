#!/bin/bash

# Script para adicionar um novo pacote e validar sua segurança
# Uso: ./scripts/add_package.sh <nome_do_pacote>

if [ -z "$1" ]; then
    echo "Erro: Nome do pacote não fornecido."
    echo "Uso: ./scripts/add_package.sh <nome_do_pacote>"
    exit 1
fi

PACKAGE_NAME=$1
VENV_PIP="./.venv/bin/pip"
VENV_PIP_AUDIT="./.venv/bin/pip-audit"

if [ ! -f "$VENV_PIP" ]; then
    echo "Erro: pip não encontrado no ambiente virtual."
    exit 1
fi

echo "--- Instalando pacote: $PACKAGE_NAME ---"
$VENV_PIP install "$PACKAGE_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar o pacote $PACKAGE_NAME."
    exit 1
fi

echo "--- Atualizando requirements.txt ---"
$VENV_PIP freeze > requirements.txt

echo "--- Validando segurança com pip-audit ---"
./scripts/audit_packages.sh
