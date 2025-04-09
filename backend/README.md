# 🛒 Loja Virtual - Backend

Este é o **backend** do projeto **Loja Virtual**, uma aplicação web desenvolvida como parte do MVP acadêmico da Sprint 3.

A API foi construída com **FastAPI**, utilizando **SQLite** para persistência de dados, adotando a arquitetura **MVC** e comunicação via **REST API** com o frontend. Ela é responsável por gerenciar os **pedidos** e **produtos** do sistema.

---

## 🚀 Tecnologias Utilizadas

- 🐍 Python 3.12+
- ⚡ FastAPI
- 🛠️ SQLAlchemy
- 💾 SQLite
- 🔥 Uvicorn
- 🐳 Docker

---

## ⚙️ Rodando o Backend Localmente

Siga os passos abaixo para executar o projeto no seu ambiente local.

### 📥 1. Clone o Repositório

```bash
git clone https://github.com/victorazevedo0/mvp-sprint-3---Loja-virtual.git
cd mvp-sprint-3---Loja-virtual/backend
```

## 🐍 2. Crie e Ative um Ambiente Virtual

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
```

## 📦 3. Instale as Dependências

```bash
pip install -r requeriments.txt
```

## ▶️ 4. Rode o Servidor

```bash
uvicorn app.main:app --reload
```

Após isso, o servidor estará disponível em: http://localhost:8000

## ⚙️ Rodando o Backend no Docker

Siga os passos abaixo para executar o projeto no seu ambiente local.

### 📥 1. Clone o Repositório

```bash
git clone https://github.com/victorazevedo0/mvp-sprint-3---Loja-virtual.git
cd mvp-sprint-3---Loja-virtual/backend
```

## 🐳 2. Rodando com Docker

📌 Pré-requisitos

Instale o Docker de acordo com seu sistema operacional:

    📥 Windows
    📥 Ubuntu
    📥 MacOS

    ⚠️ Usuários Windows: certifique-se de que a virtualização está habilitada na BIOS e que o WSL2 está corretamente instalado e configurado.

## 🧱 3. Construa a Imagem

```bash
docker build -t meu-backend .
```

## 🚀 4. Rode o Container

```bash
docker run -d -p 8000:8000 --name container-backend meu-backend
```

A API estará disponível em: http://localhost:8000
📌 Endpoints da API

Abaixo estão listados alguns dos principais endpoints disponíveis:
Método	Rota	Descrição
GET	/api/v1/orders	Lista todos os pedidos
GET	/api/v1/orders/{id}	Retorna um pedido específico
POST /api/v1/orders	Cria um novo pedido
PUT	/api/v1/orders/{id}	Atualiza um pedido existente
DELETE	/api/v1/orders/{id}	Remove um pedido

    Acesse a documentação interativa em: http://localhost:8000/docs

Segue documentação da API externa, no qual está sendo utilizada para carregar os produtos da API no projeto através de um GET.

[Fake Store](https://fakestoreapi.com/docs#tag/Products)

Obs: O projeto está com propensão de crescer, com cadastro de produtos, clientes e melhoria na estrutura de pedidos.

🧭 Diagrama da Arquitetura

A arquitetura segue o padrão MVC e comunicação via REST:

        Frontend (Html 5, Css3 Bootstrap e JS)
               │
               ▼
        FastAPI (Backend)
               │
               ▼
          SQLite (Banco de Dados)


**Desenvolvido por Victor Azevedo 💻**