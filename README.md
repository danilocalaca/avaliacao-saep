# Biblioteca Escolar

Sistema web para controlar livros, usuários e empréstimos de uma biblioteca escolar. Permite cadastrar e consultar o acervo, registrar empréstimos e devoluções com controle automático de estoque e acompanhar o histórico e os relatórios.

## Funcionalidades

- Login com validação de campos e mensagem para acesso inválido
- Página principal com a quantidade de livros, de empréstimos ativos e de usuários
- Cadastro de livros: cadastrar, alterar, excluir e pesquisar por título, autor ou categoria
- Gestão de empréstimos: registrar empréstimo, registrar devolução e consultar histórico
- Bloqueio de empréstimo quando o livro não tem exemplares disponíveis
- Atualização automática da quantidade a cada empréstimo e devolução
- Relatório de empréstimos com filtro por período e situação
- Relatório dos livros mais emprestados

## Tecnologias

- Python 3 e Flask
- SQLite
- Jinja2, HTML, CSS e JavaScript

## Estrutura do projeto

```
biblioteca-escolar/
├── app.py
├── db.py
├── schema.sql
├── seed.sql
├── requirements.txt
├── templates/
├── static/
│   ├── css/estilo.css
│   └── js/
└── docs/
    ├── 01-requisitos-funcionais.md
    ├── 02-der.md
    ├── 03-casos-de-teste.md
    └── 04-requisitos-infraestrutura.md
```

## Como executar

Pré-requisito: Python 3.10 ou superior instalado.

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone <url-do-repositorio>
   cd biblioteca-escolar
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux e macOS
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o sistema:

   ```bash
   python app.py
   ```

5. Abra no navegador: http://127.0.0.1:5000

O banco de dados é criado automaticamente na primeira execução, com as tabelas de `schema.sql` e os dados iniciais de `seed.sql`. Para recomeçar do zero, apague o arquivo `.db` gerado e inicie o sistema de novo.

## Usuários de teste

| Nome | E-mail | Senha |
| --- | --- | --- |
| (preencher) | (preencher) | (preencher) |
| (preencher) | (preencher) | (preencher) |
| (preencher) | (preencher) | (preencher) |

Os dados desta tabela são os mesmos informados no `seed.sql`. As senhas ficam armazenadas no banco apenas como hash.

## Banco de dados

Três tabelas: `Usuario`, `Livro` e `Emprestimo`. Um usuário pode ter vários empréstimos e um livro pode aparecer em vários empréstimos. O diagrama completo está em [docs/02-der.md](docs/02-der.md).

Regras principais:

- A quantidade de um livro não pode ser negativa.
- Empréstimo ativo é aquele sem data de devolução.
- Empréstimo atrasado é o ativo cuja data prevista de devolução já passou.
- O e-mail de cada usuário é único.

## Documentação

- [Requisitos funcionais](docs/01-requisitos-funcionais.md)
- [Diagrama entidade relacionamento](docs/02-der.md)
- [Casos de teste](docs/03-casos-de-teste.md)
- [Requisitos de infraestrutura](docs/04-requisitos-infraestrutura.md)

## Autor

Danilo Calaça 3°D

