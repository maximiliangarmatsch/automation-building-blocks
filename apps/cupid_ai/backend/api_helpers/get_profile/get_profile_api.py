import os
from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin

from api_helpers.get_profile.profile_data import get_user_profile
from helper import get_db_connection

MEDIA_FOLDER = "uploads"
get_profile = Blueprint("get_profile", __name__)


@get_profile.route("/get_profile", methods=["POST"])
@cross_origin()
def get_profile_method():
    conn = get_db_connection()
    data = request.json
    if not data or "unique_id" not in data:
        return jsonify({"error": "Missing unique_id"}), 422
    unique_id = data["unique_id"]
    if not unique_id:
        return make_response(jsonify({"message": "unique_id is required"}), 400)
    profile_data = get_user_profile(unique_id, conn)
    if not profile_data:
        return jsonify({"error": "Profile not found for the provided unique_id"}), 404
    return jsonify(profile_data), 200
