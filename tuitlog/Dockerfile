# Multi-stage build para produção otimizada
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências de build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Imagem final mínima
FROM python:3.11-slim

WORKDIR /app

# Copiar dependências instaladas
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY . .

# Configurar ambiente
ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Criar volumes para persistência de uploads e banco de dados
VOLUME ["/app/static/uploads", "/app/instance"]

# Expor porta
EXPOSE 8000

# Comando de inicialização com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
