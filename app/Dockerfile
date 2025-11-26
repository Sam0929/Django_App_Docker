# Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# Define diretório de trabalho no container
WORKDIR /app

# Variáveis para evitar arquivos .pyc e buffer no log
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para mysqlclient (se necessário)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# Instala dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copia o código do projeto
COPY . /app/

# Comando padrão (substitui o arquivo systemd do Gunicorn)
# Nota: workers=3 conforme sua config anterior
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "MyProject.wsgi:application"]