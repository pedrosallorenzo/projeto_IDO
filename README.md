Sistema de Reservas de Salas/Eventos
Projeto desenvolvido para a disciplina de Integração DevOps.

1. Integrantes
Mateus Reis — Desenvolvimento

Victor Marques Talá — Qualidade

Pedro Sallorenzo — Infraestrutura

2. Sobre o projeto
O projeto consiste em um sistema para gerenciamento de reservas de salas e eventos.

A aplicação permite cadastrar usuários e salas, criar e cancelar reservas e consultar a disponibilidade de uma sala em determinado período.

Uma das principais regras de negócio do sistema é impedir que duas reservas sejam criadas para a mesma sala em horários conflitantes.

3. Funcionalidades
Cadastro e listagem de usuários

Cadastro e listagem de salas

Criação de reservas

Listagem de reservas

Cancelamento de reservas

Validação de conflito de horários

Consulta de disponibilidade de salas

Cache de disponibilidade utilizando Redis

Interface web para interação com o sistema

4. Tecnologias utilizadas
Python

FastAPI

PostgreSQL

SQLAlchemy

Redis

HTML

CSS

JavaScript

Pytest

Docker

Docker Compose

Git

GitHub

GitHub Actions

GitHub Container Registry (GHCR)

5. Estrutura DevOps
O projeto utiliza uma estratégia baseada em branches curtas e Pull Requests para integração das alterações na branch main.

O pipeline de CI é executado automaticamente em pushes e Pull Requests direcionados para a main.

O CI realiza:

checkout do repositório;

configuração do Python;

instalação das dependências;

validação da sintaxe Python;

validação da aplicação FastAPI;

inicialização do Redis para os testes;

execução dos testes automatizados com Pytest.

O projeto também possui um workflow responsável pela publicação da imagem Docker no GitHub Container Registry.

A publicação é executada quando uma tag de versão no formato vX.Y.Z é enviada ao repositório.

Exemplo:

git tag v1.0.0
git push origin v1.0.0
A imagem é então publicada no GHCR com a versão correspondente e também com a tag latest.

6. Containers
A aplicação possui um Dockerfile para criação da imagem da API.

O docker-compose.yml permite executar os principais serviços do sistema:

aplicação FastAPI;

PostgreSQL;

Redis.

Para iniciar o ambiente com Docker Compose:

docker compose up --build
Após a inicialização, a aplicação fica disponível na porta 8000.

Para encerrar os containers:

docker compose down
7. Configuração das variáveis de ambiente
O projeto possui o arquivo .env.example, que pode ser utilizado como referência para criação do arquivo .env.

Exemplo:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=reservas_salas
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui

REDIS_HOST=localhost
REDIS_PORT=6379
O arquivo .env real não deve ser versionado no repositório.

8. Execução local sem Docker
1. Clonar o repositório
git clone https://github.com/pedrosallorenzo/projeto_IDO.git
2. Entrar na pasta do projeto
cd projeto_IDO
3. Criar um ambiente virtual
No Windows:

python -m venv .venv
No Linux/macOS:

python3 -m venv .venv
4. Ativar o ambiente virtual
Windows PowerShell:

.\.venv\Scripts\Activate.ps1
Linux/macOS:

source .venv/bin/activate
5. Instalar as dependências
python -m pip install -r requirements.txt
6. Criar o arquivo .env
Utilize o .env.example como referência e configure PostgreSQL e Redis.

7. Criar as tabelas
python -m app.init_db
8. Executar a aplicação
uvicorn app.main:app --reload
9. Acesso à aplicação
Interface:

http://127.0.0.1:8000
Documentação interativa da API:

http://127.0.0.1:8000/docs
10. Testes
Para executar os testes automatizados:

python -m pytest -v
11. Cache com Redis
O Redis é utilizado para armazenar temporariamente consultas de disponibilidade de salas.

Quando uma consulta de disponibilidade é realizada, a aplicação verifica primeiro se existe uma resposta armazenada no Redis.

Caso não exista, a disponibilidade é consultada no PostgreSQL e o resultado é armazenado temporariamente no cache.

Quando uma reserva é criada ou cancelada, o cache relacionado à sala é invalidado para evitar informações desatualizadas.
