# Sistema de Gestão de Oficina 🚗🔧

API REST desenvolvida com Flask para gerenciamento de clientes, veículos e ordens de serviço.

## 🚀 Tecnologias
- Flask
- PostgreSQL
- Docker
- Flask-Migrate
- JWT Authentication

## 📦 Funcionalidades
- Cadastro e login de usuários
- Gestão de clientes
- Gestão de veículos
- Ordens de serviço
- Relacionamento entre entidades

## ▶️ Como rodar

```bash
docker-compose up --build
```


---

## 2. 🔐 Usar `.env` (se ainda não fez completo)

No `__init__.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')