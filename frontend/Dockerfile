FROM python:3.12.4-slim

WORKDIR /app

RUN pip install fastapi uvicorn jinja2

COPY app.py /app/
COPY app/index.html /app/templates/
COPY app/order_manager.html /app/templates/
COPY app/static/ /app/static/

EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]