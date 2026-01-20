# ShopMarket - E-commerce de Supermercado

MVP funcional de e-commerce de supermercado usando Django (server-rendered) + HTML templates + uv.

## Stack Tecnológica

- **Django 5+**: Framework web Python
- **SQLite**: Banco de dados
- **Templates Django**: Renderização server-side
- **CSS simples**: Estilização sem frameworks
- **UV**: Gerenciador de pacotes Python

## Funcionalidades

### Loja (Contexto Obrigatório)
- Seleção de loja pelo usuário
- `store_id` salvo na sessão
- Catálogo, preço e carrinho dependem da loja selecionada
- Ao trocar de loja, o carrinho é limpo automaticamente

### Catálogo
- Categorias hierárquicas
- Produtos com nome, slug, código
- Múltiplas imagens por produto
- Preços por loja (regular, promocional, clube)
- Exibição de desconto percentual quando existir

### Páginas
- `/` - Home com banners e vitrine de produtos
- `/c/<slug>/` - Categoria com paginação (20 itens) e ordenação
- `/p/<slug>/<id>/` - Detalhe do produto
- `/carrinho/` - Carrinho de compras
- `/checkout/` - Finalização de compra
- `/pedidos/` - Lista de pedidos do usuário
- `/listas/` - Listas de desejos (wishlist)

### Carrinho
- Baseado em sessão (funciona para usuários anônimos)
- Merge automático após login
- Cálculo de totais: produtos, desconto, subtotal
- Função para limpar carrinho
- Limpa automaticamente ao trocar de loja

### Checkout / Pedido
- Métodos de entrega: delivery | pickup
- Métodos de pagamento: online | on_delivery | in_store
- Criação de Order e OrderItem
- Sistema de status simples

### Listas / Repetir Pedido
- Wishlist (listas de produtos)
- Funcionalidade de repetir pedido (cria novo carrinho com itens do pedido anterior)

### Autenticação
- Login/Cadastro usando sistema padrão do Django
- Proteção de rotas que requerem autenticação

### Admin
- Interface administrativa completa para:
  - Lojas
  - Categorias
  - Produtos + imagens
  - Preços por loja
  - Banners
  - Pedidos

## Estrutura de Apps

```
shopmarket/
├── stores/         # Gerenciamento de lojas
├── catalog/        # Produtos e categorias
├── pricing/        # Preços por loja
├── cart/           # Carrinho de compras
├── orders/         # Processamento de pedidos
├── lists/          # Listas de desejos
└── cms/            # Banners e conteúdo
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- UV (gerenciador de pacotes)

### Instalação do UV

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou via pip
pip install uv
```

## 🐳 Deploy com Docker (Recomendado para Produção)

A forma mais rápida de rodar o ShopMarket é usando Docker Compose:

```bash
# Clone o repositório
git clone https://github.com/mrmateussiilva/ShopMarket.git
cd ShopMarket

# Inicie os containers
docker-compose up -d

# Acesse em http://localhost:8000
# Admin: admin / admin123
```

**Veja o guia completo em [DOCKER.md](DOCKER.md)**

---

## 💻 Setup Local (Desenvolvimento)

1. **Clone ou navegue até o diretório do projeto**

```bash
cd /home/mateus/Projetcs/Finderbit/ShopMarket
```

2. **Instale as dependências**

```bash
uv pip install django pillow
```

3. **Execute as migrações**

```bash
uv run python manage.py migrate
```

4. **Crie um superusuário**

```bash
uv run python manage.py createsuperuser
```

5. **Popule o banco de dados com dados de exemplo**

```bash
uv run python manage.py seed
```

Este comando criará:
- 2 lojas
- 5 categorias
- 20 produtos
- Preços variados para cada loja
- Dados prontos para teste

6. **Execute o servidor de desenvolvimento**

```bash
uv run python manage.py runserver
```

7. **Acesse a aplicação**

- **Site**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/

## Fluxo de Uso

1. **Selecione uma loja** - Ao acessar pela primeira vez, você será direcionado para selecionar uma loja
2. **Navegue pelo catálogo** - Explore categorias e produtos
3. **Adicione produtos ao carrinho** - Clique em "Adicionar ao Carrinho"
4. **Visualize o carrinho** - Veja seus itens e totais
5. **Faça login** - Necessário para finalizar a compra
6. **Finalize a compra** - Escolha método de entrega e pagamento
7. **Acompanhe seus pedidos** - Veja o histórico em "Meus Pedidos"
8. **Repita pedidos** - Adicione rapidamente itens de pedidos anteriores ao carrinho

## Comandos Úteis

### Criar migrações após alterações nos models
```bash
uv run python manage.py makemigrations
```

### Aplicar migrações
```bash
uv run python manage.py migrate
```

### Criar superusuário
```bash
uv run python manage.py createsuperuser
```

### Popular banco de dados
```bash
uv run python manage.py seed
```

### Executar servidor
```bash
uv run python manage.py runserver
```

### Acessar shell do Django
```bash
uv run python manage.py shell
```

## Estrutura de Templates

```
templates/
├── base.html                          # Template base
├── partials/
│   ├── header.html                    # Cabeçalho
│   └── footer.html                    # Rodapé
├── components/
│   ├── product_card.html              # Card de produto
│   └── cart_summary.html              # Resumo do carrinho
├── stores/
│   └── select_store.html              # Seleção de loja
├── catalog/
│   ├── home.html                      # Página inicial
│   ├── category_list.html             # Lista de produtos por categoria
│   └── product_detail.html            # Detalhe do produto
├── cart/
│   └── cart_detail.html               # Carrinho de compras
├── orders/
│   ├── checkout.html                  # Finalização de compra
│   ├── order_list.html                # Lista de pedidos
│   └── order_detail.html              # Detalhe do pedido
└── lists/
    ├── list_view.html                 # Visualização de listas
    ├── list_detail.html               # Detalhe da lista
    └── list_create.html               # Criação de lista
```

## Tecnologias e Decisões de Design

- **Server-rendered**: Sem SPA, sem JavaScript complexo
- **Session-based cart**: Carrinho funciona sem login
- **Store context**: Preços e disponibilidade dependem da loja selecionada
- **Simple CSS**: Estilização limpa e responsiva sem frameworks
- **Django Admin**: Interface administrativa completa e customizada

## Próximos Passos (Fora do MVP)

- Sistema de busca de produtos
- Filtros avançados por categoria
- Sistema de avaliações de produtos
- Cupons de desconto
- Integração com gateway de pagamento
- Sistema de notificações
- Rastreamento de pedidos
- API REST para mobile

## Licença

Este é um projeto de demonstração/MVP.

## Suporte

Para questões ou suporte, entre em contato através do repositório do projeto.
