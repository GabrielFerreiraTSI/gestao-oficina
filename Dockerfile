FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask flask_sqlalchemy psycopg2-binary flask-migrate

CMD ["python", "run.py"]