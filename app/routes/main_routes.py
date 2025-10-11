from flask import Blueprint, jsonify, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/register")
def register_page():
    return render_template("register.html")

@main_bp.route("/login")
def login_page():
    return render_template("login.html")

@main_bp.route("/api/test")
def test():
    return jsonify({"message": "SkutFace API is working!"})

# avoid circular
from flask import Blueprint, jsonify, request, current_app
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    allowed_extensions = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

@main_bp.route("/api/upload", methods=["POST"])
def upload_image():

    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400
    
    file = request.files["file"]

    # check if user *actually* selected a file
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg"}), 400
    
    filename = secure_filename(file.filename)

    upload_path = os.path.join(current_app.root_path, "uploads", filename)

    file.save(upload_path)
    
    preview_url = f"/uploads/{filename}"
    return jsonify({
        "message": f"File '{filename}' uploaded succesfully!",
        "preview_url": preview_url
    }), 200

from flask import send_from_directory

@main_bp.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    upload_folder = os.path.join(current_app.root_path, "uploads")
    return send_from_directory(upload_folder, filename)
    # safely sends files from specific folder


# phase 3

from deepface import DeepFace

@main_bp.route("/api/compare", methods=["POST"])
def compare_faces():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")

    if not file1 or not file2:
        return jsonify({"error": "Please upload two images: file1 and file2"}), 400
    
    path1 = os.path.join(current_app.root_path, "uploads", secure_filename(file1.filename))
    path2 = os.path.join(current_app.root_path, "uploads", secure_filename(file2.filename))
    file1.save(path1)
    file2.save(path2)

    try:
        result = DeepFace.verify(path1, path2)
        return jsonify({
            "verified": result["verified"],
            "distance": result["distance"],
            "model": result["model"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

