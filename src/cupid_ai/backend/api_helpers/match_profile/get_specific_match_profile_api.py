from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.match_profile.get_specific_match import get_specific_match


MEDIA_FOLDER = "uploads"
get_specific_match_profile = Blueprint("get_specific_match_profile", __name__)


@get_specific_match_profile.route("/get_specific_match_profile", methods=["POST"])
@cross_origin()
def view_match_profile():
    conn = get_db_connection()
    data = request.get_json()
    from_unique_id = data.get("from_unique_id")
    to_unique_id = data.get("to_unique_id")
    if not from_unique_id or not to_unique_id:
        return (
            jsonify({"error": "Both from_unique_id and to_unique_id are required"}),
            400,
        )
    return jsonify(get_specific_match(from_unique_id, to_unique_id, conn), 200)
