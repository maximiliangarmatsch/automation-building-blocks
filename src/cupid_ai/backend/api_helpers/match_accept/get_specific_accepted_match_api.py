from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.match_accept.get_specific_match_accepted import (
    get_specific_match_accepted,
)

get_specific_accepted_match = Blueprint("get_specific_accepted_match", __name__)


@get_specific_accepted_match.route("/get_specific_accepted_match", methods=["POST"])
@cross_origin()
def specific_match_accepted():
    conn = get_db_connection()
    data = request.get_json()
    from_unique_id = data.get("from_unique_id")
    to_unique_id = data.get("to_unique_id")
    if not from_unique_id or not to_unique_id:
        return (
            jsonify({"error": "Both from_unique_id and to_unique_id are required"}),
            400,
        )
    return jsonify(get_specific_match_accepted(from_unique_id, to_unique_id, conn), 200)
