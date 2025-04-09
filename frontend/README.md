# 🛒 Loja Virtual - Frontend

Este é o repositório **frontend** do projeto **Loja Virtual**, desenvolvido como parte do MVP da Sprint 3. A aplicação permite aos usuários visualizar produtos, adicionar itens ao carrinho e gerenciar pedidos de forma prática e intuitiva.

A interface é desenvolvida em **HTML, CSS (Bootstrap)** e **JavaScript**, consumindo uma API FastAPI no backend para funcionalidades como listagem, edição e exclusão de pedidos.

---

## 📷 Arquitetura da Aplicação

A arquitetura da aplicação foi baseada na separação de responsabilidades entre frontend e backend. O frontend é responsável por:

- Exibir produtos vindos da API externa (Fake Store API);
- Enviar pedidos para o backend;
- Consultar, editar e excluir pedidos já realizados por meio da API local.

### 🔁 Fluxo de Funcionamento

![imagem_fluxograma_projeto](./img/Fluxograma%20Software.jpg)
---

## ⚙️ Instalação e Uso

Siga as etapas abaixo para rodar o frontend localmente.

### ✅ Pré-requisitos

- Navegador web moderno (Google Chrome, Firefox, etc.)
- Editor de código (Visual Studio Code, por exemplo)
- Backend da aplicação em execução (FastAPI)
- Servidor local como o **Live Server** do VSCode (recomendado)

### 📦 Estrutura de Diretórios

frontend/ 
    ├── app/ 
_______├── static/ 
_____________├── order_manager.js
_____________├── script.js
_____________├── style.css
_______├── index.html 
_______├── order_manager.html
_______├── app.py
_______├── Dockerfile
_______├── requirements.txt
_______└── README.md

### ▶️ Passos para execução

1. Clone este repositório:

```bash
git clone https://github.com/victorazevedo0/mvp-sprint-3---Loja-virtual.git
```
2. Acesso a pasta frontend:

```bash
cd mvp-sprint-3---Loja-virtual/frontend
```

3. Abra o projeto no Visual Studio Code (ou editor de sua preferência).
   
4. Execute com o **Live Server** clicando com o botão direito sobre index.html e escolhendo "Open with Live Server".

Obs: **Certifique-se de que o backend (FastAPI) está rodando. (como informando no README.md do backend)**

## 🛠️ Tecnologias Utilizadas

    HTML5
    CSS3 (Bootstrap 5)
    JavaScript
    FastAPI (backend - API)
    FakeStore API (catálogo de produtos)

## ✨ Funcionalidades

    Listagem de produtos disponíveis
    Adição ao carrinho e finalização de pedidos
    Visualização de pedidos existentes
    Filtro por status e e-mail
    Edição e exclusão de pedidos via modal
