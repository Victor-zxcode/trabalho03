# API de Categorias e Produtos

Projeto acadêmico da disciplina de Arquitetura de Software. A API representa
um catálogo simples, no qual uma categoria pode estar relacionada a vários
produtos e cada produto pertence a uma categoria. Os textos apresentados na
documentação da API estão em português; os caminhos das rotas e os nomes das
propriedades JSON permanecem em inglês.

## Modelo de dados

- **Categoria:** identificador (`id`) e nome (`name`).
- **Produto:** identificador (`id`), nome (`name`) e identificador da categoria
  (`category_id`).
- **Relacionamento:** `products.category_id` é uma chave estrangeira para
  `categories.id`. Os modelos também expõem o relacionamento por
  `relationship()` do SQLAlchemy.

## Tecnologias

- FastAPI
- SQLAlchemy
- Alembic
- SQLite

## Instalação e execução

Com o Python instalado, execute na raiz do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

A documentação interativa da API fica em <http://127.0.0.1:8000/docs>.
O arquivo SQLite `catalog.db` é criado na raiz do projeto pela migração.
O banco não é criado por `create_all`; sua estrutura é gerenciada pelo Alembic.
O arquivo do banco é local e não é enviado ao GitHub. Em uma instalação limpa,
`alembic upgrade head` cria as tabelas vazias; cadastre os dados de demonstração
pelos endpoints antes de testar consultas e relacionamentos.

Para preparar dados pelo Swagger (`/docs`), crie uma categoria em
`POST /categories`, por exemplo:

```json
{
  "name": "Informática"
}
```

Use o `id` retornado (substitua `1` pelo identificador da sua categoria) para
cadastrar produtos em `POST /products`:

```json
{
  "name": "Teclado",
  "category_id": 1
}
```

Repita o cadastro para as demais categorias e produtos usados na demonstração.

Para gerar novas migrações após alterar os modelos:

```powershell
alembic revision --autogenerate -m "descreva a alteracao"
alembic upgrade head
```

## Rotas disponíveis

| Método | Caminho | Descrição |
| --- | --- | --- |
| `POST` | `/categories` | Criar uma categoria |
| `GET` | `/categories` | Listar categorias |
| `GET` | `/categories/{category_id}` | Consultar uma categoria |
| `GET` | `/categories/{category_id}/products` | Listar os produtos de uma categoria |
| `PUT` | `/categories/{category_id}` | Atualizar uma categoria |
| `DELETE` | `/categories/{category_id}` | Excluir uma categoria sem produtos |
| `POST` | `/products` | Criar um produto (verifica se a categoria existe) |
| `GET` | `/products` | Listar produtos |
| `GET` | `/products/{product_id}` | Consultar um produto |
| `PUT` | `/products/{product_id}` | Atualizar um produto |
| `DELETE` | `/products/{product_id}` | Excluir um produto |

Criações retornam `201`; um recurso não encontrado retorna `404`; dados
inválidos são rejeitados pela validação da API com `422`. A exclusão de uma
categoria que ainda possui produtos retorna `409`.
