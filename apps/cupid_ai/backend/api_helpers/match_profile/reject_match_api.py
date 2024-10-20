from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection, validate_required_fields
from api_helpers.match_profile.reject_match import delete_match_from_db

reject_match = Blueprint("reject_match", __name__)


@reject_match.route("/reject_match", methods=["DELETE"])
@cross_origin()
def reject_profile():
    data = request.json
    conn = get_db_connection()
    error_response = validate_required_fields(data, ["from_unique_id", "to_unique_id"])
    if error_response:
        return error_response
    try:
        rows_deleted = delete_match_from_db(data, conn)
        if rows_deleted == 0:
            return (
                jsonify({"status": "success", "message": "No matching profile found"}),
                404,
            )
        return (
            jsonify({"status": "success", "message": "Match rejected succesfully"}),
            200,
        )
    except Exception as e:
        return error_response(str(e), 500)
