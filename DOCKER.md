# ShopMarket - Docker Deployment Guide

Este guia explica como fazer deploy do ShopMarket usando Docker e Docker Compose.

## Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+

## Configuração Rápida

### 1. Clone o repositório

```bash
git clone https://github.com/mrmateussiilva/ShopMarket.git
cd ShopMarket
```

### 2. Configure as variáveis de ambiente (opcional)

O sistema já vem com um arquivo `docker.env` configurado. Para produção, edite-o:

```bash
# Edite docker.env conforme necessário
```

Edite o arquivo `docker.env` e altere:
- `SECRET_KEY`: Gere uma nova chave secreta para produção
- `ALLOWED_HOSTS`: Adicione seu domínio
- `DEBUG`: Mantenha como `False` em produção

### 3. Inicie os containers

```bash
docker-compose up -d --build
```

Este comando irá:
- Baixar as imagens necessárias
- Construir a imagem da aplicação
- Criar o banco de dados PostgreSQL
- Executar as migrações
- Criar um superusuário (admin/admin123)
- Popular o banco com dados de exemplo
- Iniciar o servidor Gunicorn

### 4. Acesse a aplicação

A aplicação estará disponível na porta definida em `PORT` (padrão `8001`):

- **Site**: http://localhost:8001/
- **Admin**: http://localhost:8001/admin/
  - Usuário: `admin`
  - Senha: `admin123`

## Comandos Úteis

### Ver logs

```bash
# Todos os serviços
docker-compose logs -f

# Apenas web
docker-compose logs -f web

# Apenas database
docker-compose logs -f db
```

### Executar comandos Django

```bash
# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Executar migrações
docker-compose exec web python manage.py migrate

# Popular banco de dados
docker-compose exec web python manage.py seed

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Shell do Django
docker-compose exec web python manage.py shell
```

### Parar os containers

```bash
# Parar sem remover
docker-compose stop

# Parar e remover containers
docker-compose down

# Parar e remover containers + volumes (CUIDADO: apaga o banco!)
docker-compose down -v
```

### Reconstruir a imagem

```bash
# Reconstruir e reiniciar
docker-compose up -d --build
```

### Acessar o shell do container

```bash
docker-compose exec web bash
```

### Backup do banco de dados

```bash
# Criar backup
docker-compose exec db pg_dump -U shopmarket shopmarket > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U shopmarket shopmarket < backup.sql
```

## Estrutura de Volumes

O Docker Compose cria os seguintes volumes:

- `postgres_data`: Dados do PostgreSQL (persistente)
- `./media`: Arquivos de mídia enviados pelos usuários
- `./staticfiles`: Arquivos estáticos coletados

## Variáveis de Ambiente

### Aplicação (web)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PORT` | Porta exposta no host | `8001` |
| `DEBUG` | Modo debug | `False` |
| `SECRET_KEY` | Chave secreta Django | (gerada) |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DATABASE_URL` | URL do banco PostgreSQL | (configurada) |

### Banco de Dados (db)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `POSTGRES_DB` | Nome do banco | `shopmarket` |
| `POSTGRES_USER` | Usuário | `shopmarket` |
| `POSTGRES_PASSWORD` | Senha | `shopmarket123` |

## Produção

### Segurança

Para produção, **SEMPRE**:

1. **Altere as senhas padrão**:
   - Senha do PostgreSQL
   - Senha do superusuário Django
   - SECRET_KEY do Django

2. **Configure HTTPS**:
   - Use um proxy reverso (Nginx/Traefik)
   - Configure certificados SSL

3. **Configure ALLOWED_HOSTS**:
   - Adicione apenas seus domínios reais

4. **Desative DEBUG**:
   - Mantenha `DEBUG=False`

### Exemplo com Nginx

Crie um arquivo `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./staticfiles:/app/staticfiles:ro
      - ./media:/app/media:ro
    depends_on:
      - web

  web:
    ports: []  # Remove exposição direta
```

### Escalabilidade

Para escalar a aplicação:

```bash
docker-compose up -d --scale web=3
```

## Troubleshooting

### Erro de conexão com banco de dados

Aguarde alguns segundos para o PostgreSQL inicializar completamente:

```bash
docker-compose logs db
```

### Permissões de arquivos

Se tiver problemas com permissões em `media/` ou `staticfiles/`:

```bash
sudo chown -R $USER:$USER media staticfiles
```

### Resetar tudo

Para começar do zero:

```bash
docker-compose down -v
docker-compose up -d --build
```

## Monitoramento

### Health Check

O PostgreSQL tem health check configurado. Verifique o status:

```bash
docker-compose ps
```

### Recursos

Monitore uso de recursos:

```bash
docker stats
```

## Suporte

Para problemas ou dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação do Django
- Verifique os logs: `docker-compose logs -f`
