from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.date_scheduling.get_schedule_date import handle_get_schedule_date


get_schedule_date = Blueprint("get_schedule_date", __name__)


@get_schedule_date.route("/get_schedule_date", methods=["POST"])
@cross_origin()
def get_schedule_date_method():
    conn = get_db_connection()
    data = request.get_json()
    unique_id = data.get("unique_id")
    if not unique_id:
        return jsonify({"error": "'unique_id' is required."}), 400
    response, status_code = handle_get_schedule_date(unique_id, conn)
    return jsonify(response), status_code
