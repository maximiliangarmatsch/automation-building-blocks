from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from helper import get_db_connection
from api_helpers.date_scheduling.schedule_date import handle_date_schedule


schedule_date = Blueprint("schedule_date", __name__)


@schedule_date.route("/schedule_date", methods=["POST"])
@cross_origin()
def add_user_date():
    conn = get_db_connection()
    data = request.get_json()
    response, status_code = handle_date_schedule(data, conn)
    return jsonify(response), status_code
