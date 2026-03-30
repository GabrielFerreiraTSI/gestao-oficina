from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.cliente import Cliente
    from app.models.veiculo import Veiculo
    from app.models.ordem_servico import OrdemServico
    from app.models.user import User

    from app.routes.cliente_routes import cliente_bp
    from app.routes.veiculo_routes import veiculo_bp
    from app.routes.ordem_routes import ordem_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.health_check import health_bp

    app.register_blueprint(cliente_bp)
    app.register_blueprint(veiculo_bp)
    app.register_blueprint(ordem_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)

    return app