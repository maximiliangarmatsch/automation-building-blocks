from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin

# Create auth module imports
from api_helpers.auth.helpers import (
    extract_user_login_data,
    fetch_user_by_email,
    hash_user_password,
    authenticate_user,
)
from api_helpers.auth.create_new_user import create_new_user
from helper import get_db_connection


auth = Blueprint("auth", __name__)


@auth.route("/auth", methods=["POST"])
@cross_origin()
def authenticate():
    data = request.json
    user_data, error_message, error_code = extract_user_login_data(data)
    if error_message:
        return jsonify({"error": error_message}), error_code
    email = user_data["email"]
    password = user_data["password"]
    hashed_password = hash_user_password(password)
    conn = get_db_connection()
    user = fetch_user_by_email(conn, email)
    if user:
        auth_response, auth_code = authenticate_user(user, hashed_password)
        conn.close()
        return make_response(jsonify(auth_response), auth_code)
    else:
        unique_id = create_new_user(conn, email, hashed_password)
        conn.close()
        return make_response(
            jsonify({"message": "User created successfully!", "unique_id": unique_id}),
            201,
        )
