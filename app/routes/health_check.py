# em qualquer blueprint ou em um novo arquivo de rotas
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200