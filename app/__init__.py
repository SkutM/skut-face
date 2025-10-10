from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")

    print("✅ SkutFace configuration loaded:")
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    print(f"DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app