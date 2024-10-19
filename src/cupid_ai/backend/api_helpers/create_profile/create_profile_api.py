from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

# Create Profile module imports
from api_helpers.create_profile.extract_profile_data import extract_profile_data
from api_helpers.create_profile.helpers import (
    check_mandatory_fields,
    user_profile_exists,
    calculate_bmi,
    handle_create_profile,
    handle_update_profile,
)
from helper import get_db_connection

create_profile = Blueprint("create_profile", __name__)


@create_profile.route("/create_profile", methods=["POST"])
@cross_origin()
def create_or_update_user_profile():
    data = request.json
    are_fields_present, missing_fields = check_mandatory_fields(data)
    if not are_fields_present:
        return (
            jsonify(
                {"error": f'Missing mandatory fields: {", ".join(missing_fields)}'}
            ),
            400,
        )
    profile_data = extract_profile_data(data)
    conn = get_db_connection()
    cursor = conn.cursor()
    bmi = calculate_bmi(profile_data["weight"], profile_data["height"])
    if user_profile_exists(cursor, profile_data["unique_id"]):
        return handle_update_profile(conn, profile_data, bmi)
    else:
        return handle_create_profile(conn, profile_data, bmi)
