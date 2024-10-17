from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.match_accept.get_match_accepted import get_match_accepted


MEDIA_FOLDER = "uploads"
get_accepted_match = Blueprint("get_accepted_match", __name__)


@get_accepted_match.route("/get_accepted_match", methods=["POST"])
@cross_origin()
def accepted_profiles():
    connection = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if unique_id is None:
        return jsonify({"error": "unique_id is required"}), 400
    profiles = get_match_accepted(unique_id, connection)
    return profiles
