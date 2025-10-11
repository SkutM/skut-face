import json
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    embedding_json = db.Column(db.Text, nullable=False) # store list[float] as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def embedding(self):
        return json.loads(self.embedding_json)
    
    @embedding.setter
    def embedding(self, vector):
        self.embedding_json = json.dumps(vector)