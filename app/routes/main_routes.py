from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/api/test")
def test():
    return jsonify({"message": "SkutFace API is working!"})