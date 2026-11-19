#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/.."
if ! command -v git >/dev/null 2>&1; then echo "Instale o Git: pkg install git"; exit 1; fi
git init
git add .
git commit -m "Initial CONECTAQR SaaS MVP" || true
echo
read -r -p "Cole a URL HTTPS ou SSH do repositório GitHub: " REPO
if [ -z "$REPO" ]; then echo "Nenhum repositório informado. Repositório local preparado."; exit 0; fi
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git push -u origin main
echo "Código enviado ao GitHub."
