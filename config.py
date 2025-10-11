## Place to manage settings

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///../instance/skutface.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "app/uploads"
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    JWT = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")