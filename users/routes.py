from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200