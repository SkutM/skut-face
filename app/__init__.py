from flask import Flask
from dotenv import load_dotenv
# stage 3
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")

    # stage 3
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # stage 3
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app