from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection, validate_required_fields
from api_helpers.match_accept.accept_match import (
    insert_accepted_match,
    check_existing_match,
)

MEDIA_FOLDER = "uploads"
accept_match = Blueprint("accept_match", __name__)


@accept_match.route("/accept_match", methods=["POST"])
@cross_origin()
def add_accepted_match():
    data = request.get_json()
    error_response = validate_required_fields(
        data, ["to_user_id", "from_user_id", "answer"]
    )
    if error_response:
        return error_response
    conn = get_db_connection()
    if check_existing_match(conn, data):
        conn.close()
        return jsonify({"error": "Match already exists"}), 200
    insert_accepted_match(conn, data)
    conn.close()
    return jsonify({"message": "Accepted match added successfully"}), 200
