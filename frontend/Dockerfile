FROM python:3.9-slim

WORKDIR /app

# Instalar dependências primeiro para melhor cache
RUN pip install fastapi uvicorn jinja2

# Copiar aplicação
COPY app.py /app/
COPY app/index.html /app/templates/
COPY app/order_manager.html /app/templates/
COPY app/static/ /app/static/

EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]