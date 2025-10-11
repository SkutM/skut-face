import os
import numpy as np
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, create_refresh_token
from deepface import DeepFace

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

# helper: computes embedding vector from uploaded face
def get_face_embedding(img_path):
    # return a 1D numpy array representing face embedding
    try:
        # deepface.represent returns a list of dicts; take the first embedding
        result = DeepFace.represent(img_path=img_path, model_name="VGG-Face", enforce_detection=True)
        embedding = np.array(result[0]["embedding"])
        return embedding
    except Exception as e:
        raise ValueError(f"Face embedding failed: {str(e)}")
    

# Register route
@auth_bp.route("/register", methods=["POST"])
def register_user():
    email = request.form.get("email")
    file = request.files.get("file")

    if not email or not file:
        return jsonify({"error": "Email and file are required"}), 400
    
    # prevent dupe users
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400
    
    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        embedding = get_face_embedding(save_path)
        user = User(email=email)
        user.embedding = embedding.tolist() # save as JSON
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
# Login route
@auth_bp.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("email")
    file = request.files.get("file")

    if not email or not file:
        return jsonify({"error": "Email and file are required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        # compute current embedding
        new_embedding = get_face_embedding(save_path)

        # compute cosine similarity
        stored = np.array(user.embedding)
        distance = np.dot(stored, new_embedding) / (np.linalg.norm(stored) * np.linalg.norm(new_embedding))

        if distance > 0.60: # threshold ~0.85 works well for cosine similarity
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify({
                "message": "Login successful",
                "similarity": float(distance),
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"error": "Face not recognized", "similarity": float(distance)}), 401
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500 