## Place to manage settings

# os.getenv, like Flask, reads env variables (secret key, db URL)
# BUT os.getenv lets you "safely fall back to defaults."
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///../instance/skutface.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False