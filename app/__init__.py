from flask import Flask
from dotenv import load_dotenv

def create_app():
    # .env values (like SECRET_KEY) avaialbe when app starts
    load_dotenv()

    # "use a separate instance/ folder as a safe home for
    # runtime files -- and make it accessible via
    # app.instance_path"
    # this way, we can later do:
    # app.config.from_pyfile("config.py", silent=True)
    # and Flask will look inside:
    # skutface/instance/config.py
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")

    print("✅ SkutFace configuration loaded:")
    print(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    print(f"DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app