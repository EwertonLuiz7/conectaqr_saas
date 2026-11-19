#!/usr/bin/env bash
set -e
echo "Este script deve ser executado na raiz do projeto já extraído."
mkdir -p backend/routes frontend/assets scripts tests data
touch backend/__init__.py backend/routes/__init__.py
echo "Estrutura verificada/criada."
