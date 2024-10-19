from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.match_profile.get_match_profile import get_match_profiles


MEDIA_FOLDER = "uploads"
get_match_profile = Blueprint("get_match_profile", __name__)


@get_match_profile.route("/get_match_profile", methods=["POST"])
@cross_origin()
def get_profiles():
    conn = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if unique_id is None:
        return jsonify({"error": "unique_id is required"}), 400
    profiles = get_match_profiles(unique_id, conn=conn)
    return profiles
