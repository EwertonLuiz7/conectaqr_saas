# CONECTAQR SaaS — MVP 1.0

Plataforma inicial de identidade digital, QR Codes dinâmicos e conexão com WhatsApp.

## 1. Recursos desta versão

- Cadastro e login com token JWT.
- Perfil digital público personalizável.
- QR Codes dinâmicos com destinos para perfil, WhatsApp ou URL.
- Redirecionamento e contagem de leituras.
- Estatísticas totais e últimos 30 dias.
- Limite de QR Codes por plano.
- Interface responsiva para celular e computador.
- API documentada automaticamente pelo FastAPI em `/docs`.

## 2. Estrutura

```text
conectaqr_saas/
├── backend/
│   ├── routes/
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── frontend/
│   ├── assets/
│   ├── index.html
│   └── profile.html
├── scripts/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Executar no computador

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edite `.env` e altere `SECRET_KEY`. Depois:

```bash
export PYTHONPATH=.
uvicorn backend.main:app --reload
```

No Windows PowerShell, use `$env:PYTHONPATH="."` antes do comando.

Abra `http://127.0.0.1:8000`. Documentação da API: `http://127.0.0.1:8000/docs`.

## 4. Instalação automatizada no Termux

Extraia o ZIP no armazenamento do Termux ou clone o repositório. Entre na pasta do projeto e execute:

```bash
bash scripts/termux_setup.sh
bash scripts/run_termux.sh
```

Se o script não executar diretamente, use `bash` como nos exemplos acima. No Android, abra `http://127.0.0.1:8000` no navegador.

Para permitir acesso por outros dispositivos na mesma rede Wi-Fi, o servidor escuta em `0.0.0.0`. Use o IP local do telefone e mantenha o Termux ativo.

## 5. Enviar para o GitHub pelo Termux

Crie um repositório vazio no GitHub (sem README inicial). Depois:

```bash
bash scripts/github_deploy.sh
```

Cole a URL HTTPS ou SSH do repositório. Para HTTPS, autentique usando um Personal Access Token quando o Git solicitar; não coloque tokens dentro dos arquivos do projeto.

Fluxo manual alternativo:

```bash
git init
git add .
git commit -m "Initial CONECTAQR SaaS MVP"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

## 6. Testes

```bash
source .venv/bin/activate
pip install pytest
pytest -q
```

## 7. Banco de dados

Por padrão, usa SQLite (`sqlite:///./conectaqr.db`) para facilitar o desenvolvimento local.

Para produção, configure PostgreSQL em `DATABASE_URL`, por exemplo:

```text
postgresql+psycopg://usuario:senha@host:5432/conectaqr
```

O usuário de banco deve ter permissões mínimas necessárias. Configure backups e migrações antes de produção. Esta versão cria tabelas automaticamente; para evolução de schema, adote Alembic.

## 8. Configuração de ambiente

- `SECRET_KEY`: chave secreta longa e aleatória. Obrigatória trocar antes de publicar.
- `DATABASE_URL`: conexão do banco.
- `BASE_URL`: URL pública real da aplicação, incluindo HTTPS em produção.
- `ENVIRONMENT`: `development` ou `production`.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: duração dos tokens.

Não envie `.env` ao GitHub. O `.gitignore` já o exclui.

## 9. Fluxo de utilização

1. Crie uma conta na página inicial.
2. Edite seu perfil e informe WhatsApp com DDI + DDD + número.
3. Crie um QR Code com destino Perfil, WhatsApp ou URL.
4. Baixe o PNG do QR Code.
5. Escaneie com outro aparelho para testar.
6. Consulte as estatísticas no painel.

## 10. Limitações conhecidas do MVP

- Cobrança recorrente ainda não está integrada; os planos pagos são demonstrativos.
- O plano do usuário é inicialmente `free`. Alterações de plano são administrativas/manuais nesta versão.
- Não há recuperação de senha por e-mail.
- Não há painel administrativo web completo, equipe multiusuário, catálogo ou API oficial do WhatsApp nesta entrega.
- As estatísticas registram leituras do redirecionador, mas ainda não filtram sofisticadamente bots e pré-visualizadores.
- A geração de QR Code depende de `BASE_URL` correto e acessível publicamente.
- SQLite é para desenvolvimento e testes; produção deve usar PostgreSQL, HTTPS, backups e migrações.
- Antes de uso comercial, implemente política de privacidade, termos de uso, controles de abuso, rate limiting, logs e revisão de segurança.

## 11. Deploy em produção

O ZIP inclui `Dockerfile` e `docker-compose.yml` como ponto de partida. Em hospedagem pública:
1. Configure PostgreSQL gerenciado.
2. Configure `SECRET_KEY` forte por variável de ambiente.
3. Configure `BASE_URL` com HTTPS.
4. Defina `ENVIRONMENT=production`.
5. Configure domínio, proxy HTTPS, backups e monitoramento.
6. Restrinja CORS ao domínio oficial.
7. Adote Alembic para migrações e revise a segurança.

O Termux é adequado para desenvolvimento, testes e demonstração. Para serviço comercial 24/7, utilize hospedagem de produção; o telefone pode desligar, perder conexão ou encerrar processos em segundo plano.

## 12. Próximas versões

- Integração Mercado Pago com webhooks verificados.
- Painel de administração.
- Gestão multiempresa e equipes.
- Catálogos e campanhas.
- Estatísticas com filtros anti-bot e privacidade.
- Recuperação de senha e verificação de e-mail.
- Testes de integração e pipeline CI/CD.
