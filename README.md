# Sistema de Reservas de Salas/Eventos

## 1. Identificação

- **Nome:** Victor Marques Talá, Pedro Sallorenzo, Mateus Reis
- **Disciplina:** Integração DevOps

## 2. Tema escolhido

Sistema de Reservas de Salas/Eventos.

## 3. Descrição do Projeto

O projeto consiste em um sistema desenvolvido em Python para gerenciamento de reservas de salas e eventos.

A aplicação permite organizar o processo de reservas, realizando o gerenciamento de usuários, salas e reservas. O sistema utiliza FastAPI para disponibilizar seus recursos por meio de uma API, facilitando a comunicação entre as diferentes funcionalidades da aplicação.

## 4. Tecnologias utilizadas

- Python
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Pytest

## 5. Guia rápido de execução

**Pré-requisitos:**
- Python instalado.
- PostgreSQL configurado.
- Redis configurado.

**Passo 1 — Clonar o repositório**

```bash
git clone https://github.com/pedrosallorenzo/projeto_IDO.git
```

**Passo 2 — Entrar na pasta do projeto**

```bash
cd projeto_IDO
```

**Passo 3 — Criar ambiente virtual**

```bash
py -m venv .venv
```

**Passo 4 — Ativar o ambiente virtual**

```bash
.venv\Scripts\activate
```

**Passo 5 — Instalar as dependências**

```bash
py -m pip install -r requirements.txt
```

**Passo 6 — Configurar as variáveis de ambiente**

Criar um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência e preenchendo os dados de conexão.

**Passo 7 — Executar a aplicação**

```bash
uvicorn app.main:app --reload
```

Após iniciar, acessar no navegador:

```text
http://127.0.0.1:8000
```

A documentação interativa da API pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```
