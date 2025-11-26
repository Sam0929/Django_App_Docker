# CoinFlip - Projeto Django com Docker

Este projeto roda uma aplicação Django completa utilizando Docker Compose, orquestrando containers para a Aplicação (Gunicorn), Banco de Dados (MySQL) e Proxy Reverso (Nginx).

## 📋 Pré-requisitos

* [Docker](https://www.docker.com/get-started)

---

## 🚀 Instalação e Inicialização

Siga os passos abaixo na ordem exata para configurar o ambiente pela primeira vez.

### 1. Configurar Variáveis de Ambiente
```sh
cp .env.example .env
```

### 2. Construir e Subir os Containers
```sh
docker-compose up -d --build
```

### 3. Criar as Tabelas no Banco de Dados
```sh
docker-compose exec web python manage.py migrate
```

### 4. Configurar Arquivos Estáticos (CSS/JS)
```sh
docker-compose exec web python manage.py collectstatic --no-input
```

### 5. Configurar Mídia Padrão
```sh
docker cp ./app/Projeto_1_Nuvem/default.jpg coinflip_web:/app/mediafiles/default.jpg
```

### 6. Criar Superusuário (Admin)
```sh
docker-compose exec web python manage.py createsuperuser
```

### 7. Acesse a aplicação
```sh
http://localhost:8080
```
