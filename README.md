#  SkutFace
Face-based authentication web app built with Flask, DeepFace, and JWT.

##  Features
- Register and log in with face recognition
- AI-powered embedding comparison (DeepFace + VGG-Face)
- JSON Web Tokens (JWT) for secure sessions
- SQLite + SQLAlchemy for persistent storage
- Responsive dark-themed UI with live image preview

##  How It Works
1. User uploads a face image.
2. Flask sends it to DeepFace, & model generates a 2622-dimension embedding.
3. The embedding is stored in the database (JSON).
4. On login, another embedding is generated.
5. Flask compares both using cosine similarity.
6. If above threshold, then it returns JWT token.

##  How to Run
```bash
python -m venv venv
source venv\Scripts\activate 
pip install -r requirements.txt
python run.py
