#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "== CONECTAQR | Preparação do Termux =="
pkg update -y
pkg install -y python git openssl

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(48))')
  sed -i "s|troque-esta-chave-por-uma-chave-aleatoria-longa|$SECRET|" .env
fi
mkdir -p data
echo
echo "Instalação concluída."
echo "Para iniciar: ./scripts/run_termux.sh"
